import { API_BASE } from "../constants.js";
import { getAccessToken, setAccessToken, setRefreshTokenCookie } from "../auth/tokenStorage.js";

let refreshPromise = null;

async function parseResponse(response) {
  const text = await response.text();
  if (!text) {
    return { success: false, message: response.statusText, data: null };
  }
  try {
    return JSON.parse(text);
  } catch {
    return { success: false, message: text, data: null };
  }
}

async function refreshAccessToken() {
  const accessToken = getAccessToken();
  const response = await fetch(`${API_BASE}/user/refresh`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
  });

  const body = await parseResponse(response);
  if (!response.ok || !body.success || !body.data?.access_token) {
    throw new Error(body.message || "Не удалось обновить токен");
  }

  setAccessToken(body.data.access_token);
  if (body.data.refresh_token) {
    setRefreshTokenCookie(body.data.refresh_token);
  }
  return body.data.access_token;
}

async function ensureRefreshed() {
  if (!refreshPromise) {
    refreshPromise = refreshAccessToken().finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

export async function apiFetch(path, options = {}, retry = true) {
  const accessToken = getAccessToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (accessToken && !headers.Authorization) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    credentials: "include",
    headers,
  });

  if (response.status === 401 && retry && !path.includes("/user/refresh") && !path.includes("/auth/")) {
    try {
      await ensureRefreshed();
      return apiFetch(path, options, false);
    } catch {
      return parseResponse(response);
    }
  }

  return parseResponse(response);
}

export async function loginRequest(credentials) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  return parseResponse(response);
}

export async function registerRequest(payload) {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse(response);
}

export async function logoutRequest() {
  return apiFetch("/user/logout", { method: "POST" }, false);
}

export async function getCurrentUser() {
  return apiFetch("/user/me", { method: "GET" });
}

export function persistTokens(data) {
  if (data?.access_token) {
    setAccessToken(data.access_token);
  }
  if (data?.refresh_token) {
    setRefreshTokenCookie(data.refresh_token);
  }
}
