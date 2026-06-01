const API_BASE = "http://127.0.0.1:8000";

// ── Helpers ──────────────────────────────────────────────────────────────────

function formatDate(datetimeStr) {
  const d = new Date(datetimeStr.replace(" ", "T"));
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
    + " at "
    + d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
}

function showLoading() {
  document.getElementById("results").innerHTML =
    '<p style="color:#64748b; text-align:center;">Loading events...</p>';
}

function showError(msg) {
  const p = document.createElement("p");
  p.style.cssText = "color:#dc2626; text-align:center;";
  p.textContent = msg;
  const container = document.getElementById("results");
  container.innerHTML = "";
  container.appendChild(p);
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

// ── Display ───────────────────────────────────────────────────────────────────

function displayResults(results) {
  const container = document.getElementById("results");
  container.innerHTML = "";

  if (!results || results.length === 0) {
    container.innerHTML = '<p style="color:#64748b; text-align:center;">No events found.</p>';
    return;
  }

  results.forEach((event) => {
    const card = document.createElement("div");
    card.className = "card";

    const title = document.createElement("h3");
    title.textContent = event.event_name;

    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = event.event_type;

    const clubP = document.createElement("p");
    clubP.innerHTML = "<strong>Club:</strong> ";
    clubP.appendChild(document.createTextNode(event.club_name));

    const venueP = document.createElement("p");
    venueP.innerHTML = "<strong>Venue:</strong> ";
    venueP.appendChild(document.createTextNode(event.venue));

    const dateP = document.createElement("p");
    dateP.innerHTML = "<strong>Date:</strong> ";
    dateP.appendChild(document.createTextNode(formatDate(event.start_time)));

    const descP = document.createElement("p");
    descP.textContent = event.description;

    const calBtn = document.createElement("button");
    calBtn.className = "calendar-btn";
    calBtn.textContent = "+ Add to Google Calendar";
    calBtn.addEventListener("click", () =>
      addToCalendar(event.event_name, event.start_time, event.end_time, event.venue)
    );

    card.append(title, tag, clubP, venueP, dateP, descP, calBtn);
    container.appendChild(card);
  });
}

// ── Search & filter ───────────────────────────────────────────────────────────

async function searchEvents() {
  const keyword = document.getElementById("searchInput").value.trim();
  if (!keyword) {
    document.getElementById("results").innerHTML =
      '<p style="color:#64748b; text-align:center;">Search for an event or select a category above to get started.</p>';
    return;
  }
  showLoading();
  try {
    const data = await apiFetch(`/search?keyword=${encodeURIComponent(keyword)}`);
    displayResults(data.results);
  } catch (e) {
    showError("Search failed: " + e.message);
  }
}

async function filterEvents(event_type) {
  showLoading();
  try {
    const data = await apiFetch(`/filter?event_type=${event_type}`);
    displayResults(data.results);
  } catch (e) {
    showError("Filter failed: " + e.message);
  }
}

async function loadAllEvents() {
  showLoading();
  try {
    const data = await apiFetch("/events");
    displayResults(data.results);
  } catch (e) {
    showError("Could not load events. Make sure the server is running.");
  }
}

// ── Club chips ────────────────────────────────────────────────────────────────

async function loadClubChips() {
  try {
    const data = await apiFetch("/clubs");
    const row = document.getElementById("clubChipsRow");
    row.innerHTML = "";
    const icons = {
      "Artificial Intelligence": "fa-robot",
      "Cybersecurity": "fa-shield-halved",
      "Robotics": "fa-gears",
      "Data Science": "fa-chart-simple",
      "Computer Science": "fa-laptop-code",
      "Entrepreneurship": "fa-lightbulb",
      "Diversity in Tech": "fa-users",
    };
    data.clubs.forEach((club) => {
      const icon = icons[club.category] || "fa-users";
      const span = document.createElement("span");
      span.className = "club-tag";
      span.onclick = () => goToClub(club.name);
      span.innerHTML = `<i class="fa-solid ${icon}"></i>`;
      span.appendChild(document.createTextNode(club.name));
      row.appendChild(span);
    });
  } catch (e) {
    // Non-critical — chips just won't show
    console.error("Could not load club chips:", e.message);
  }
}

// ── Calendar ──────────────────────────────────────────────────────────────────

function toCalendarDate(datetimeStr) {
  const clean = datetimeStr.replace(/[-: ]/g, "");
  return clean.slice(0, 8) + "T" + clean.slice(8, 14) + "Z";
}

function addToCalendar(name, start, end, venue) {
  const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(name)}&dates=${toCalendarDate(start)}/${toCalendarDate(end)}&location=${encodeURIComponent(venue)}`;
  window.open(url);
}

function goToClub(name) {
  window.location.href = "club.html?name=" + encodeURIComponent(name);
}

// ── Modal ─────────────────────────────────────────────────────────────────────

function openModal() {
  document.getElementById("submitModal").style.display = "block";
  loadClubDropdown();
}

function closeModal() {
  document.getElementById("submitModal").style.display = "none";
}

function showTab(tab) {
  document.getElementById("eventForm").style.display = tab === "event" ? "block" : "none";
  document.getElementById("clubForm").style.display = tab === "club" ? "block" : "none";
}

async function loadClubDropdown() {
  try {
    const data = await apiFetch("/clubs");
    const select = document.getElementById("s_club_name");
    select.innerHTML = '<option value="">Select Club</option>';
    data.clubs.forEach((club) => {
      const opt = document.createElement("option");
      opt.value = club.name;
      opt.textContent = club.name;
      select.appendChild(opt);
    });
  } catch (e) {
    console.error("Could not load clubs for dropdown:", e.message);
  }
}

// ── Form validation ───────────────────────────────────────────────────────────

function validateEventForm() {
  const fields = [
    ["s_club_name", "Club"],
    ["s_event_name", "Event Name"],
    ["s_description", "Description"],
    ["s_venue", "Venue"],
    ["s_start_date", "Start Date"],
    ["s_start_time", "Start Time"],
    ["s_end_date", "End Date"],
    ["s_end_time", "End Time"],
    ["s_event_type", "Event Type"],
    ["s_submitter_name", "Your Name"],
    ["s_submitter_email", "Your Email"],
  ];
  for (const [id, label] of fields) {
    if (!document.getElementById(id).value.trim()) {
      alert(`Please fill in: ${label}`);
      return false;
    }
  }
  const email = document.getElementById("s_submitter_email").value;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    alert("Please enter a valid email address.");
    return false;
  }
  return true;
}

function validateClubForm() {
  const fields = [
    ["c_name", "Club Name"],
    ["c_description", "Description"],
    ["c_category", "Category"],
    ["c_contact_name", "Contact Name"],
    ["c_contact_email", "Contact Email"],
  ];
  for (const [id, label] of fields) {
    if (!document.getElementById(id).value.trim()) {
      alert(`Please fill in: ${label}`);
      return false;
    }
  }
  const email = document.getElementById("c_contact_email").value;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    alert("Please enter a valid email address.");
    return false;
  }
  return true;
}

// ── Submissions ───────────────────────────────────────────────────────────────

async function submitEvent() {
  if (!validateEventForm()) return;

  const payload = {
    club_name: document.getElementById("s_club_name").value,
    event_name: document.getElementById("s_event_name").value,
    description: document.getElementById("s_description").value,
    venue: document.getElementById("s_venue").value,
    start_date: document.getElementById("s_start_date").value,
    start_time: document.getElementById("s_start_time").value,
    end_date: document.getElementById("s_end_date").value,
    end_time: document.getElementById("s_end_time").value,
    event_type: document.getElementById("s_event_type").value,
    submitter_name: document.getElementById("s_submitter_name").value,
    submitter_email: document.getElementById("s_submitter_email").value,
  };

  try {
    const data = await apiFetch("/submit-event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    alert(data.message);
    closeModal();
  } catch (e) {
    alert("Submission failed: " + e.message);
  }
}

async function submitClub() {
  if (!validateClubForm()) return;

  const payload = {
    name: document.getElementById("c_name").value,
    description: document.getElementById("c_description").value,
    category: document.getElementById("c_category").value,
    website: document.getElementById("c_website").value || null,
    instagram: document.getElementById("c_instagram").value || null,
    discord: document.getElementById("c_discord").value || null,
    contact_name: document.getElementById("c_contact_name").value,
    contact_email: document.getElementById("c_contact_email").value,
  };

  try {
    const data = await apiFetch("/submit-club", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    alert(data.message);
    closeModal();
  } catch (e) {
    alert("Submission failed: " + e.message);
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("results").innerHTML =
    '<p style="color:#64748b; text-align:center;">Search for an event or select a category above to get started.</p>';
  loadClubChips();
});
