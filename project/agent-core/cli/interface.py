import asyncio
from typing import Optional
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage

from config import config
from agent.debug_tools import log_error
from models.session import Session, SessionStatus
from database.service import DatabaseService
from agent.state import AgentState
from exceptions.tool_execution import ToolExecutionError
from exceptions.browser_closed import BrowserClosedError
from exceptions.function_call_format import FunctionCallFormatError
from exceptions.domain_error import DomainError
from exceptions.unknown_error import UnknownError


class CLIInterface:
    """Command-line interface for interacting with the agent"""
    
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.current_session: Optional[Session] = None
    
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "="*60)
        print("  Chrome Agent - AI Browser Automation")
        print("="*60)
        print("\nКоманды:")
        print("  /exit     - Выход из программы")
        print("  /new      - Начать новую сессию")
        print("  /history  - Показать историю текущей сессии")
        print("\nПросто напишите задачу для агента, чтобы начать работу.")
        print("="*60 + "\n")
    
    def start_new_session(self):
        """Start a new session"""
        self.current_session = self.db_service.create_session()
        print(f"\n✓ Новая сессия создана: {self.current_session.id[:8]}...\n")
    
    def show_history(self):
        """Show current session history"""
        if not self.current_session:
            print("\n⚠ Нет активной сессии. Используйте /new для создания.\n")
            return
        
        session = self.db_service.get_session(self.current_session.id)
        if not session or not session.messages:
            print("\n⚠ История сессии пуста.\n")
            return
        
        print("\n" + "-"*60)
        print(f"История сессии {session.id[:8]}...")
        print("-"*60)
        
        for msg in session.messages:
            timestamp = msg.timestamp.strftime("%H:%M:%S")
            role_emoji = "👤" if msg.role == "user" else "🤖"
            print(f"\n[{timestamp}] {role_emoji} {msg.role.upper()}:")
            print(f"{msg.content[:200]}{'...' if len(msg.content) > 200 else ''}")
        
        print("-"*60 + "\n")
    
    async def run(self, agent_graph, browser_manager):
        """Main CLI loop"""
        self.print_banner()
        self.start_new_session()
        
        try:
            while True:
                try:
                    user_input = input("Вы: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle commands
                    if user_input.startswith("/"):
                        await self.handle_command(user_input, agent_graph, browser_manager)
                        continue
                    
                    # Process user message
                    await self.process_message(user_input, agent_graph)
                    
                except KeyboardInterrupt:
                    print("\n\n⚠ Прервано. Используйте /exit для выхода.\n")
                    continue
                except Exception as e:
                    print(f"\n❌ Ошибка: {e}\n")
                    continue
                    
        except KeyboardInterrupt:
            print("\n\nВыход...")
        finally:
            if self.current_session:
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.COMPLETED
                )
    
    async def handle_command(self, command: str, agent_graph, browser_manager):
        """Handle special commands"""
        if command == "/exit":
            print("\nЗавершение работы...")
            if self.current_session:
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.COMPLETED
                )
            raise KeyboardInterrupt
        
        elif command == "/new":
            if self.current_session:
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.COMPLETED
                )
            self.start_new_session()
        
        elif command == "/history":
            self.show_history()
        
        else:
            print(f"\n⚠ Неизвестная команда: {command}\n")
    
    async def process_message(self, message: str, agent_graph):
        """Process user message through the agent"""
        if not self.current_session:
            print("\n⚠ Нет активной сессии. Создание новой...\n")
            self.start_new_session()
        
        # Save user message
        self.db_service.save_message(
            self.current_session.id,
            "user",
            message
        )
        
        print(f"\n🤖 Агент думает...\n")
        
        # Create initial state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=message)],
            "current_page": None,
            "task": message,
            "completed": False,
            "error": None
        }
        
        # Run agent with retry logic for recoverable errors
        MAX_RETRIES = config.agent_max_retries
        retry_count = 0
        current_state = initial_state
        
        while retry_count <= MAX_RETRIES:
            try:
                step_count = 0
                async for event in agent_graph.astream(current_state):
                    step_count += 1
                    
                    # Extract node name and state
                    for node_name, node_state in event.items():
                        if node_name == "agent":
                            last_message = node_state["messages"][-1]
                            
                            # Display model reasoning (check both possible locations)
                            reasoning_content = None
                            if hasattr(last_message, "reasoning") and last_message.reasoning:
                                reasoning_content = last_message.reasoning
                            elif hasattr(last_message, "additional_kwargs") and "reasoning_content" in last_message.additional_kwargs:
                                reasoning_content = last_message.additional_kwargs["reasoning_content"]
                            
                            if reasoning_content:
                                print(f"\n💭 Размышления модели:")
                                print("-" * 60)
                                print(reasoning_content)
                                print("-" * 60 + "\n")
                            
                            # Check for tool calls
                            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                                for tool_call in last_message.tool_calls:
                                    tool_name = tool_call.get("name", "unknown")
                                    print(f"  → Вызов инструмента: {tool_name}")
                            
                            # Check for text response
                            if hasattr(last_message, "content") and last_message.content:
                                if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                                    print(f"\n💬 Агент: {last_message.content}\n")
                                    
                                    # Save assistant message
                                    self.db_service.save_message(
                                        self.current_session.id,
                                        "assistant",
                                        last_message.content
                                    )
                        
                        elif node_name == "tools":
                            # Tool execution results
                            if "messages" in node_state:
                                for msg in node_state["messages"]:
                                    if hasattr(msg, "content"):
                                        print(f"  ✓ Результат: {msg.content[:100]}...")
                    
                    # Prevent infinite loops
                    if step_count > config.agent_max_steps:
                        print(f"\n⚠ Достигнут лимит шагов ({config.agent_max_steps}). Остановка.\n")
                        break
                
                print("\n✓ Задача завершена.\n")
                break
                
            except ToolExecutionError as e:
                retry_count += 1
                if retry_count > MAX_RETRIES:
                    print(f"\n❌ Превышен лимит попыток ({MAX_RETRIES})")
                    print(f"❌ Ошибка: {e.error_reason}\n")
                    
                    self.db_service.save_message(
                        self.current_session.id,
                        "system",
                        f"Failed after {MAX_RETRIES} attempts: {e.error_reason}"
                    )
                    self.db_service.update_session_status(
                        self.current_session.id,
                        SessionStatus.FAILED
                    )
                    break
                
                # Add error to context and let agent retry
                error_message = (
                    f"Tool execution failed: {e.error_reason}\n"
                    f"Suggested fix: {e.proposed_fix}\n"
                    f"Attempt {retry_count}/{MAX_RETRIES}. Try alternative approach."
                )
                
                current_state["messages"].append(SystemMessage(content=error_message))
                
                print(f"\n⚠️ Попытка {retry_count}/{MAX_RETRIES}: {e.error_reason}")
                print(f"💡 Подсказка: {e.proposed_fix}")
                print("🔄 Агент попробует снова...\n")
                
                self.db_service.save_message(
                    self.current_session.id,
                    "system",
                    error_message
                )
                
            except BrowserClosedError as e:
                print(f"\n❌ {e.error_reason}")
                print(f"💡 {e.proposed_fix}\n")
                
                self.db_service.save_message(
                    self.current_session.id,
                    "system",
                    f"Browser closed: {e.error_reason}"
                )
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.FAILED
                )
                break
                
            except FunctionCallFormatError as e:
                print(f"\n❌ Критическая ошибка: {e.error_reason}")
                print(f"💡 Требуется: {e.proposed_fix}\n")
                
                self.db_service.save_message(
                    self.current_session.id,
                    "system",
                    f"Critical error: {e.error_reason}. Required: {e.proposed_fix}"
                )
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.FAILED
                )
                break
                
            except DomainError as e:
                print(f"\n❌ Ошибка: {e.error_reason}")
                print(f"💡 Решение: {e.proposed_fix}\n")
                
                self.db_service.save_message(
                    self.current_session.id,
                    "system",
                    f"Error: {e.error_reason}. Fix: {e.proposed_fix}"
                )
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.FAILED
                )
                break
                
            except Exception as e:
                unknown_error = UnknownError(e)
                log_error(unknown_error)
                print(f"\n❌ {unknown_error.error_reason}")
                print(f"💡 {unknown_error.proposed_fix}\n")
                
                self.db_service.save_message(
                    self.current_session.id,
                    "system",
                    f"Unexpected error: {unknown_error.error_reason}"
                )
                self.db_service.update_session_status(
                    self.current_session.id,
                    SessionStatus.FAILED
                )
                break
