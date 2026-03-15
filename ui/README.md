# Agent Chat UI (Next.js + Tailwind)

Modular Next.js app converted from `code.html`. Uses Tailwind CSS and the same chat/streaming behavior, with the backend served by the FastAPI server in `../server`.

## Setup

```bash
npm install
cp .env.example .env   # optional: set API_BASE_URL if backend runs on another host/port
```

## Run

1. Start the FastAPI backend (from `agent/server`):

   ```bash
   cd ../server && uvicorn main:app --reload
   ```

2. Start the Next.js dev server:

   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000). Chat requests are proxied to the backend via `src/app/api/chat/route.ts` (default: `http://127.0.0.1:8000`).

## Structure

- `src/app/` – App router: `layout.tsx`, `page.tsx`, `globals.css`, `api/chat/route.ts`
- `src/components/` – Sidebar, ChatArea, ChatInput, ThoughtBlock, WelcomeMessage, UserMessage, AssistantMessage, icons
- `src/hooks/useChat.ts` – Chat state and streaming logic

## Env

| Variable        | Description                          | Default              |
|----------------|--------------------------------------|----------------------|
| `API_BASE_URL` | FastAPI backend base URL for proxy   | `http://127.0.0.1:8000` |
