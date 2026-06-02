import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  getCurrentUser,
  loginRequest,
  logoutRequest,
  persistTokens,
  registerRequest,
} from "../api/client.js";
import { clearAllTokens, getAccessToken } from "./tokenStorage.js";
import { getDeviceName } from "../constants.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadUser = useCallback(async () => {
    const token = getAccessToken();
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    const body = await getCurrentUser();
    if (body.success && body.data) {
      setUser(body.data);
    } else {
      clearAllTokens();
      setUser(null);
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(async ({ username, password }) => {
    const body = await loginRequest({
      username,
      password,
      device_name: getDeviceName(),
    });

    if (!body.success || !body.data?.access_token) {
      throw new Error(body.message || "Ошибка входа");
    }

    persistTokens(body.data);
    await loadUser();
    return body;
  }, [loadUser]);

  const register = useCallback(async ({ username, password, email }) => {
    const payload = {
      username,
      password,
      device_name: getDeviceName(),
    };
    if (email) {
      payload.email = email;
    }

    const body = await registerRequest(payload);
    if (!body.success || !body.data?.access_token) {
      throw new Error(body.message || "Ошибка регистрации");
    }

    persistTokens(body.data);
    await loadUser();
    return body;
  }, [loadUser]);

  const logout = useCallback(async () => {
    try {
      await logoutRequest();
    } finally {
      clearAllTokens();
      setUser(null);
    }
  }, []);

  const value = useMemo(
    () => ({
      user,
      isLoading,
      isAuthenticated: Boolean(user),
      login,
      register,
      logout,
    }),
    [user, isLoading, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
