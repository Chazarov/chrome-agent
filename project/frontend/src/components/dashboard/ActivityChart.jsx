export default function ActivityChart({ data }) {
  const max = Math.max(...data.map((d) => d.value), 1);
  const width = 320;
  const height = 120;
  const barWidth = width / data.length - 8;

  const points = data
    .map((item, index) => {
      const x = index * (width / data.length) + barWidth / 2 + 4;
      const y = height - (item.value / max) * (height - 20) - 10;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="chart-panel">
      <svg viewBox={`0 0 ${width} ${height}`} className="activity-chart" role="img" aria-label="График активности за 7 дней">
        <defs>
          <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="rgba(61, 214, 195, 0.45)" />
            <stop offset="100%" stopColor="rgba(61, 214, 195, 0)" />
          </linearGradient>
        </defs>
        <polyline
          fill="url(#areaGrad)"
          stroke="none"
          points={`0,${height} ${points} ${width},${height}`}
        />
        <polyline
          fill="none"
          stroke="#3dd6c3"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={points}
        />
        {data.map((item, index) => {
          const x = index * (width / data.length) + 4;
          const barH = (item.value / max) * (height - 30);
          return (
            <g key={item.day}>
              <rect
                x={x}
                y={height - barH - 18}
                width={barWidth}
                height={barH}
                rx="4"
                fill="rgba(61, 214, 195, 0.12)"
              />
              <text x={x + barWidth / 2} y={height - 2} textAnchor="middle" className="chart-label">
                {item.day}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
