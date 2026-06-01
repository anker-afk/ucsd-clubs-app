// 1. Read the club name from the URL string
const params = new URLSearchParams(window.location.search);
const name = params.get("name");

// 2. Fetch the specific club dataset metadata model
fetch("http://127.0.0.1:8000/club?name=" + encodeURIComponent(name))
  .then((res) => res.json())
  .then((club) => {
    let iconClass = "fa-solid fa-cubes";
    if (club.category.toLowerCase().includes("data"))
      iconClass = "fa-solid fa-chart-pie";
    if (club.category.toLowerCase().includes("robot"))
      iconClass = "fa-solid fa-robot";
    if (club.category.toLowerCase().includes("cyber"))
      iconClass = "fa-solid fa-shield-halved";
    if (club.category.toLowerCase().includes("comput"))
      iconClass = "fa-solid fa-laptop-code";

    document.getElementById("club-info").innerHTML = `
      <section class="club-hero">
          <div class="hero-content">
              <div class="club-badge-avatar">
                  <i class="${iconClass}"></i>
              </div>
              <div class="hero-text">
                  <h1>${club.name}</h1>
                  <span class="club-category-tag">${club.category}</span>
              </div>
          </div>
      </section>

      <div class="profile-grid">
          <main class="profile-main">
              <div class="profile-card">
                  <h3><i class="fa-solid fa-circle-info"></i> About Our Organization</h3>
                  <p class="club-description">${club.description}</p>
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
                      ${club.website ? `<a href="${club.website}" target="_blank" class="social-btn web-btn"><i class="fa-solid fa-globe"></i> Visit Website</a>` : ""}
                      ${club.instagram ? `<a href="${club.instagram}" target="_blank" class="social-btn ig-btn"><i class="fa-brands fa-instagram"></i> Instagram</a>` : ""}
                      ${club.discord ? `<a href="${club.discord}" target="_blank" class="social-btn discord-btn"><i class="fa-brands fa-discord"></i> Join Discord</a>` : ""}
                  </div>
              </div>

              <div class="profile-card">
                  <h3>Official Contacts</h3>
                  <p class="meta-label">Contact Board Point</p>
                  <p class="meta-value">${club.contact_name}</p>
                  <p class="meta-label">Email Inquiries</p>
                  <p class="meta-value">
                      <a href="mailto:${club.contact_email}" class="email-link">
                          <i class="fa-solid fa-envelope"></i> ${club.contact_email}
                      </a>
                  </p>
              </div>
          </aside>
      </div>
    `;

    document.title = club.name;
  })
  .catch((err) => {
    document.getElementById("club-info").innerHTML = `
      <div class="loading-state">
          <i class="fa-solid fa-circle-exclamation"></i> Error loading club information.
      </div>`;
  });
