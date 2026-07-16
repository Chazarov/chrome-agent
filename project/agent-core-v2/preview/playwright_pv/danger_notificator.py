from __future__ import annotations

import base64
import json
from pathlib import Path

from playwright.sync_api import Page

from domain.interfaces.notificator import Notificator
from domain.models import DangerLevel, DangerReason

STATIC_DIR = Path(__file__).resolve().parents[2] / "static"
COMPONENTS_DIR = Path(__file__).parent / "components"
MASCOT_IMAGE_COUNT = 5

WIDGET_INIT_SCRIPT_TEMPLATE = (COMPONENTS_DIR / "init_widjet.js").read_text()

UPDATE_WIDGET_SCRIPT = (COMPONENTS_DIR / "update_widjet.js").read_text()


WARNING_IMAGE_KEY = 5


def _load_mascot_data_urls() -> dict[int, str]:
    images: dict[int, str] = {}
    for index in range(1, MASCOT_IMAGE_COUNT + 1):
        path = STATIC_DIR / f"{index}.png"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        images[index] = f"data:image/png;base64,{encoded}"
    return images


def _build_widget_init_script(mascot_images: dict[int, str]) -> str:
    return WIDGET_INIT_SCRIPT_TEMPLATE.format(
        mascot_images_json=json.dumps(mascot_images),
    )


def _image_key_for_level(level_id: int) -> int:
    return min(max(level_id + 1, 1), MASCOT_IMAGE_COUNT)


class PlaywrightDangerNotificator(Notificator):
    def __init__(self, page: Page) -> None:
        self._page = page
        self._mascot_images = _load_mascot_data_urls()
        self._widget_init_script = _build_widget_init_script(self._mascot_images)
        self._attach_widget()

    def _attach_widget(self) -> None:
        self._page.context.add_init_script(self._widget_init_script)
        self._page.evaluate(self._widget_init_script)

    def danger_level_notify(
        self,
        danger_level: DangerLevel,
        reason: DangerReason,
    ) -> None:
        self._page.evaluate(
            UPDATE_WIDGET_SCRIPT,
            {
                "imageKey": _image_key_for_level(danger_level.id),
                "description": (
                    f"{danger_level.name}. {danger_level.description}. "
                    f"{reason.name}. {reason.description}"
                ),
            },
        )

    def warning_notify(self, warning: str) -> None:
        self._page.evaluate(
            UPDATE_WIDGET_SCRIPT,
            {
                "imageKey": WARNING_IMAGE_KEY,
                "description": warning,
            },
        )
