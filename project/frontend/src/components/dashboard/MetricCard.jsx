export default function MetricCard({ label, value, delta, trend }) {
  const trendClass = trend === "up" ? "metric-delta-up" : "metric-delta-down";
  return (
    <article className="metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value}</p>
      <p className={`metric-delta mono ${trendClass}`}>{delta}</p>
    </article>
  );
}
