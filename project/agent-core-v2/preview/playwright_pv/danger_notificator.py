from __future__ import annotations

from playwright.sync_api import Page

from domain.interfaces.notificator import Notificator
from domain.models import DangerLevel, DangerReason

WIDGET_INIT_SCRIPT = """
(() => {
    if (window.__chromeAgentWidgetInstalled) return;
    window.__chromeAgentWidgetInstalled = true;

    const ensureWidget = () => {
        let widget = document.getElementById('chrome-agent-status-widget');
        if (widget) return widget;

        const style = document.createElement('style');
        style.textContent = `
            #chrome-agent-status-widget {
                position: fixed;
                top: 12px;
                right: 12px;
                z-index: 2147483647;
                width: 72px;
                height: 72px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 6px;
                border-radius: 4px;
                box-sizing: border-box;
                color: #fff;
                font: 600 11px/1.2 system-ui, sans-serif;
                text-align: center;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.45);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
                pointer-events: none;
                user-select: none;
            }
        `;
        (document.head || document.documentElement).appendChild(style);

        widget = document.createElement('div');
        widget.id = 'chrome-agent-status-widget';
        widget.setAttribute('role', 'status');
        widget.setAttribute('aria-live', 'polite');
        widget.textContent = 'Агент';
        widget.style.backgroundColor = '#64748b';
        (document.body || document.documentElement).appendChild(widget);
        return widget;
    };

    window.__chromeAgentUpdateStatusWidget = (payload) => {
        const widget = ensureWidget();
        widget.textContent = payload.label;
        widget.style.backgroundColor = payload.color;
        if (payload.description) {
            widget.setAttribute('aria-label', payload.description);
            widget.title = payload.description;
        }
    };

    const boot = () => ensureWidget();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
"""

UPDATE_WIDGET_SCRIPT = """
(payload) => {
    if (typeof window.__chromeAgentUpdateStatusWidget === 'function') {
        window.__chromeAgentUpdateStatusWidget(payload);
    }
}
"""

DANGER_LEVEL_COLORS: dict[int, str] = {
    0: "#22c55e",
    1: "#eab308",
    2: "#f97316",
    3: "#ef4444",
}

DEFAULT_COLOR = "#64748b"
WARNING_COLOR = "#f97316"


class PlaywrightDangerNotificator(Notificator):
    def __init__(self, page: Page) -> None:
        self._page = page
        self._attach_widget()

    def _attach_widget(self) -> None:
        self._page.context.add_init_script(WIDGET_INIT_SCRIPT)
        self._page.evaluate(WIDGET_INIT_SCRIPT)

    def _color_for_level(self, level_id: int) -> str:
        return DANGER_LEVEL_COLORS.get(level_id, DEFAULT_COLOR)

    def danger_level_notify(
        self,
        danger_level: DangerLevel,
        reason: DangerReason,
    ) -> None:
        self._page.evaluate(
            UPDATE_WIDGET_SCRIPT,
            {
                "label": danger_level.name,
                "color": self._color_for_level(danger_level.id),
                "description": (
                    f"{danger_level.description}. {reason.description}"
                ),
            },
        )

    def warning_notify(self, warning: str) -> None:
        self._page.evaluate(
            UPDATE_WIDGET_SCRIPT,
            {
                "label": "Внимание",
                "color": WARNING_COLOR,
                "description": warning,
            },
        )
