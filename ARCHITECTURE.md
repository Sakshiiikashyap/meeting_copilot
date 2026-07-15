# Architecture

## Backend Layering

The backend follows a strict layered architecture:

\`\`\`
routers/      → HTTP layer only: request parsing, status codes, response shaping
services/     → business logic: "what does registering a user mean"
repositories/ → the only layer that touches the database directly
models/       → SQLAlchemy ORM definitions (database shape)
schemas/      → Pydantic definitions (API contract shape)
llm/          → provider-agnostic AI integration, zero knowledge of "meetings"
prompts/      → specialized, constrained prompt templates per AI output
\`\`\`

This separation means: swapping the ORM only touches `repositories/`. Swapping the AI provider only touches `llm/factory.py`. Adding a new AI output type means one new prompt file, one new service function, one new route — the pattern is fully repeatable.

## LLM Provider Abstraction

\`\`\`python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt, user_prompt, temperature, max_tokens) -> LLMResult:
        ...
\`\`\`

Every provider (OpenAI, Groq) implements this same interface. `llm/factory.py` is the single chokepoint that decides which provider to instantiate based on config — nothing above this layer knows or cares which provider is actually running. This was validated in practice, not just designed in theory: the project originally used OpenAI and was switched to Groq (for cost reasons) with a one-file change and zero changes to business logic.

## Structured Output Validation

LLMs don't guarantee valid JSON, even when explicitly asked for it. The defense is three layers:

1. **Prompt-level enforcement** — every structured-output prompt shows the model the exact JSON skeleton expected, with explicit "return `[]` if none exist" instructions to prevent hallucinated content when there's nothing to extract.
2. **Parsing safety** (`llm/json_parser.py`) — strips markdown code fences and handles malformed JSON gracefully, raising a specific `LLMResponseError` rather than crashing.
3. **Schema validation** (Pydantic models in `schemas/ai_outputs.py`) — the parsed JSON is validated against a strict schema before ever touching the database. A malformed AI response never reaches storage.

## Database Design

A single `meetings` table holds both the meeting metadata and all 13 AI-generated fields as nullable columns, rather than a separate `meeting_insights` table. This was a deliberate choice: the relationship between a meeting and its AI outputs is strictly 1:1 with no independent lifecycle — a meeting doesn't have "many" summaries. Splitting into two tables would add a join for no real benefit at the current scope. If a future feature required versioned summaries or multi-entity relationships (e.g. "chat with this meeting"), this would be refactored into a separate table at that point — premature normalization was avoided deliberately, not by oversight.

## Authorization: Preventing IDOR

Every meeting-scoped endpoint checks not just "does this meeting exist" but "does it belong to the requesting user":

\`\`\`python
if meeting.user_id != user_id:
    raise HTTPException(status_code=403, detail="Not your meeting")
\`\`\`

This closes an Insecure Direct Object Reference vulnerability — without it, an authenticated user could access another user's data simply by guessing/incrementing meeting IDs. This is covered by an automated test (`test_cannot_access_other_users_meeting`).

## Production Hardening

- **Retry logic** (`llm/retry.py`): exponential backoff (1s, 2s, 4s) on rate-limit errors specifically — not on malformed-response errors, since retrying a genuinely bad response wastes time without fixing anything.
- **Rate limiting**: AI-generation endpoints are limited per-IP to protect both the app's own availability and the upstream LLM provider quota.
- **Structured logging**: every AI generation call logs start, success/failure, and token usage — enabling real observability rather than silent failures.

## Known Limitations

- PDF export is a plain-text dump via `jsPDF`, not a fully styled document — a production version would render HTML and convert, or generate PDFs server-side.
- AI-generation endpoints are not covered by automated tests (deliberately — testing against a real LLM API is slow, costly, and flaky; a mocked-provider test suite would be the next step).
- Session tokens are stored in `localStorage`, which is simpler to implement but more vulnerable to XSS than httpOnly cookies — a known simplification for this project's scope.