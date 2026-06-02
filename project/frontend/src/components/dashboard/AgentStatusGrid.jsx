const STATUS_LABELS = {
  online: "Online",
  idle: "Idle",
  error: "Error",
};

export default function AgentStatusGrid({ agents }) {
  return (
    <div className="agent-grid">
      {agents.map((agent) => (
        <article key={agent.id} className={`agent-card agent-${agent.status}`}>
          <div className="agent-card-head">
            <span className={`agent-dot agent-dot-${agent.status}`} aria-hidden="true" />
            <h4>{agent.name}</h4>
          </div>
          <p className="agent-status mono">{STATUS_LABELS[agent.status]}</p>
          <div className="agent-load">
            <div className="agent-load-bar" style={{ width: `${agent.load}%` }} />
          </div>
          <p className="agent-load-label">Load {agent.load}%</p>
        </article>
      ))}
    </div>
  );
}
