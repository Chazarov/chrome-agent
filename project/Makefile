.DEFAULT_GOAL := help

AGENT_CORE_V2 := agent-core-v2

.PHONY: help install-playwright test-notificator

help:
	@echo Доступные команды:
	@echo   make install-playwright  Установить браузер Chromium для Playwright
	@echo   make test-notificator      Запуск демо статус-виджета агента в браузере

install-playwright:
	cd $(AGENT_CORE_V2) && python -m playwright install chromium

test-notificator: install-playwright
	cd $(AGENT_CORE_V2) && python -m tests.test_notificator
