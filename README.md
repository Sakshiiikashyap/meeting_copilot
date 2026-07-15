# AI Meeting Copilot

A full-stack SaaS application that transforms raw meeting transcripts into 13 structured AI-generated outputs — executive summaries, action items, decisions, risks, follow-up emails, and more — using a provider-agnostic LLM architecture.

## Features

- **13 AI-generated outputs** from a single transcript: executive summary, detailed summary, key discussion points, action items, decisions, risks, open questions, follow-up email, next meeting agenda, AI-generated title, tags, category, and sentiment analysis
- **Provider-agnostic LLM layer** — swap between OpenAI and Groq via a single config change, with retry logic and rate limiting built in
- **Structured output validation** — all AI responses are parsed and validated with Pydantic before being persisted, preventing malformed data from reaching the database
- **File parsing** — accepts pasted text, `.txt`, `.pdf`, and `.docx` transcript uploads
- **Full authentication** — JWT-based auth with per-user data isolation and IDOR protection
- **Inline editing & export** — edit AI-generated summaries directly, export to Markdown or PDF
- **Light/dark theming**, search, and meeting management

## Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, JWT, pytest
**Frontend:** React, TypeScript, Vite, Tailwind CSS
**AI:** Groq API (Llama 3.1), OpenAI-compatible provider abstraction
**Infra:** Docker-ready, deployable to Railway (backend) + Vercel (frontend)

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for a detailed breakdown of the layered backend design, the LLM provider abstraction pattern, and key engineering decisions.

## Running Locally

### Backend
\`\`\`bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
cp .env.example .env         # fill in your own values
alembic upgrade head
uvicorn app.main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
cp .env.example .env         # fill in your own values
npm run dev
\`\`\`

### Running Tests
\`\`\`bash
cd backend
pytest -v
\`\`\`

## Key Engineering Decisions

- **Why a wide `meetings` table instead of separate tables per AI output:** the relationship is strictly 1:1 with no independent lifecycle — see ARCHITECTURE.md for the full reasoning.
- **Why Groq instead of only OpenAI:** cost — the provider abstraction layer made this a one-file swap, which is the actual point of building it that way.
- **Why structured JSON outputs with Pydantic validation:** LLMs don't guarantee valid JSON; malformed responses are caught and rejected before they can corrupt stored data.

## License

MIT