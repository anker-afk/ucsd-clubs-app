from fastapi import FastAPI
from database import get_connection
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"message": "UCSD Clubs API is running"}

@app.get("/search")
def search_clubs(keyword: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT clubs.name, events.name, events.event_type, events.venue, events.start_time, events.end_time, events.description
        FROM clubs
        JOIN events ON clubs.id = events.club_id
        WHERE (events.name ILIKE %s
        OR clubs.name ILIKE %s)
        AND events.status = 'approved'
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    formatted = []
    for row in results:
        formatted.append({
            "club_name": row[0],
            "event_name": row[1],
            "event_type": row[2],
            "venue": row[3],
            "start_time": str(row[4]),
            "end_time": str(row[5]),
            "description": row[6]
        })
    
    return {"results": formatted}


@app.get("/filter")
def filter_events(event_type: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT clubs.name, events.name, events.event_type, events.venue, events.start_time, events.end_time, events.description
        FROM clubs
        JOIN events ON clubs.id = events.club_id
        WHERE events.event_type ILIKE %s
        AND events.status = 'approved'
    """, (event_type,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    formatted = []
    for row in results:
        formatted.append({
            "club_name": row[0],
            "event_name": row[1],
            "event_type": row[2],
            "venue": row[3],
            "start_time": str(row[4]),
            "end_time": str(row[5]),
            "description": row[6]
        })
    
    return {"results": formatted}



class EventSubmission(BaseModel):
    club_name: str
    event_name: str
    description: str
    venue: str
    start_time: datetime
    end_time: datetime
    event_type: str
    submitter_name: str
    submitter_email: EmailStr

    @field_validator('submitter_name')
    def name_must_be_real(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v

    @field_validator('event_name')
    def event_name_must_be_real(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Event name must be at least 3 characters')
        return v

@app.post("/submit")
def submit_event(event: EventSubmission):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM clubs WHERE name ILIKE %s", (event.club_name,))
        club = cursor.fetchone()
        
        if not club:
            return {"error": "Club not found"}
        
        club_id = club[0]
        
        cursor.execute("""
            INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (

            club_id,
            event.event_name,
            event.description,
            event.venue,
            event.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            event.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            event.event_type

        ))
        
        conn.commit()
        return {"message": "Event submitted successfully and pending approval"}
    
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conn.close()


@app.get("/admin/pending")
def get_pending_events():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT events.id, clubs.name, events.name, events.event_type, 
               events.venue, events.start_time, events.description
        FROM events
        JOIN clubs ON events.club_id = clubs.id
        WHERE events.status = 'pending'
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    formatted = []
    for row in results:
        formatted.append({
            "event_id": row[0],
            "club_name": row[1],
            "event_name": row[2],
            "event_type": row[3],
            "venue": row[4],
            "start_time": str(row[5]),
            "description": row[6]
        })
    
    return {"pending_events": formatted}

@app.post("/admin/approve/{event_id}")
def approve_event(event_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE events SET status = 'approved' WHERE id = %s
        """, (event_id,))
        
        conn.commit()
        return {"message": f"Event {event_id} approved successfully"}
    
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conn.close()