import asyncio

from config import config
from parser.browser_manager import BrowserManager
from agent.graph import create_agent_graph
from database.service import DatabaseService
from cli.interface import CLIInterface
from exceptions.domain_error import DomainError


async def main():
    """Main entry point for the Chrome Agent"""
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"\n❌ Ошибка конфигурации: {e}\n")
        return
    
    # Debug mode info
    if config.is_debug():
        print(f"\n🔧 DEBUG MODE: {config}\n")
    
    print("\n🚀 Запуск Chrome Agent...")
    
    # Initialize components
    browser_manager = BrowserManager()
    db_service = DatabaseService()
    
    try:
        # Start browser
        print("📱 Запуск браузера...")
        await browser_manager.start()
        print("✓ Браузер запущен\n")
        
        # Create agent graph
        agent_graph = create_agent_graph(browser_manager.page, config.groq_api_key)
        
        # Start CLI
        cli = CLIInterface(db_service)
        await cli.run(agent_graph, browser_manager)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Получен сигнал прерывания...")
    except DomainError as e:
        print(f"\n❌ {e.error_reason}")
        print(f"💡 {e.proposed_fix}\n")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}\n")
    finally:
        # Cleanup
        print("\n🔄 Завершение работы...")
        await browser_manager.stop()
        print("✓ Браузер закрыт")
        print("✓ Сессии сохранены")
        print("\nДо встречи! 👋\n")


if __name__ == "__main__":
    asyncio.run(main())
