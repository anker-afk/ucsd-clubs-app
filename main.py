import logging
from fastapi import FastAPI, Depends, HTTPException, Security, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, EmailStr, field_validator
import re
from typing import Optional, Literal, get_args
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database import get_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ucsd-clubs-secret-2026"
api_key_header = APIKeyHeader(name="X-API-Key")

def require_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

EventType = Literal["workshop", "panel", "seminar", "competition", "social"]
VALID_EVENT_TYPES = set(get_args(EventType))

ClubCategory = Literal[
    "Artificial Intelligence", "Cybersecurity", "Robotics",
    "Data Science", "Computer Science", "Entrepreneurship", "Diversity in Tech"
]

def format_row(row):
    return {
        "club_name": row[0],
        "event_name": row[1],
        "event_type": row[2],
        "venue": row[3],
        "start_time": str(row[4]),
        "end_time": str(row[5]),
        "description": row[6],
    }


@app.get("/")
def read_root():
    return {"message": "UCSD Clubs API is running"}


@app.get("/events")
@limiter.limit("60/minute")
def get_events(request: Request, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    offset = (page - 1) * limit
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT clubs.name, events.name, events.event_type, events.venue,
                   events.start_time, events.end_time, events.description
            FROM clubs
            JOIN events ON clubs.id = events.club_id
            WHERE events.is_approved = TRUE AND clubs.is_approved = TRUE
            ORDER BY events.start_time
            LIMIT %s OFFSET %s
        """, (limit, offset))
        rows = cursor.fetchall()
        cursor.execute("""
            SELECT COUNT(*) FROM events
            JOIN clubs ON clubs.id = events.club_id
            WHERE events.is_approved = TRUE AND clubs.is_approved = TRUE
        """)
        total = cursor.fetchone()[0]
    logger.info("GET /events page=%d limit=%d total=%d", page, limit, total)
    return {"results": [format_row(r) for r in rows], "total": total, "page": page, "limit": limit}


@app.get("/clubs")
@limiter.limit("60/minute")
def get_clubs(request: Request):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category FROM clubs WHERE is_approved = TRUE ORDER BY name")
        rows = cursor.fetchall()
    return {"clubs": [{"id": r[0], "name": r[1], "category": r[2]} for r in rows]}


@app.get("/search")
@limiter.limit("30/minute")
def search_clubs(request: Request, keyword: str, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    offset = (page - 1) * limit
    pattern = f"%{keyword}%"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT clubs.name, events.name, events.event_type, events.venue,
                   events.start_time, events.end_time, events.description
            FROM clubs
            JOIN events ON clubs.id = events.club_id
            WHERE events.is_approved = TRUE AND clubs.is_approved = TRUE
              AND (clubs.name ILIKE %s OR events.name ILIKE %s OR events.description ILIKE %s)
            ORDER BY events.start_time
            LIMIT %s OFFSET %s
        """, (pattern, pattern, pattern, limit, offset))
        rows = cursor.fetchall()
    logger.info("GET /search keyword=%r results=%d", keyword, len(rows))
    return {"results": [format_row(r) for r in rows]}


@app.get("/filter")
@limiter.limit("60/minute")
def filter_events(request: Request, event_type: str, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    if event_type not in VALID_EVENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid event_type. Must be one of: {', '.join(VALID_EVENT_TYPES)}")
    offset = (page - 1) * limit
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT clubs.name, events.name, events.event_type, events.venue,
                   events.start_time, events.end_time, events.description
            FROM clubs
            JOIN events ON clubs.id = events.club_id
            WHERE events.is_approved = TRUE AND clubs.is_approved = TRUE
              AND events.event_type ILIKE %s
            ORDER BY events.start_time
            LIMIT %s OFFSET %s
        """, (event_type, limit, offset))
        rows = cursor.fetchall()
    logger.info("GET /filter event_type=%r results=%d", event_type, len(rows))
    return {"results": [format_row(r) for r in rows]}


@app.get("/club")
@limiter.limit("60/minute")
def get_club(request: Request, name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, description, category, website, instagram, discord, contact_name, contact_email
            FROM clubs
            WHERE name ILIKE %s AND is_approved = TRUE
        """, (name,))
        row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Club not found")
    return {
        "name": row[0], "description": row[1], "category": row[2],
        "website": row[3], "instagram": row[4], "discord": row[5],
        "contact_name": row[6], "contact_email": row[7],
    }


# --- Submission models ---

