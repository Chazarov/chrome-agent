const STATUS_LABELS = {
  done: "Готово",
  running: "В работе",
  error: "Ошибка",
  idle: "Ожидание",
};

export default function RecentTasksTable({ tasks }) {
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            <th>Сайт</th>
            <th>Действие</th>
            <th>Статус</th>
            <th>Время</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id}>
              <td className="mono">{task.site}</td>
              <td>{task.action}</td>
              <td>
                <span className={`status-badge status-${task.status}`}>
                  {STATUS_LABELS[task.status]}
                </span>
              </td>
              <td className="muted-cell">{task.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
