export const ACCESS_TOKEN_KEY = "sobagent_access_token";
export const REFRESH_TOKEN_COOKIE = "refresh_token";

export const API_BASE = import.meta.env.VITE_API_URL || "/api";

export function getDeviceName() {
  const ua = navigator.userAgent.replace(/\s+/g, " ").slice(0, 48);
  return `Web · ${ua}`;
}

export const KPI_METRICS = [
  { id: "sessions", label: "Активных сессий", value: "1 247", delta: "+12.4%", trend: "up" },
  { id: "tasks", label: "Задач выполнено", value: "8 432", delta: "+8.1%", trend: "up" },
  { id: "success", label: "Success rate", value: "94.7%", delta: "+1.2%", trend: "up" },
  { id: "latency", label: "Среднее время", value: "1.2s", delta: "-0.3s", trend: "down" },
];

export const WEEKLY_ACTIVITY = [
  { day: "Пн", value: 62 },
  { day: "Вт", value: 78 },
  { day: "Ср", value: 55 },
  { day: "Чт", value: 91 },
  { day: "Пт", value: 84 },
  { day: "Сб", value: 43 },
  { day: "Вс", value: 38 },
];

export const RECENT_TASKS = [
  { id: 1, site: "shop.example.com", action: "Оформление заказа", status: "done", time: "2 мин назад" },
  { id: 2, site: "crm.internal.io", action: "Экспорт отчёта", status: "done", time: "8 мин назад" },
  { id: 3, site: "mail.provider.ru", action: "Фильтрация входящих", status: "running", time: "12 мин назад" },
  { id: 4, site: "analytics.cloud", action: "Сбор метрик", status: "done", time: "24 мин назад" },
  { id: 5, site: "docs.notion.so", action: "Обновление wiki", status: "error", time: "31 мин назад" },
  { id: 6, site: "github.com", action: "Review PR #142", status: "done", time: "45 мин назад" },
  { id: 7, site: "jira.company.com", action: "Создание тикета", status: "idle", time: "1 ч назад" },
  { id: 8, site: "stripe.com", action: "Сверка платежей", status: "done", time: "1.5 ч назад" },
];

export const AGENT_STATUS = [
  { id: "alpha", name: "Agent Alpha", status: "online", load: 34 },
  { id: "beta", name: "Agent Beta", status: "online", load: 67 },
  { id: "gamma", name: "Agent Gamma", status: "idle", load: 8 },
  { id: "delta", name: "Agent Delta", status: "online", load: 52 },
  { id: "epsilon", name: "Agent Epsilon", status: "error", load: 0 },
  { id: "zeta", name: "Agent Zeta", status: "online", load: 41 },
];

export const SPARKLINE_METRICS = [
  { id: "cpu", label: "CPU proxy", value: "23%", data: [20, 22, 19, 25, 23, 21, 23] },
  { id: "queue", label: "Очередь задач", value: "14", data: [8, 12, 10, 15, 18, 14, 14] },
  { id: "errors", label: "Ошибки за 24ч", value: "3", data: [5, 4, 6, 3, 2, 4, 3] },
];

export const WEEKLY_GOALS = [
  { id: "automation", label: "Автоматизация", progress: 87 },
  { id: "coverage", label: "Покрытие сценариев", progress: 72 },
  { id: "uptime", label: "Uptime агентов", progress: 99 },
];
