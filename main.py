from fastapi import FastAPI
from database import get_connection
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection

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
        WHERE clubs.name ILIKE %s
        OR events.name ILIKE %s
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
    
@app.get("/club")
def get_club(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, description, category, website, instagram, discord, contact_name, contact_email
        FROM clubs
        WHERE name ILIKE %s
    """, (name,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return {"error": "Club not found"}
    return {
        "name": row[0],
        "description": row[1],
        "category": row[2],
        "website": row[3],
        "instagram": row[4],
        "discord": row[5],
        "contact_name": row[6],
        "contact_email": row[7]
    }