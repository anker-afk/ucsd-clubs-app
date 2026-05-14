async function searchEvents() {
    const keyword = document.getElementById('searchInput').value;
    const response = await fetch(`http://127.0.0.1:8000/search?keyword=${keyword}`);
    const data = await response.json();
    displayResults(data.results);
}

async function filterEvents(event_type) {
    const response = await fetch(`http://127.0.0.1:8000/filter?event_type=${event_type}`);
    const data = await response.json();
    displayResults(data.results);
}

function displayResults(results) {
    const container = document.getElementById('results');
    container.innerHTML = '';

    if (results.length === 0) {
        container.innerHTML = '<p>No events found.</p>';
        return;
    }

    results.forEach(event => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>${event.event_name}</h3>
            <span class="tag">${event.event_type}</span>
            <p><strong>Club:</strong> ${event.club_name}</p>
            <p><strong>Venue:</strong> ${event.venue}</p>
            <p><strong>Date:</strong> ${event.start_time}</p>
            <p>${event.description}</p>
            <button class="calendar-btn" onclick="addToCalendar('${event.event_name}', '${event.start_time}', '${event.end_time}', '${event.venue}')">
                + Add to Google Calendar
            </button>
        `;
        container.appendChild(card);
    });
}

function addToCalendar(name, start, end, venue) {
    const startFormatted = start.replace(/[-: ]/g, '').slice(0, 15) + 'Z';
    const endFormatted = end.replace(/[-: ]/g, '').slice(0, 15) + 'Z';
    const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(name)}&dates=${startFormatted}/${endFormatted}&location=${encodeURIComponent(venue)}`;
    window.open(url);
}