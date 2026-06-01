# UCSD Club Events Hub

A full-stack web application that aggregates UCSD STEM club events in one place. Search by keyword, filter by category, browse clubs, submit new events, and add anything directly to Google Calendar.

## Features

- Browse all upcoming events on page load
- Search events by keyword across club names, event names, and descriptions
- Filter events by type: workshop, panel, seminar, competition, social
- Click any club chip to view its full profile page
- Add events to Google Calendar in one click
- Submit new events or register a new club via the submission form
- Submissions go through an admin approval flow before appearing publicly
- Paginated API responses (default 20 per page, max 100)
- Rate limiting on all endpoints to prevent abuse

## Tech Stack

**Backend**
- Python + FastAPI
- PostgreSQL
- psycopg2 (with connection pooling)
- Pydantic (request validation)
- slowapi (rate limiting)

**Frontend**
- HTML, CSS, Vanilla JavaScript

## Clubs Included

1. ACM UCSD
2. ACM AI at UCSD
3. ACM Cyber at UCSD
4. Triton Robotics
5. DS3 at UCSD
6. Women in Computing (WIC)
7. The Basement UCSD

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 16
- pip

### Setup

**1. Clone the repository**
```bash
git clone git@github.com:anker-afk/ucsd-clubs-app.git
cd ucsd-clubs-app
```

**2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install fastapi uvicorn psycopg2-binary pydantic[email] slowapi
```

**4. Set up PostgreSQL database**
```bash
psql postgres
```
```sql
CREATE DATABASE ucsd_clubs;
\c ucsd_clubs
```

**5. Create the tables**
```sql
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    website TEXT,
    instagram TEXT,
    discord TEXT,
    contact_name TEXT,
    contact_email TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    club_id INTEGER REFERENCES clubs(id),
    name TEXT NOT NULL,
    description TEXT,
    venue TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    event_type TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_events_start_time ON events(start_time);
CREATE INDEX idx_events_club_id ON events(club_id);
CREATE INDEX idx_events_approved ON events(is_approved);
CREATE INDEX idx_clubs_name ON clubs(name);
CREATE INDEX idx_clubs_approved ON clubs(is_approved);
```

**6. Seed the database**
```bash
psql -U your_username ucsd_clubs -f seed_data.sql
```

Then mark the seed data as approved:
```sql
UPDATE clubs SET is_approved = TRUE;
UPDATE events SET is_approved = TRUE;
```

**7. Update database credentials in `database.py`**

Replace `smritiattam` with your system username:
```python
_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    dbname="ucsd_clubs",
    user="your_username_here",
    password="",
    host="localhost",
    port="5432"
)
```

**8. Start the backend server**
```bash
uvicorn main:app --reload
```

**9. Open the frontend**

Open `index.html` in your browser using Live Server in VS Code or directly in Chrome.

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/events?page=1&limit=20` | All approved events (paginated) |
| GET | `/clubs` | All approved clubs |
| GET | `/club?name=ACM+UCSD` | Single club detail |
| GET | `/search?keyword=AI` | Search events by keyword |
| GET | `/filter?event_type=workshop` | Filter events by type |

### Authenticated (requires `X-API-Key` header)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/submit-event` | Submit a new event for approval |
| POST | `/submit-club` | Register a new club for approval |
| GET | `/admin/pending-events` | List all unapproved events |
| GET | `/admin/pending-clubs` | List all unapproved clubs |
| POST | `/admin/approve-event/{id}` | Approve an event |
| POST | `/admin/reject-event/{id}` | Reject and delete an event |
| POST | `/admin/approve-club/{id}` | Approve a club |
| POST | `/admin/reject-club/{id}` | Reject and delete a club |

The API key is set in `main.py` as `API_KEY`. Change it before deploying.

Visit `http://127.0.0.1:8000/docs` to explore and test all endpoints interactively.

## Project Structure

```
ucsd-clubs-app/
├── main.py          # FastAPI app — all endpoints, auth, rate limiting
├── database.py      # PostgreSQL connection pool
├── seed_data.sql    # Club and event seed data
├── index.html       # Main page — search, filter, event cards
├── club.html        # Club detail page
├── script.js        # Main page logic
├── club.js          # Club detail page logic
├── styles.css       # Styling
└── README.md
```

## Project Status

- [x] PostgreSQL database with 7 clubs and 21 events
- [x] Search, filter, and browse endpoints
- [x] Club detail page
- [x] Event submission and club registration forms
- [x] Admin approval workflow
- [x] API key authentication on write endpoints
- [x] Rate limiting on all endpoints
- [x] Connection pooling
- [x] Google Calendar integration
- [x] Paginated API responses
- [ ] Deployment

## Team

Built by UCSD students as part of the SP26 Programming for Tritons project.
