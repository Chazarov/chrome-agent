function Sparkline({ data }) {
  const max = Math.max(...data, 1);
  const width = 80;
  const height = 28;
  const step = width / (data.length - 1);

  const points = data
    .map((value, index) => {
      const x = index * step;
      const y = height - (value / max) * (height - 4) - 2;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="sparkline" aria-hidden="true">
      <polyline fill="none" stroke="#3dd6c3" strokeWidth="1.5" points={points} />
    </svg>
  );
}

export default function SparklineMetrics({ metrics }) {
  return (
    <div className="sparkline-grid">
      {metrics.map((metric) => (
        <article key={metric.id} className="sparkline-card">
          <p className="sparkline-label">{metric.label}</p>
          <p className="sparkline-value">{metric.value}</p>
          <Sparkline data={metric.data} />
        </article>
      ))}
    </div>
  );
}
