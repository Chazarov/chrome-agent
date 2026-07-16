(() => {{
    if (window.__chromeAgentWidgetInstalled) return;
    window.__chromeAgentWidgetInstalled = true;

    window.__chromeAgentMascotImages = {mascot_images_json};

    const ensureWidget = () => {{
        let widget = document.getElementById('chrome-agent-status-widget');
        if (widget) return widget;

        const style = document.createElement('style');
        style.textContent = `
            #chrome-agent-status-widget {{
                position: fixed;
                top: 12px;
                right: 12px;
                z-index: 2147483647;
                width: 100px;
                height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 4px;
                border-radius: 8px;
                box-sizing: border-box;
                background-color: transpanent;
                pointer-events: none;
                user-select: none;
            }}
            #chrome-agent-status-widget img {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                display: block;
            }}
        `;
        (document.head || document.documentElement).appendChild(style);

        widget = document.createElement('div');
        widget.id = 'chrome-agent-status-widget';
        widget.setAttribute('role', 'status');
        widget.setAttribute('aria-live', 'polite');

        const img = document.createElement('img');
        img.alt = '';
        img.src = window.__chromeAgentMascotImages[1] || '';
        widget.appendChild(img);

        (document.body || document.documentElement).appendChild(widget);
        return widget;
    }};

    window.__chromeAgentUpdateStatusWidget = (payload) => {{
        const widget = ensureWidget();
        const img = widget.querySelector('img');
        const imageUrl =
            payload.imageUrl ||
            window.__chromeAgentMascotImages[payload.imageKey];

        if (img && imageUrl) {{
            img.src = imageUrl;
        }}

        if (payload.description) {{
            widget.setAttribute('aria-label', payload.description);
            widget.title = payload.description;
        }}
    }};

    const boot = () => ensureWidget();
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', boot);
    }} else {{
        boot();
    }}
}})();