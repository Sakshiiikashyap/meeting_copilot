import { useState, FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const { register, loading } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await register(email, password, fullName);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  }

  return (
    <div className="min-h-screen bg-canvas-light dark:bg-canvas-dark text-ink-light dark:text-ink-dark transition-colors flex items-center justify-center px-6">
      <button
        onClick={toggleTheme}
        className="fixed top-6 right-6 text-sm border border-ink-light/15 dark:border-ink-dark/15 rounded-full px-3 py-1.5 hover:border-ink-light/40 dark:hover:border-ink-dark/40 transition-colors"
      >
        {theme === "light" ? "Dark" : "Light"}
      </button>

      <form onSubmit={handleSubmit} className="w-full max-w-sm">
        <h1 className="font-serif text-3xl mb-1">Create your account</h1>
        <p className="text-sm text-ink-light/50 dark:text-ink-dark/50 mb-8">
          Get started with your meeting copilot
        </p>

        {error && (
          <div className="text-sm text-accent border border-accent/20 rounded-md px-3 py-2 mb-5">
            {error}
          </div>
        )}

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-xs uppercase tracking-wider text-ink-light/40 dark:text-ink-dark/40 mb-1.5">
              Full name
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full bg-transparent border-b border-ink-light/15 dark:border-ink-dark/15 pb-2 outline-none focus:border-accent transition-colors"
            />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-wider text-ink-light/40 dark:text-ink-dark/40 mb-1.5">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full bg-transparent border-b border-ink-light/15 dark:border-ink-dark/15 pb-2 outline-none focus:border-accent transition-colors"
            />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-wider text-ink-light/40 dark:text-ink-dark/40 mb-1.5">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full bg-transparent border-b border-ink-light/15 dark:border-ink-dark/15 pb-2 outline-none focus:border-accent transition-colors"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent hover:bg-accent-light disabled:opacity-40 text-white text-sm font-medium py-2.5 rounded-md transition-colors"
        >
          {loading ? "Creating account…" : "Register"}
        </button>

        <p className="text-sm text-ink-light/50 dark:text-ink-dark/50 text-center mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-accent hover:text-accent-light transition-colors">
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
}