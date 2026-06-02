import AppHeader from "../components/AppHeader.jsx";
import ActivityChart from "../components/dashboard/ActivityChart.jsx";
import AgentStatusGrid from "../components/dashboard/AgentStatusGrid.jsx";
import MetricCard from "../components/dashboard/MetricCard.jsx";
import RecentTasksTable from "../components/dashboard/RecentTasksTable.jsx";
import SparklineMetrics from "../components/dashboard/SparklineMetrics.jsx";
import WeeklyGoals from "../components/dashboard/WeeklyGoals.jsx";
import {
  AGENT_STATUS,
  KPI_METRICS,
  RECENT_TASKS,
  SPARKLINE_METRICS,
  WEEKLY_ACTIVITY,
  WEEKLY_GOALS,
} from "../constants.js";
import { useAuth } from "../auth/AuthContext.jsx";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="dashboard-app">
      <AppHeader showLogout />
      <main className="dashboard-main">
        <div className="wrap">
          <section className="dashboard-hero">
            <div>
              <span className="hero-badge mono">Dashboard · live</span>
              <h1>Привет, {user?.username ?? "агент"}</h1>
              <p className="dashboard-lead">
                Обзор активности агентов, задач и ключевых метрик за последние 7 дней.
              </p>
            </div>
            <div className="dashboard-hero-stat">
              <p className="mono">Uptime</p>
              <p className="hero-stat-value">99.97%</p>
            </div>
          </section>

          <section className="metrics-grid">
            {KPI_METRICS.map((metric) => (
              <MetricCard key={metric.id} {...metric} />
            ))}
          </section>

          <section className="dashboard-grid">
            <article className="panel panel-wide">
              <div className="panel-head">
                <h2>Активность за 7 дней</h2>
                <span className="panel-meta mono">+18% к прошлой неделе</span>
              </div>
              <ActivityChart data={WEEKLY_ACTIVITY} />
            </article>

            <article className="panel">
              <div className="panel-head">
                <h2>Цели недели</h2>
              </div>
              <WeeklyGoals goals={WEEKLY_GOALS} />
            </article>

            <article className="panel">
              <div className="panel-head">
                <h2>Микрометрики</h2>
              </div>
              <SparklineMetrics metrics={SPARKLINE_METRICS} />
            </article>

            <article className="panel panel-wide">
              <div className="panel-head">
                <h2>Последние задачи</h2>
                <span className="panel-meta">8 записей</span>
              </div>
              <RecentTasksTable tasks={RECENT_TASKS} />
            </article>

            <article className="panel panel-wide">
              <div className="panel-head">
                <h2>Статус агентов</h2>
                <span className="panel-meta">
                  {AGENT_STATUS.filter((a) => a.status === "online").length} online
                </span>
              </div>
              <AgentStatusGrid agents={AGENT_STATUS} />
            </article>
          </section>
        </div>
      </main>
    </div>
  );
}
