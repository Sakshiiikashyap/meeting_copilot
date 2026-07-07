export interface ActionItem {
  task: string;
  owner: string | null;
  due_date: string | null;
}

export interface Decision {
  decision: string;
  context: string | null;
}

export interface FollowUpEmail {
  subject: string;
  body: string;
}

export interface Meeting {
  id: number;
  user_id: number;
  title: string;
  raw_transcript: string;
  status: string;
  executive_summary: string | null;
  detailed_summary: string | null;
  action_items: string | null; // JSON string
  decisions: string | null; // JSON string
  key_discussion_points: string | null; // JSON string
  risks: string | null; // JSON string
  open_questions: string | null; // JSON string
  follow_up_email: string | null; // JSON string
  next_meeting_agenda: string | null; // JSON string
  ai_title: string | null;
  tags: string | null; // JSON string
  category: string | null;
  sentiment: string | null;
  sentiment_reason: string | null;
  created_at: string;
  updated_at: string;
}

export interface MeetingListItem {
  id: number;
  title: string;
  status: string;
  created_at: string;
}