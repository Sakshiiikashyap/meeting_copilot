import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { listMeetings, createMeeting } from "../services/meetings";
import { MeetingListItem } from "../types/meeting";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [meetings, setMeetings] = useState<MeetingListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);
  const [title, setTitle] = useState("");
  const [transcript, setTranscript] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadMeetings();
  }, []);

  async function loadMeetings() {
    setLoading(true);
    try {
      const data = await listMeetings();
      setMeetings(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate() {
    if (!title.trim() || !transcript.trim()) return;
    setCreating(true);
    try {
      const meeting = await createMeeting(title, transcript);
      navigate(`/meetings/${meeting.id}`);
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-semibold">Welcome, {user?.full_name || user?.email}</h1>
        <button onClick={logout} className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg">
          Log out
        </button>
      </div>

      <button
        onClick={() => setShowUpload(!showUpload)}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg mb-6"
      >
        {showUpload ? "Cancel" : "+ New Meeting"}
      </button>

      {showUpload && (
        <div className="bg-gray-900 p-6 rounded-xl mb-8 space-y-4">
          <input
            type="text"
            placeholder="Meeting title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-gray-800 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Paste transcript here..."
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            rows={8}
            className="w-full bg-gray-800 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleCreate}
            disabled={creating}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-4 py-2 rounded-lg"
          >
            {creating ? "Creating..." : "Create Meeting"}
          </button>
        </div>
      )}

      <h2 className="text-lg font-medium mb-4">Your Meetings</h2>

      {loading ? (
        <p className="text-gray-400">Loading...</p>
      ) : meetings.length === 0 ? (
        <p className="text-gray-400">No meetings yet — create one above.</p>
      ) : (
        <div className="space-y-3">
          {meetings.map((m) => (
            <div
              key={m.id}
              onClick={() => navigate(`/meetings/${m.id}`)}
              className="bg-gray-900 hover:bg-gray-800 p-4 rounded-lg cursor-pointer flex justify-between items-center"
            >
              <div>
                <p className="font-medium">{m.title}</p>
                <p className="text-sm text-gray-400">
                  {new Date(m.created_at).toLocaleDateString()}
                </p>
              </div>
              <span className="text-xs bg-gray-800 px-2 py-1 rounded-full text-gray-300">
                {m.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}