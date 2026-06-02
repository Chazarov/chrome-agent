export default function WeeklyGoals({ goals }) {
  return (
    <div className="goals-list">
      {goals.map((goal) => (
        <div key={goal.id} className="goal-item">
          <div className="goal-head">
            <span>{goal.label}</span>
            <span className="mono">{goal.progress}%</span>
          </div>
          <div className="goal-track">
            <div className="goal-fill" style={{ width: `${goal.progress}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}
