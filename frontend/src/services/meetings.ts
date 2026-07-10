import api from "./api";
import type { Meeting, MeetingListItem } from "../types/meeting";

export async function listMeetings(): Promise<MeetingListItem[]> {
  const res = await api.get("/meetings/");
  return res.data;
}

export async function getMeeting(id: number): Promise<Meeting> {
  const res = await api.get(`/meetings/${id}`);
  return res.data;
}

export async function createMeeting(title: string, raw_transcript: string): Promise<Meeting> {
  const res = await api.post("/meetings/", { title, raw_transcript });
  return res.data;
}

export async function uploadMeeting(title: string, file: File): Promise<Meeting> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post(`/meetings/upload?title=${encodeURIComponent(title)}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function deleteMeeting(id: number): Promise<void> {
  await api.delete(`/meetings/${id}`);
}

export async function generateExecutiveSummary(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/summarize`);
  return res.data;
}

export async function generateDetailedSummary(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/detailed-summary`);
  return res.data;
}

export async function generateActionItems(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/action-items`);
  return res.data;
}

export async function generateDecisions(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/decisions`);
  return res.data;
}

export async function generateKeyPoints(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/key-points`);
  return res.data;
}

export async function generateRisks(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/risks`);
  return res.data;
}

export async function generateOpenQuestions(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/open-questions`);
  return res.data;
}

export async function generateFollowUpEmail(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/follow-up-email`);
  return res.data;
}

export async function generateNextAgenda(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/next-agenda`);
  return res.data;
}

export async function generateTitle(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/ai-title`);
  return res.data;
}

export async function generateTags(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/tags`);
  return res.data;
}

export async function generateSentiment(id: number): Promise<Meeting> {
  const res = await api.post(`/meetings/${id}/sentiment`);
  return res.data;
}

export async function searchMeetings(query: string): Promise<MeetingListItem[]> {
  const res = await api.get(`/meetings/search/?q=${encodeURIComponent(query)}`);
  return res.data;
}