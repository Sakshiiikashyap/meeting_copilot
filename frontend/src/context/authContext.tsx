import { createContext, useContext, useState, ReactNode } from "react";
import api from "../services/api";

interface User {
  id: number;
  email: string;
  full_name: string | null;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("access_token"));
  const [loading, setLoading] = useState(false);

  async function fetchMe() {
    const res = await api.get("/auth/me");
    setUser(res.data);
  }

  async function login(email: string, password: string) {
    setLoading(true);
    try {
      const res = await api.post("/auth/login", { email, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("access_token", accessToken);
      setToken(accessToken);
      await fetchMe();
    } finally {
      setLoading(false);
    }
  }

  async function register(email: string, password: string, fullName?: string) {
    setLoading(true);
    try {
      await api.post("/auth/register", { email, password, full_name: fullName });
      await login(email, password);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}