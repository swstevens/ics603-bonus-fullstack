# Reflection Manager - Full Stack Application

## Setup Instructions

### Prerequisites
- Python 3.10+
- Supabase account (for PostgreSQL database)
- OpenAI API key

### 1. Clone and Create Virtual Environment
```bash
git clone https://github.com/swstevens/ics603-bonus-fullstack
cd ics603-bonus-fullstack
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Insert the provided `.env` file in the `backend/` directory with:
```
SUPABASE_DB_URL=postgresql://...
OPENAI_API_KEY=sk-...
```
Database should be initialized in my supabase.

### 5. Start the Backend
```bash
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Start the Frontend (in a new terminal)
```bash
cd front-end
source ../venv/bin/activate
python main.py
```

The frontend will launch at `http://localhost:32000` (or similar port shown in terminal)

## Project Structure

```
ics603-bonus-fullstack/
├── backend/
│   ├── api.py              # FastAPI application with all endpoints
│   ├── models.py           # SQLAlchemy models (User, Topic, Reflection)
│   ├── classifier.py       # OpenAI topic classification logic
│   ├── create_db.py        # Database initialization script
│   └── .env                # Environment variables (not in repo)
├── front-end/
│   ├── main.py             # Main FastHTML app with routing
│   └── components/
│       ├── add_form.py     # Form to add new reflections
│       ├── reflections_list.py  # Table view of reflections
│       └── single_reflection.py # Detail view for one reflection
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

### Users
- `GET /api/users` - Get all users

### Reflections
- `GET /api/reflections` - Get all reflections (or filter by `?user_id=1`)
- `GET /api/reflections/{id}` - Get single reflection
- `POST /api/reflections` - Create reflection
- `POST /api/reflections/classify` - Classify topics for a reflection

### Topics
- `GET /api/topics` - Get all topics (or filter by `?user_id=1`)
- `POST /api/topics` - Create topics

## Frontend Routes

- `/` - Home page with add reflection form
- `/reflections` - List all reflections with user filter
- `/reflection/{id}` - View single reflection details

## Implementation Notes

- "All Users" option (id=0) shows reflections across all users
- Topics are automatically created/reused during reflection creation
- UI components are separated in `components/` folder for modularity
