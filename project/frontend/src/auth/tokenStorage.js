import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_COOKIE } from "../constants.js";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function setRefreshTokenCookie(token, maxAgeSeconds = 5184000) {
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie = `${REFRESH_TOKEN_COOKIE}=${encodeURIComponent(token)}; path=/; max-age=${maxAgeSeconds}; SameSite=Lax${secure}`;
}

export function clearRefreshTokenCookie() {
  document.cookie = `${REFRESH_TOKEN_COOKIE}=; path=/; max-age=0; SameSite=Lax`;
}

export function clearAllTokens() {
  clearAccessToken();
  clearRefreshTokenCookie();
}
