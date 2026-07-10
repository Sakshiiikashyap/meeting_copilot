import type { Meeting, ActionItem, Decision } from "../types/meeting";
import jsPDF from "jspdf";

export function downloadPDF(meeting: Meeting) {
  const md = meetingToMarkdown(meeting);
  const doc = new jsPDF();
  const lines = doc.splitTextToSize(md.replace(/[#*\-\[\]]/g, ""), 180);
  doc.setFontSize(11);
  doc.text(lines, 15, 15);
  doc.save(`${meeting.title.replace(/[^a-z0-9]/gi, "_")}.pdf`);
}

export function meetingToMarkdown(meeting: Meeting): string {
  const actionItems: ActionItem[] = meeting.action_items ? JSON.parse(meeting.action_items) : [];
  const decisions: Decision[] = meeting.decisions ? JSON.parse(meeting.decisions) : [];
  const keyPoints: string[] = meeting.key_discussion_points ? JSON.parse(meeting.key_discussion_points) : [];
  const risks: string[] = meeting.risks ? JSON.parse(meeting.risks) : [];
  const openQuestions: string[] = meeting.open_questions ? JSON.parse(meeting.open_questions) : [];
  const nextAgenda: string[] = meeting.next_meeting_agenda ? JSON.parse(meeting.next_meeting_agenda) : [];

  let md = `# ${meeting.title}\n\n`;
  md += `*${new Date(meeting.created_at).toLocaleDateString()}*\n\n`;

  if (meeting.executive_summary) {
    md += `## Executive Summary\n\n${meeting.executive_summary}\n\n`;
  }
  if (meeting.detailed_summary) {
    md += `## Detailed Summary\n\n${meeting.detailed_summary}\n\n`;
  }
  if (keyPoints.length) {
    md += `## Key Discussion Points\n\n${keyPoints.map((k) => `- ${k}`).join("\n")}\n\n`;
  }
  if (actionItems.length) {
    md += `## Action Items\n\n`;
    md += actionItems
      .map((a) => `- [ ] ${a.task}${a.owner ? ` (${a.owner})` : ""}${a.due_date ? ` — due ${a.due_date}` : ""}`)
      .join("\n");
    md += "\n\n";
  }
  if (decisions.length) {
    md += `## Decisions\n\n${decisions.map((d) => `- ${d.decision}`).join("\n")}\n\n`;
  }
  if (risks.length) {
    md += `## Risks\n\n${risks.map((r) => `- ⚠ ${r}`).join("\n")}\n\n`;
  }
  if (openQuestions.length) {
    md += `## Open Questions\n\n${openQuestions.map((q) => `- ${q}`).join("\n")}\n\n`;
  }
  if (nextAgenda.length) {
    md += `## Next Meeting Agenda\n\n${nextAgenda.map((a) => `- ${a}`).join("\n")}\n\n`;
  }

  return md;
}

export function downloadMarkdown(meeting: Meeting) {
  const md = meetingToMarkdown(meeting);
  const blob = new Blob([md], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${meeting.title.replace(/[^a-z0-9]/gi, "_")}.md`;
  a.click();
  URL.revokeObjectURL(url);
}