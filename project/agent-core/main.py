import asyncio
import os
from dotenv import load_dotenv

from parser.browser_manager import BrowserManager
from agent.graph import create_agent_graph
from database.service import DatabaseService
from cli.interface import CLIInterface


async def main():
    """Main entry point for the Chrome Agent"""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n❌ Ошибка: GROQ_API_KEY не найден в переменных окружения.")
        print("Создайте файл .env и добавьте: GROQ_API_KEY=your_key_here\n")
        return
    
    print("\n🚀 Запуск Chrome Agent...")
    
    # Initialize components
    browser_manager = BrowserManager()
    db_service = DatabaseService()
    
    try:
        # Start browser
        print("📱 Запуск браузера...")
        await browser_manager.start(headless=False)
        print("✓ Браузер запущен\n")
        
        # Create agent graph
        agent_graph = create_agent_graph(browser_manager.page, api_key)
        
        # Start CLI
        cli = CLIInterface(db_service)
        await cli.run(agent_graph, browser_manager)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Получен сигнал прерывания...")
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
