# UCSD Club Events Hub

A full stack web application that aggregates UCSD STEM club events in one place. Search by keyword, filter by event type, and add events directly to your Google Calendar.

## Features

- Search events by keyword (e.g. "AI", "robotics", "machine learning")
- Filter events by type (workshop, panel, seminar, competition, social)
- View club details and upcoming events
- Add events directly to Google Calendar in one click

## Tech Stack

**Backend**
- Python + FastAPI
- PostgreSQL
- psycopg2

**Frontend**
- HTML, CSS, JavaScript

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

1. Clone the repository
```bash
git clone git@github.com:anker-afk/ucsd-clubs-app.git
cd ucsd-clubs-app
```

2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install fastapi uvicorn psycopg2-binary
```

4. Set up PostgreSQL database
```bash
psql postgres
CREATE DATABASE ucsd_clubs;
\c ucsd_clubs
```

5. Run the seed data
```bash
psql ucsd_clubs -f seed_data.sql
```

6. Update database credentials in `database.py`

Replace `"postgres"` with your system username:
```python
conn = psycopg2.connect(
    dbname="ucsd_clubs",
    user="your_username_here",
    password="",
    host="localhost",
    port="5432"
)
```

7. Start the backend server
```bash
uvicorn main:app --reload
```

8. Open the frontend

Open `index.html` in your browser using Live Server in VS Code or directly in Chrome.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/search?keyword=AI` | Search events by keyword |
| GET | `/filter?event_type=workshop` | Filter events by type |

Visit `http://127.0.0.1:8000/docs` to explore and test all endpoints interactively.

## Project Structure

```
ucsd-clubs-app/
├── main.py          # FastAPI app - search and filter endpoints
├── database.py      # PostgreSQL connection
├── seed_data.sql    # Club and event data
├── index.html       # Frontend
├── styles.css       # Styling
├── script.js        # Search, filter, and calendar logic
└── README.md
```

## Project Status

- [x] PostgreSQL database with 7 clubs and 21 events
- [x] Search endpoint
- [x] Filter endpoint
- [x] Frontend with event cards
- [x] Google Calendar integration
- [ ] Deployment

## Team

Built by UCSD students as part of the SP26 Programming for Tritons project.