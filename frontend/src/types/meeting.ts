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
  action_items: string | null;
  decisions: string | null;
  key_discussion_points: string | null;
  risks: string | null;
  open_questions: string | null;
  follow_up_email: string | null;
  next_meeting_agenda: string | null;
  ai_title: string | null;
  tags: string | null;
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