import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { listMeetings, createMeeting } from "../services/meetings";
import type { MeetingListItem } from "../types/meeting";
import {
  Moon,
  Sun,
  LogOut,
  Plus,
  FileText,
  Clock,
  ArrowRight,
} from "lucide-react";
import { uploadMeeting } from "../services/meetings";
import toast from "react-hot-toast";
import { deleteMeeting } from "../services/meetings";
import { Trash2 } from "lucide-react";
import { searchMeetings } from "../services/meetings"; // you'll add this function

export default function Dashboard() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [meetings, setMeetings] = useState<MeetingListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);
  const [title, setTitle] = useState("");
  const [transcript, setTranscript] = useState("");
  const [creating, setCreating] = useState(false);
  const [uploadMode, setUploadMode] = useState<"paste" | "file">("paste");
  const [file, setFile] = useState<File | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    loadMeetings();
  }, []);
  useEffect(() => {
    const timeout = setTimeout(async () => {
      if (searchQuery.trim()) {
        setMeetings(await searchMeetings(searchQuery));
      } else {
        loadMeetings();
      }
    }, 300);
    return () => clearTimeout(timeout);
  }, [searchQuery]);

  async function loadMeetings() {
    setLoading(true);
    try {
      setMeetings(await listMeetings());
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate() {
    if (!title.trim()) return;
    if (uploadMode === "paste" && !transcript.trim()) return;
    if (uploadMode === "file" && !file) return;

    setCreating(true);
    try {
      const meeting =
        uploadMode === "paste"
          ? await createMeeting(title, transcript)
          : await uploadMeeting(title, file!);
      navigate(`/meetings/${meeting.id}`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Failed to create meeting");
    } finally {
      setCreating(false);
    }
  }

  const completedCount = meetings.filter(
    (m) => m.status === "completed",
  ).length;

  return (
    <div className="min-h-screen bg-canvas-light dark:bg-canvas-dark text-ink-light dark:text-ink-dark transition-colors">
      {/* subtle top texture line */}
      <div className="h-1 bg-gradient-to-r from-accent/0 via-accent to-accent/0" />

      <div className="max-w-4xl mx-auto px-6 py-10">
        <header className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center font-serif text-accent text-lg">
              {(user?.full_name || user?.email || "?")[0].toUpperCase()}
            </div>
            <div>
              <p className="text-xs text-ink-light/40 dark:text-ink-dark/40 uppercase tracking-wider">
                Meeting Copilot
              </p>
              <h1 className="font-serif text-xl leading-tight">
                {user?.full_name || user?.email}
              </h1>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="w-9 h-9 flex items-center justify-center rounded-full border border-ink-light/15 dark:border-ink-dark/15 hover:border-accent/40 hover:text-accent transition-colors"
            >
              {theme === "light" ? <Moon size={15} /> : <Sun size={15} />}
            </button>
            <button
              onClick={logout}
              aria-label="Sign out"
              className="w-9 h-9 flex items-center justify-center rounded-full border border-ink-light/15 dark:border-ink-dark/15 hover:border-accent/40 hover:text-accent transition-colors"
            >
              <LogOut size={15} />
            </button>
          </div>
        </header>

        {/* Stats strip */}
        <div className="grid grid-cols-3 gap-px bg-ink-light/10 dark:bg-ink-dark/10 rounded-lg overflow-hidden mb-10 border border-ink-light/10 dark:border-ink-dark/10">
          <Stat label="Total meetings" value={meetings.length} />
          <Stat label="Fully processed" value={completedCount} />
          <Stat label="Pending" value={meetings.length - completedCount} />
        </div>

        <div className="flex items-center justify-between mb-6">
          <h2 className="font-serif text-lg">Your meetings</h2>
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="flex items-center gap-1.5 text-sm font-medium text-accent hover:text-accent-light transition-colors"
          >
            <Plus size={15} strokeWidth={2.5} />
            New meeting
          </button>
        </div>
        <input
          type="text"
          placeholder="Search meetings…"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-transparent border-b border-ink-light/15 dark:border-ink-dark/15 pb-2 mb-6 text-sm outline-none focus:border-accent transition-colors placeholder:text-ink-light/30 dark:placeholder:text-ink-dark/30"
        />

        {showUpload && (
          <div className="bg-ink-light/[0.02] dark:bg-ink-dark/[0.03] border border-ink-light/10 dark:border-ink-dark/10 rounded-xl p-6 mb-10 space-y-4">
            <input
              type="text"
              placeholder="Meeting title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-transparent border-b border-ink-light/15 dark:border-ink-dark/15 pb-2 text-lg font-serif outline-none focus:border-accent transition-colors placeholder:text-ink-light/25 dark:placeholder:text-ink-dark/25"
            />

            <div className="flex gap-2 text-xs">
              <button
                onClick={() => setUploadMode("paste")}
                className={`px-3 py-1.5 rounded-full border transition-colors ${
                  uploadMode === "paste"
                    ? "border-accent text-accent"
                    : "border-ink-light/15 dark:border-ink-dark/15 text-ink-light/40 dark:text-ink-dark/40"
                }`}
              >
                Paste text
              </button>
              <button
                onClick={() => setUploadMode("file")}
                className={`px-3 py-1.5 rounded-full border transition-colors ${
                  uploadMode === "file"
                    ? "border-accent text-accent"
                    : "border-ink-light/15 dark:border-ink-dark/15 text-ink-light/40 dark:text-ink-dark/40"
                }`}
              >
                Upload file
              </button>
            </div>

            {uploadMode === "paste" ? (
              <textarea
                placeholder="Paste transcript here…"
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                rows={7}
                className="w-full bg-canvas-light dark:bg-canvas-dark border border-ink-light/10 dark:border-ink-dark/10 rounded-lg p-3 text-sm outline-none focus:border-accent transition-colors placeholder:text-ink-light/25 dark:placeholder:text-ink-dark/25 resize-none"
              />
            ) : (
              <input
                type="file"
                accept=".txt,.pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="w-full text-sm text-ink-light/60 dark:text-ink-dark/60 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-accent/10 file:text-accent file:text-xs file:cursor-pointer"
              />
            )}

            <button
              onClick={handleCreate}
              disabled={creating}
              className="bg-accent hover:bg-accent-light disabled:opacity-40 text-white text-sm font-medium px-5 py-2.5 rounded-lg transition-colors flex items-center gap-2"
            >
              {creating ? "Creating…" : "Create meeting"}
              {!creating && <ArrowRight size={14} />}
            </button>
          </div>
        )}

        {loading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div
                key={i}
                className="h-16 rounded-lg bg-ink-light/[0.03] dark:bg-ink-dark/[0.03] animate-pulse"
              />
            ))}
          </div>
        ) : meetings.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-ink-light/15 dark:border-ink-dark/15 rounded-xl">
            <FileText
              className="mx-auto mb-3 text-ink-light/25 dark:text-ink-dark/25"
              size={28}
            />
            <p className="text-sm text-ink-light/40 dark:text-ink-dark/40">
              No meetings yet — create your first one above.
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {meetings.map((m) => (
              <div
                key={m.id}
                className="group flex justify-between items-center px-5 py-4 rounded-lg border border-ink-light/8 dark:border-ink-dark/8 hover:border-accent/30 hover:bg-accent/[0.03] transition-all"
              >
                <div
                  onClick={() => navigate(`/meetings/${m.id}`)}
                  className="flex items-center gap-3 cursor-pointer flex-1"
                >
                  <FileText
                    size={16}
                    className="text-ink-light/30 dark:text-ink-dark/30 group-hover:text-accent transition-colors"
                  />
                  <div>
                    <p className="text-[15px] group-hover:text-accent transition-colors">
                      {m.title}
                    </p>
                    <div className="flex items-center gap-1.5 text-xs text-ink-light/40 dark:text-ink-dark/40 mt-0.5">
                      <Clock size={11} />
                      {new Date(m.created_at).toLocaleDateString(undefined, {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      })}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge status={m.status} />
                  <button
                    onClick={async (e) => {
                      e.stopPropagation();
                      if (!confirm(`Delete "${m.title}"?`)) return;
                      await deleteMeeting(m.id);
                      toast.success("Meeting deleted");
                      loadMeetings();
                    }}
                    className="text-ink-light/20 dark:text-ink-dark/20 hover:text-accent transition-colors"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-canvas-light dark:bg-canvas-dark px-5 py-4">
      <p className="font-serif text-2xl">{value}</p>
      <p className="text-xs text-ink-light/40 dark:text-ink-dark/40 mt-0.5">
        {label}
      </p>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const isDone = status === "completed";
  return (
    <span
      className={`text-xs px-2.5 py-1 rounded-full border ${
        isDone
          ? "border-accent/30 text-accent bg-accent/5"
          : "border-ink-light/15 dark:border-ink-dark/15 text-ink-light/40 dark:text-ink-dark/40"
      }`}
    >
      {status}
    </span>
  );
}
