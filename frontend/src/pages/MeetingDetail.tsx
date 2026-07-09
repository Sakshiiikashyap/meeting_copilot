import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  getMeeting,
  generateExecutiveSummary,
  generateDetailedSummary,
  generateActionItems,
  generateDecisions,
  generateKeyPoints,
  generateRisks,
  generateOpenQuestions,
  generateFollowUpEmail,
  generateNextAgenda,
  generateTitle,
  generateTags,
  generateSentiment,
} from "../services/meetings";
import type { Meeting, ActionItem, Decision } from "../types/meeting";
import {
  ArrowLeft, CheckCircle2, Circle, Loader2, AlertTriangle,
  ListChecks, FileText, HelpCircle, Mail, Calendar, Tag, Smile,
} from "lucide-react";

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
      setMeeting(await getMeeting(parseInt(id)));
    } finally {
      setLoading(false);
    }
  }

  async function runGeneration(key: string, fn: (id: number) => Promise<Meeting>) {
    if (!meeting) return;
    setGenerating(key);
    try {
      setMeeting(await fn(meeting.id));
    } finally {
      setGenerating(null);
    }
  }

  if (loading || !meeting) {
    return (
      <div className="min-h-screen bg-canvas-light dark:bg-canvas-dark flex items-center justify-center">
        <Loader2 className="animate-spin text-accent" size={22} />
      </div>
    );
  }

  const actionItems: ActionItem[] = meeting.action_items ? JSON.parse(meeting.action_items) : [];
  const decisions: Decision[] = meeting.decisions ? JSON.parse(meeting.decisions) : [];
  const keyPoints: string[] = meeting.key_discussion_points ? JSON.parse(meeting.key_discussion_points) : [];
  const risks: string[] = meeting.risks ? JSON.parse(meeting.risks) : [];
  const openQuestions: string[] = meeting.open_questions ? JSON.parse(meeting.open_questions) : [];
  const followUpEmail = meeting.follow_up_email ? JSON.parse(meeting.follow_up_email) : null;
  const nextAgenda: string[] = meeting.next_meeting_agenda ? JSON.parse(meeting.next_meeting_agenda) : [];
  const tags: string[] = meeting.tags ? JSON.parse(meeting.tags) : [];

  const progressItems = [
    { label: "Executive summary", done: !!meeting.executive_summary },
    { label: "Detailed summary", done: !!meeting.detailed_summary },
    { label: "Key discussion points", done: !!meeting.key_discussion_points },
    { label: "Action items", done: !!meeting.action_items },
    { label: "Decisions", done: !!meeting.decisions },
    { label: "Risks", done: !!meeting.risks },
    { label: "Open questions", done: !!meeting.open_questions },
    { label: "Follow-up email", done: !!meeting.follow_up_email },
    { label: "Next agenda", done: !!meeting.next_meeting_agenda },
    { label: "AI title", done: !!meeting.ai_title },
    { label: "Tags & category", done: !!meeting.tags },
    { label: "Sentiment", done: !!meeting.sentiment },
  ];
  const doneCount = progressItems.filter((p) => p.done).length;

  return (
    <div className="min-h-screen bg-canvas-light dark:bg-canvas-dark text-ink-light dark:text-ink-dark transition-colors">
      <div className="max-w-5xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-[1fr_240px] gap-10">

        <div>
          <button
            onClick={() => navigate("/dashboard")}
            className="flex items-center gap-1.5 text-sm text-ink-light/40 dark:text-ink-dark/40 hover:text-accent transition-colors mb-8"
          >
            <ArrowLeft size={14} />
            Back to dashboard
          </button>

          <p className="text-xs uppercase tracking-wider text-ink-light/40 dark:text-ink-dark/40 mb-2">
            {new Date(meeting.created_at).toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" })}
          </p>
          <h1 className="font-serif text-3xl mb-1">{meeting.title}</h1>
          {meeting.ai_title && (
            <p className="text-sm text-ink-light/40 dark:text-ink-dark/40 italic mb-2">
              AI suggests: "{meeting.ai_title}"
            </p>
          )}
          {(tags.length > 0 || meeting.category) && (
            <div className="flex flex-wrap gap-1.5 mb-4">
              {meeting.category && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-accent/10 text-accent border border-accent/20">
                  {meeting.category}
                </span>
              )}
              {tags.map((t, i) => (
                <span key={i} className="text-xs px-2 py-0.5 rounded-full border border-ink-light/15 dark:border-ink-dark/15 text-ink-light/50 dark:text-ink-dark/50">
                  {t}
                </span>
              ))}
            </div>
          )}
          <div className="mb-10" />

          {/* TRANSCRIPT */}
          <Section icon={<FileText size={14} />} label="Transcript">
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink-light/75 dark:text-ink-dark/75 max-h-64 overflow-y-auto">
              {meeting.raw_transcript}
            </p>
          </Section>

          {/* EXECUTIVE SUMMARY */}
          <Section
            icon={<ListChecks size={14} />}
            label="Executive summary"
            action={<GenerateButton active={generating === "summary"} exists={!!meeting.executive_summary} onClick={() => runGeneration("summary", generateExecutiveSummary)} />}
          >
            {meeting.executive_summary ? (
              <p className="leading-relaxed text-[15px]">{meeting.executive_summary}</p>
            ) : (
              <Empty text="Generate a concise summary of this meeting." />
            )}
          </Section>

          {/* DETAILED SUMMARY */}
          <Section
            icon={<FileText size={14} />}
            label="Detailed summary"
            action={<GenerateButton active={generating === "detailed"} exists={!!meeting.detailed_summary} onClick={() => runGeneration("detailed", generateDetailedSummary)} />}
          >
            {meeting.detailed_summary ? (
              <p className="leading-relaxed text-[15px] whitespace-pre-wrap">{meeting.detailed_summary}</p>
            ) : (
              <Empty text="Generate a thorough, multi-paragraph summary." />
            )}
          </Section>

          {/* KEY DISCUSSION POINTS */}
          <Section
            icon={<ListChecks size={14} />}
            label="Key discussion points"
            action={<GenerateButton active={generating === "keypoints"} exists={!!meeting.key_discussion_points} onClick={() => runGeneration("keypoints", generateKeyPoints)} />}
          >
            {keyPoints.length > 0 ? (
              <ul className="space-y-2.5">
                {keyPoints.map((k, i) => (
                  <li key={i} className="flex gap-2.5 text-[15px]">
                    <Circle size={6} className="text-accent mt-2 flex-shrink-0" fill="currentColor" />
                    <span>{k}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Extract the main topics discussed." />
            )}
          </Section>

          {/* ACTION ITEMS */}
          <Section
            icon={<ListChecks size={14} />}
            label="Action items"
            action={<GenerateButton active={generating === "action_items"} exists={!!meeting.action_items} onClick={() => runGeneration("action_items", generateActionItems)} />}
          >
            {actionItems.length > 0 ? (
              <ul className="space-y-3">
                {actionItems.map((item, i) => (
                  <li key={i} className="flex gap-3 text-[15px]">
                    <Circle size={6} className="text-accent mt-2 flex-shrink-0" fill="currentColor" />
                    <span>
                      {item.task}
                      {item.owner && <span className="text-ink-light/50 dark:text-ink-dark/50"> — {item.owner}</span>}
                      {item.due_date && <span className="text-ink-light/35 dark:text-ink-dark/35"> · {item.due_date}</span>}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Extract action items with owners and due dates." />
            )}
          </Section>

          {/* DECISIONS */}
          <Section
            icon={<CheckCircle2 size={14} />}
            label="Decisions"
            action={<GenerateButton active={generating === "decisions"} exists={!!meeting.decisions} onClick={() => runGeneration("decisions", generateDecisions)} />}
          >
            {decisions.length > 0 ? (
              <ul className="space-y-3">
                {decisions.map((d, i) => (
                  <li key={i} className="flex gap-3 text-[15px]">
                    <CheckCircle2 size={15} className="text-accent mt-0.5 flex-shrink-0" />
                    <span>
                      {d.decision}
                      {d.context && <span className="block text-sm text-ink-light/40 dark:text-ink-dark/40 mt-0.5">{d.context}</span>}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Extract decisions that were explicitly confirmed." />
            )}
          </Section>

          {/* RISKS */}
          <Section
            icon={<AlertTriangle size={14} />}
            label="Risks"
            action={<GenerateButton active={generating === "risks"} exists={!!meeting.risks} onClick={() => runGeneration("risks", generateRisks)} />}
          >
            {risks.length > 0 ? (
              <ul className="space-y-2.5">
                {risks.map((r, i) => (
                  <li key={i} className="flex gap-2.5 text-[15px]">
                    <AlertTriangle size={14} className="text-accent mt-0.5 flex-shrink-0" />
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Surface genuine risks and blockers." />
            )}
          </Section>

          {/* OPEN QUESTIONS */}
          <Section
            icon={<HelpCircle size={14} />}
            label="Open questions"
            action={<GenerateButton active={generating === "open_questions"} exists={!!meeting.open_questions} onClick={() => runGeneration("open_questions", generateOpenQuestions)} />}
          >
            {openQuestions.length > 0 ? (
              <ul className="space-y-2.5">
                {openQuestions.map((q, i) => (
                  <li key={i} className="flex gap-2.5 text-[15px]">
                    <HelpCircle size={14} className="text-accent mt-0.5 flex-shrink-0" />
                    <span>{q}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Find questions raised but left unanswered." />
            )}
          </Section>

          {/* FOLLOW-UP EMAIL */}
          <Section
            icon={<Mail size={14} />}
            label="Follow-up email"
            action={<GenerateButton active={generating === "email"} exists={!!meeting.follow_up_email} onClick={() => runGeneration("email", generateFollowUpEmail)} />}
          >
            {followUpEmail ? (
              <div className="bg-ink-light/[0.02] dark:bg-ink-dark/[0.03] border border-ink-light/10 dark:border-ink-dark/10 rounded-lg p-4">
                <p className="text-sm font-medium mb-2">{followUpEmail.subject}</p>
                <p className="text-sm text-ink-light/70 dark:text-ink-dark/70 whitespace-pre-wrap leading-relaxed">{followUpEmail.body}</p>
              </div>
            ) : (
              <Empty text="Draft a ready-to-send follow-up email." />
            )}
          </Section>

          {/* NEXT MEETING AGENDA */}
          <Section
            icon={<Calendar size={14} />}
            label="Next meeting agenda"
            action={<GenerateButton active={generating === "agenda"} exists={!!meeting.next_meeting_agenda} onClick={() => runGeneration("agenda", generateNextAgenda)} />}
          >
            {nextAgenda.length > 0 ? (
              <ul className="space-y-2.5">
                {nextAgenda.map((a, i) => (
                  <li key={i} className="flex gap-2.5 text-[15px]">
                    <Circle size={6} className="text-accent mt-2 flex-shrink-0" fill="currentColor" />
                    <span>{a}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Empty text="Propose an agenda based on unresolved items." />
            )}
          </Section>

          {/* AI TITLE */}
          <Section
            icon={<Tag size={14} />}
            label="AI-generated title"
            action={<GenerateButton active={generating === "title"} exists={!!meeting.ai_title} onClick={() => runGeneration("title", generateTitle)} />}
          >
            {meeting.ai_title ? (
              <p className="text-[15px]">{meeting.ai_title}</p>
            ) : (
              <Empty text="Generate a concise, descriptive title." />
            )}
          </Section>

          {/* TAGS & CATEGORY */}
          <Section
            icon={<Tag size={14} />}
            label="Tags & category"
            action={<GenerateButton active={generating === "tags"} exists={!!meeting.tags} onClick={() => runGeneration("tags", generateTags)} />}
          >
            {tags.length > 0 || meeting.category ? (
              <div className="flex flex-wrap gap-1.5">
                {meeting.category && (
                  <span className="text-xs px-2.5 py-1 rounded-full bg-accent/10 text-accent border border-accent/20">
                    {meeting.category}
                  </span>
                )}
                {tags.map((t, i) => (
                  <span key={i} className="text-xs px-2.5 py-1 rounded-full border border-ink-light/15 dark:border-ink-dark/15 text-ink-light/50 dark:text-ink-dark/50">
                    {t}
                  </span>
                ))}
              </div>
            ) : (
              <Empty text="Classify this meeting with tags and a category." />
            )}
          </Section>

          {/* SENTIMENT */}
          <Section
            icon={<Smile size={14} />}
            label="Sentiment"
            action={<GenerateButton active={generating === "sentiment"} exists={!!meeting.sentiment} onClick={() => runGeneration("sentiment", generateSentiment)} />}
          >
            {meeting.sentiment ? (
              <div className="flex items-start gap-3">
                <span
                  className={`text-xs px-2.5 py-1 rounded-full border capitalize flex-shrink-0 ${
                    meeting.sentiment === "positive"
                      ? "border-accent/30 text-accent bg-accent/5"
                      : meeting.sentiment === "negative"
                      ? "border-ink-light/30 dark:border-ink-dark/30 text-ink-light/70 dark:text-ink-dark/70"
                      : "border-ink-light/15 dark:border-ink-dark/15 text-ink-light/40 dark:text-ink-dark/40"
                  }`}
                >
                  {meeting.sentiment}
                </span>
                <p className="text-sm text-ink-light/60 dark:text-ink-dark/60">{meeting.sentiment_reason}</p>
              </div>
            ) : (
              <Empty text="Analyze the overall tone of the meeting." />
            )}
          </Section>
        </div>

        {/* Sidebar progress */}
        <aside className="lg:sticky lg:top-10 h-fit">
          <div className="border border-ink-light/10 dark:border-ink-dark/10 rounded-xl p-5">
            <div className="flex items-baseline justify-between mb-4">
              <p className="text-xs uppercase tracking-wider text-ink-light/40 dark:text-ink-dark/40">
                Progress
              </p>
              <p className="font-serif text-lg text-accent">{doneCount}/{progressItems.length}</p>
            </div>
            <div className="space-y-2.5">
              {progressItems.map((p) => (
                <div key={p.label} className="flex items-center gap-2 text-sm">
                  {p.done ? (
                    <CheckCircle2 size={15} className="text-accent flex-shrink-0" />
                  ) : (
                    <Circle size={15} className="text-ink-light/20 dark:text-ink-dark/20 flex-shrink-0" />
                  )}
                  <span className={p.done ? "" : "text-ink-light/40 dark:text-ink-dark/40"}>{p.label}</span>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

function Section({
  icon,
  label,
  action,
  children,
}: {
  icon?: React.ReactNode;
  label: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="border-t border-ink-light/10 dark:border-ink-dark/10 py-7">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-2 text-ink-light/50 dark:text-ink-dark/50">
          {icon}
          <h3 className="text-xs uppercase tracking-wider">{label}</h3>
        </div>
        {action}
      </div>
      {children}
    </div>
  );
}

function GenerateButton({ active, exists, onClick }: { active: boolean; exists: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      disabled={active}
      className="flex items-center gap-1.5 text-xs text-accent hover:text-accent-light disabled:opacity-40 transition-colors"
    >
      {active && <Loader2 size={12} className="animate-spin" />}
      {active ? "Generating…" : exists ? "Regenerate" : "Generate"}
    </button>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="text-sm text-ink-light/30 dark:text-ink-dark/30 italic">{text}</p>;
}