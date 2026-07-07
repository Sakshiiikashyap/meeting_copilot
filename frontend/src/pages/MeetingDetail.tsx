import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getMeeting, generateExecutiveSummary, generateActionItems, generateRisks } from "../services/meetings";
import { Meeting, ActionItem } from "../types/meeting";

export default function MeetingDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [meeting, setMeeting] = useState<Meeting | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState<string | null>(null);

  useEffect(() => {
    load();
  }, [id]);

  async function load() {
    if (!id) return;
    setLoading(true);
    try {
      const data = await getMeeting(parseInt(id));
      setMeeting(data);
    } finally {
      setLoading(false);
    }
  }

  async function runGeneration(key: string, fn: (id: number) => Promise<Meeting>) {
    if (!meeting) return;
    setGenerating(key);
    try {
      const updated = await fn(meeting.id);
      setMeeting(updated);
    } finally {
      setGenerating(null);
    }
  }

  if (loading) return <div className="min-h-screen bg-gray-950 text-white p-8">Loading...</div>;
  if (!meeting) return <div className="min-h-screen bg-gray-950 text-white p-8">Meeting not found.</div>;

  const actionItems: ActionItem[] = meeting.action_items ? JSON.parse(meeting.action_items) : [];

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 max-w-4xl mx-auto">
      <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white mb-6">
        ← Back to Dashboard
      </button>

      <h1 className="text-3xl font-semibold mb-2">{meeting.title}</h1>
      <p className="text-gray-400 mb-8">{new Date(meeting.created_at).toLocaleString()}</p>

      <div className="bg-gray-900 p-6 rounded-xl mb-6">
        <h3 className="text-sm text-gray-400 mb-2">TRANSCRIPT</h3>
        <p className="text-gray-200 whitespace-pre-wrap">{meeting.raw_transcript}</p>
      </div>

      <div className="bg-gray-900 p-6 rounded-xl mb-6">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-sm text-gray-400">EXECUTIVE SUMMARY</h3>
          <button
            onClick={() => runGeneration("summary", generateExecutiveSummary)}
            disabled={generating === "summary"}
            className="text-xs bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-3 py-1 rounded-full"
          >
            {generating === "summary" ? "Generating..." : meeting.executive_summary ? "Regenerate" : "Generate"}
          </button>
        </div>
        <p className="text-gray-200">{meeting.executive_summary || "Not generated yet."}</p>
      </div>

      <div className="bg-gray-900 p-6 rounded-xl mb-6">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-sm text-gray-400">ACTION ITEMS</h3>
          <button
            onClick={() => runGeneration("action_items", generateActionItems)}
            disabled={generating === "action_items"}
            className="text-xs bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-3 py-1 rounded-full"
          >
            {generating === "action_items" ? "Generating..." : meeting.action_items ? "Regenerate" : "Generate"}
          </button>
        </div>
        {actionItems.length > 0 ? (
          <ul className="space-y-2">
            {actionItems.map((item, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">•</span>
                <span>
                  {item.task}
                  {item.owner && <span className="text-gray-400"> — {item.owner}</span>}
                  {item.due_date && <span className="text-gray-500 text-sm"> ({item.due_date})</span>}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400">Not generated yet.</p>
        )}
      </div>

      <div className="bg-gray-900 p-6 rounded-xl mb-6">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-sm text-gray-400">RISKS</h3>
          <button
            onClick={() => runGeneration("risks", generateRisks)}
            disabled={generating === "risks"}
            className="text-xs bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-3 py-1 rounded-full"
          >
            {generating === "risks" ? "Generating..." : meeting.risks ? "Regenerate" : "Generate"}
          </button>
        </div>
        {meeting.risks && JSON.parse(meeting.risks).length > 0 ? (
          <ul className="space-y-1">
            {JSON.parse(meeting.risks).map((risk: string, i: number) => (
              <li key={i} className="text-gray-200">⚠ {risk}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400">Not generated yet.</p>
        )}
      </div>
    </div>
  );
}