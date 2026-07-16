"""Демо статус-виджета: при переходе по ссылке id уровня опасности меняется случайно."""

from __future__ import annotations

import random
import time

from playwright.sync_api import Page, sync_playwright
from playwright_stealth import Stealth

from domain.models import DangerLevel, DangerLevelBase, DangerReason
from preview.playwright_pv.danger_notificator import PlaywrightDangerNotificator

DANGER_LEVELS: list[tuple[int, str, str]] = [
    (0, "Безопасно", "Страница не вызывает подозрений"),
    (1, "Осторожно", "Есть незначительные признаки риска"),
    (2, "Подозрительно", "Обнаружены признаки возможной угрозы"),
    (3, "Опасно", "Высокий уровень угрозы для пользователя"),
]

REASONS: list[tuple[int, str, str]] = [
    (0, "Домен в белом списке", "Сайт ранее не вызывал жалоб"),
    (1, "Новый домен", "Домен зарегистрирован недавно"),
    (2, "Подозрительные ключевые слова", "На странице найдены тревожные формулировки"),
    (3, "Известная фишинговая схема", "Поведение страницы совпадает с мошенническими паттернами"),
]


def _random_danger_level() -> tuple[DangerLevel, DangerReason]:
    level_id, level_name, level_description = random.choice(DANGER_LEVELS)
    prev_id, prev_name, prev_description = random.choice(DANGER_LEVELS)
    reason_id, reason_name, reason_description = random.choice(REASONS)

    danger_level = DangerLevel(
        id=level_id,
        name=level_name,
        description=level_description,
        prev_state=DangerLevelBase(
            id=prev_id,
            name=prev_name,
            description=prev_description,
        ),
    )
    reason = DangerReason(
        id=reason_id,
        name=reason_name,
        description=reason_description,
    )
    return danger_level, reason


def _notify_random(notificator: PlaywrightDangerNotificator) -> int:
    danger_level, reason = _random_danger_level()
    notificator.danger_level_notify(danger_level, reason)
    return danger_level.id


def _on_navigation(
    page: Page,
    notificator: PlaywrightDangerNotificator,
) -> None:
    def handle_navigation(frame: object) -> None:
        if frame != page.main_frame:
            return
        level_id = _notify_random(notificator)
        print(f"Навигация: {page.url} -> уровень опасности id={level_id}")

    page.on("framenavigated", handle_navigation)


def run_demo() -> None:
    with Stealth().use_sync(sync_playwright()) as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        notificator = PlaywrightDangerNotificator(page)
        _on_navigation(page, notificator)

        page.goto("https://example.com", wait_until="domcontentloaded")
        initial_id = _notify_random(notificator)
        print(f"Старт: {page.url} -> уровень опасности id={initial_id}")
        print("Переходите по ссылкам на странице — виджет будет обновляться.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Завершение демо.")
        finally:
            browser.close()


if __name__ == "__main__":
    run_demo()
