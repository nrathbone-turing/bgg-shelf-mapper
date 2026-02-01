# bgg-shelf-mapper

A small, local-first app to:
- sync your BoardGameGeek collection (optional / later),
- maintain *your* location metadata (which cube/shelf/bin each game lives in),
- browse/search your games,
- and view/assign them in a visual fixture grid (starting with a 2-row x 5-column cube fixture).

## Tech (simple + evolvable)
- **Frontend:** Vite + React + TypeScript
- **Backend:** FastAPI + SQLite (SQLAlchemy)
- **Dev experience:** Run locally OR via Docker Compose

---

## Quickstart (Docker)
1) Copy env file:
```bash
cp .env.example .env
```

2) Start:
```bash
docker compose up --build
```

3) Open:
- Web UI: http://localhost:5173
- API docs (Swagger): http://localhost:8000/docs

The API will auto-seed:
- one fixture: `Office Cubes (2x5)`
- a few sample games (from your list)

---

## Quickstart (Local, no Docker)
### Backend
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:5173

---

## GitHub repo setup (push this scaffold)
### Option A: GitHub UI (simple)
1) On GitHub, click **New repository**
2) Name it something like: `bgg-shelf-mapper`
3) Keep it public/private however you prefer
4) Don’t initialize with a README (this repo already has one)

Then in this folder:
```bash
git init
git add .
git commit -m "Initial scaffold: Vite web + FastAPI api"
git branch -M main
git remote add origin git@github.com:<YOUR_USER>/bgg-shelf-mapper.git
git push -u origin main
```

### Option B: GitHub CLI (fastest)
If you have `gh` installed and authenticated:
```bash
git init
git add .
git commit -m "Initial scaffold: Vite web + FastAPI api"
gh repo create bgg-shelf-mapper --source=. --public --remote=origin --push
```

> Tip: Keep `.env` out of git (it already is).

---

## Where the important code is

### Backend
- `apps/api/app/models.py` – DB tables (Game, Fixture, Placement)
- `apps/api/app/seed.py` – inserts sample data if DB is empty
- `apps/api/app/routes/*` – API endpoints

### Frontend
- `apps/web/src/components/FixtureGrid.tsx` – the 2x5 grid UI
- `apps/web/src/components/GameSearch.tsx` – search + assign flow
- `apps/web/src/api.ts` – typed fetch wrappers

---

## Next upgrades
- Drag & drop to move games between cubes
- Thumbnails/box art (requires fetching image URLs via BGG API)
- Multiple fixtures / rooms
- “Unassigned pile” view
