(payload) => {
    if (typeof window.__chromeAgentUpdateStatusWidget === 'function') {
        window.__chromeAgentUpdateStatusWidget(payload);
    }
}