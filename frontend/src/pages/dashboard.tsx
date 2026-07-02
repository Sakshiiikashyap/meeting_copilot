import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Welcome, {user?.full_name || user?.email}</h1>
        <button onClick={logout} className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg">
          Log out
        </button>
      </div>
      <p className="text-gray-400 mt-4">This will become your meeting dashboard in Week 2.</p>
    </div>
  );
}