class EventSubmission(BaseModel):
    club_name: str
    event_name: str
    description: str
    venue: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    event_type: EventType
    submitter_name: str
    submitter_email: EmailStr

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date(cls, v):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("must be YYYY-MM-DD")
        return v

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time(cls, v):
        if not re.match(r"^\d{2}:\d{2}(:\d{2})?$", v):
            raise ValueError("must be HH:MM")
        return v

class ClubSubmission(BaseModel):
    name: str
    description: str
    category: ClubCategory
    website: Optional[str] = None
    instagram: Optional[str] = None
    discord: Optional[str] = None
    contact_name: str
    contact_email: EmailStr


@app.post("/submit-event")
@limiter.limit("10/minute")
def submit_event(request: Request, event: EventSubmission):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM clubs WHERE name ILIKE %s AND is_approved = TRUE", (event.club_name,))
            club = cursor.fetchone()
            if not club:
                raise HTTPException(status_code=404, detail="Club not found")
            start_dt = f"{event.start_date} {event.start_time}"
            end_dt = f"{event.end_date} {event.end_time}"
            cursor.execute("""
                INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type, is_approved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
            """, (club[0], event.event_name, event.description, event.venue, start_dt, end_dt, event.event_type))
            conn.commit()
            logger.info("Event submitted for approval: %r by %r", event.event_name, event.submitter_email)
            return {"message": "Event submitted and pending approval"}
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            logger.error("submit_event error: %s", e)
            raise HTTPException(status_code=500, detail="Submission failed")


@app.post("/submit-club")
@limiter.limit("10/minute")
def submit_club(request: Request, club: ClubSubmission):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM clubs WHERE name ILIKE %s", (club.name,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Club already exists")
            cursor.execute("""
                INSERT INTO clubs (name, description, category, website, instagram, discord, contact_name, contact_email, is_approved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
            """, (club.name, club.description, club.category, club.website, club.instagram,
                  club.discord, club.contact_name, club.contact_email))
            conn.commit()
            logger.info("Club submitted for approval: %r by %r", club.name, club.contact_email)
            return {"message": "Club submitted and pending approval"}
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            logger.error("submit_club error: %s", e)
            raise HTTPException(status_code=500, detail="Submission failed")


# --- Admin endpoints ---

@app.get("/admin/pending-events", dependencies=[Depends(require_api_key)])
def pending_events():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT events.id, clubs.name, events.name, events.event_type,
                   events.venue, events.start_time, events.end_time, events.description, events.created_at
            FROM events
            JOIN clubs ON clubs.id = events.club_id
            WHERE events.is_approved = FALSE
            ORDER BY events.created_at
        """)
        rows = cursor.fetchall()
    return {"pending": [
        {"id": r[0], "club_name": r[1], "event_name": r[2], "event_type": r[3],
         "venue": r[4], "start_time": str(r[5]), "end_time": str(r[6]),
         "description": r[7], "submitted_at": str(r[8])}
        for r in rows
    ]}


@app.get("/admin/pending-clubs", dependencies=[Depends(require_api_key)])
def pending_clubs():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description, category, website, contact_name, contact_email, created_at
            FROM clubs
            WHERE is_approved = FALSE
            ORDER BY created_at
        """)
        rows = cursor.fetchall()
    return {"pending": [
        {"id": r[0], "name": r[1], "description": r[2], "category": r[3],
         "website": r[4], "contact_name": r[5], "contact_email": r[6], "submitted_at": str(r[7])}
        for r in rows
    ]}


@app.post("/admin/approve-event/{event_id}", dependencies=[Depends(require_api_key)])
def approve_event(event_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET is_approved = TRUE WHERE id = %s", (event_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        conn.commit()
    logger.info("Event approved: id=%d", event_id)
    return {"message": "Event approved"}


@app.post("/admin/reject-event/{event_id}", dependencies=[Depends(require_api_key)])
def reject_event(event_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = %s AND is_approved = FALSE", (event_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found or already approved")
        conn.commit()
    logger.info("Event rejected: id=%d", event_id)
    return {"message": "Event rejected and removed"}


@app.post("/admin/approve-club/{club_id}", dependencies=[Depends(require_api_key)])
def approve_club(club_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE clubs SET is_approved = TRUE WHERE id = %s", (club_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Club not found")
        conn.commit()
    logger.info("Club approved: id=%d", club_id)
    return {"message": "Club approved"}


@app.post("/admin/reject-club/{club_id}", dependencies=[Depends(require_api_key)])
def reject_club(club_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clubs WHERE id = %s AND is_approved = FALSE", (club_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Club not found or already approved")
        conn.commit()
    logger.info("Club rejected: id=%d", club_id)
    return {"message": "Club rejected and removed"}
