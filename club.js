const API_BASE = "http://127.0.0.1:8000";
const params = new URLSearchParams(window.location.search);
const name = params.get("name");

function esc(str) {
  const d = document.createElement("div");
  d.textContent = str || "";
  return d.innerHTML;
}

function safeUrl(url) {
  if (!url) return null;
  try {
    const u = new URL(url);
    return u.protocol === "https:" || u.protocol === "http:" ? url : null;
  } catch {
    return null;
  }
}

if (!name) {
  document.getElementById("club-info").innerHTML = `
    <div class="loading-state">
      <i class="fa-solid fa-circle-exclamation"></i> No club specified.
    </div>`;
} else {
  fetch(API_BASE + "/club?name=" + encodeURIComponent(name))
    .then((res) => {
      if (!res.ok) throw new Error("Club not found");
      return res.json();
    })
    .then((club) => {
      let iconClass = "fa-solid fa-cubes";
      const cat = (club.category || "").toLowerCase();
      if (cat.includes("data")) iconClass = "fa-solid fa-chart-pie";
      else if (cat.includes("robot")) iconClass = "fa-solid fa-robot";
      else if (cat.includes("cyber")) iconClass = "fa-solid fa-shield-halved";
      else if (cat.includes("comput")) iconClass = "fa-solid fa-laptop-code";
      else if (cat.includes("artificial") || cat.includes("ai")) iconClass = "fa-solid fa-robot";
      else if (cat.includes("entrepreneur")) iconClass = "fa-solid fa-lightbulb";

      const website = safeUrl(club.website);
      const instagram = safeUrl(club.instagram);
      const discord = safeUrl(club.discord);

      document.getElementById("club-info").innerHTML = `
        <section class="club-hero">
          <div class="hero-content">
            <div class="club-badge-avatar">
              <i class="${iconClass}"></i>
            </div>
            <div class="hero-text">
              <h1>${esc(club.name)}</h1>
              <span class="club-category-tag">${esc(club.category)}</span>
            </div>
          </div>
        </section>

        <div class="profile-grid">
          <main class="profile-main">
            <div class="profile-card">
              <h3><i class="fa-solid fa-circle-info"></i> About Our Organization</h3>
              <p class="club-description">${esc(club.description)}</p>
            </div>
            <div class="profile-card">
              <h3><i class="fa-solid fa-calendar-days"></i> Upcoming Club Events</h3>
              <p>Check your calendar feed for recent matching sessions.</p>
            </div>
          </main>

          <aside class="profile-sidebar">
            <div class="profile-card">
              <h3>Connect With Us</h3>
              <div class="social-links-container">
                ${website ? `<a href="${esc(website)}" target="_blank" rel="noopener noreferrer" class="social-btn web-btn"><i class="fa-solid fa-globe"></i> Visit Website</a>` : ""}
                ${instagram ? `<a href="${esc(instagram)}" target="_blank" rel="noopener noreferrer" class="social-btn ig-btn"><i class="fa-brands fa-instagram"></i> Instagram</a>` : ""}
                ${discord ? `<a href="${esc(discord)}" target="_blank" rel="noopener noreferrer" class="social-btn discord-btn"><i class="fa-brands fa-discord"></i> Join Discord</a>` : ""}
              </div>
            </div>

            <div class="profile-card">
              <h3>Official Contacts</h3>
              <p class="meta-label">Contact Board Point</p>
              <p class="meta-value">${esc(club.contact_name)}</p>
              <p class="meta-label">Email Inquiries</p>
              <p class="meta-value">
                <a href="mailto:${esc(club.contact_email)}" class="email-link">
                  <i class="fa-solid fa-envelope"></i> ${esc(club.contact_email)}
                </a>
              </p>
            </div>
          </aside>
        </div>
      `;

      document.title = club.name;
    })
    .catch(() => {
      document.getElementById("club-info").innerHTML = `
        <div class="loading-state">
          <i class="fa-solid fa-circle-exclamation"></i> Error loading club information.
        </div>`;
    });
}
