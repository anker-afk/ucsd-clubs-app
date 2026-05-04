from fastapi import FastAPI
from database import get_connection

app = FastAPI()

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