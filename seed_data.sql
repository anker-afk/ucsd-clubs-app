-- =============================================
-- UCSD Club Events App — Seed Data
-- Run this in psql while connected to ucsd_clubs
-- =============================================

-- CLUBS
INSERT INTO clubs (name, description, category, website, instagram, discord, contact_name, contact_email)
VALUES
  (
    'ACM UCSD',
    'UC San Diego''s largest computing organization with 2000+ members. Hosts 150+ technical, professional, and social events year-round across AI, cybersecurity, design, and software engineering.',
    'Computer Science',
    'https://acmucsd.com',
    'https://instagram.com/acm.ucsd',
    'https://discord.gg/acmucsd',
    'ACM Board',
    'acm@ucsd.edu'
  ),
  (
    'ACM AI at UCSD',
    'The AI-focused community within ACM UCSD. Hosts workshops, competitions, and networking events to help students navigate the world of artificial intelligence and machine learning.',
    'Artificial Intelligence',
    'https://acmucsd.com/communities',
    'https://instagram.com/acm.ucsd',
    'https://discord.gg/acmucsd',
    'ACM AI Board',
    'acm@ucsd.edu'
  ),
  (
    'ACM Cyber at UCSD',
    'UC San Diego''s largest cybersecurity community with 700+ members. Hosts workshops, industry panels, CTF training, and the annual San Diego CTF — a 48-hour hacking competition.',
    'Cybersecurity',
    'https://cyber.acmucsd.com',
    'https://instagram.com/acm.ucsd',
    'https://discord.gg/acmucsd',
    'ACM Cyber Board',
    'cyber@acmucsd.com'
  ),
  (
    'Triton Robotics',
    'A 501(c)(3) non-profit student organization at UCSD focused on robotics competitions, workshops, and community building. Currently competing in the international RoboMaster Competition by DJI.',
    'Robotics',
    'https://tritonrobotics.org',
    'https://instagram.com/tritonrobotics',
    'https://discord.gg/5ZDqNmraXU',
    'Elena Contreras Chavez',
    'tritonrobotics@ucsd.edu'
  ),
  (
    'DS3 at UCSD',
    'The Data Science Student Society at UCSD is an interdisciplinary academic organization immersing students in machine learning, statistics, data mining, predictive analytics, and emerging data science fields.',
    'Data Science',
    'https://www.ds3atucsd.com',
    'https://instagram.com/ds3ucsd',
    NULL,
    'DS3 Board',
    'ds3@ucsd.edu'
  ),
  (
    'Women in Computing at UCSD',
    'WIC is a non-profit student organization supporting the female presence in computing — open to all genders. Hosts tech talks, workshops, mentorship programs, and a beginner''s programming competition.',
    'Diversity in Tech',
    'https://wic.ucsd.edu',
    'https://instagram.com/wicucsd',
    NULL,
    'WIC Board',
    'wic@ucsd.edu'
  ),
  (
    'The Basement UCSD',
    'UCSD''s on-campus startup incubator and accelerator. Provides innovation space, mentorship, prototyping labs, and programs like Blackstone LaunchPad and Innovating for X (i4X) to help student entrepreneurs build companies.',
    'Entrepreneurship',
    'https://thebasement.ucsd.edu',
    'https://instagram.com/ucsdbasement',
    NULL,
    'Jacques Chirazi',
    'basement@ucsd.edu'
  );


-- EVENTS
-- ACM UCSD (club_id = 1)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (1, 'Spring Kickoff', 'ACM''s spring quarter kickoff event. Learn how to get involved through socials, coding workshops, hackathons, and tech talks. Free food and drinks provided.', 'PC East Ballroom', '2026-04-01 18:00:00', '2026-04-01 20:00:00', 'social'),
  (1, 'ACM x Adobe Technical Panel', 'An informational session for Adobe''s SWE internship program. Talk to Adobe software engineers about their experience and go through a technical interview walkthrough.', 'SME ASML Room', '2026-04-07 18:00:00', '2026-04-07 20:00:00', 'panel'),
  (1, 'Arduino UnoQ Workshop by Qualcomm', 'Hands-on workshop featuring Arduino UnoQ, App Lab Development, and Edge Impulse Integration. Learn how to take an AI model from concept to app with live demos from Qualcomm engineers.', 'Qualcomm Conference Center', '2026-04-20 18:00:00', '2026-04-20 20:00:00', 'workshop');

-- ACM AI (club_id = 2)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (2, 'ACM AI Spring Kickoff', 'Meet the ACM AI team, preview hands-on technical workshops, and see what socials are lined up for the quarter. Learn critical AI technologies to spark your next project. Free food included.', 'SME ASML Room', '2026-04-06 18:00:00', '2026-04-06 20:00:00', 'social'),
  (2, 'Agentic AI: Building Automation That Acts', 'Explore how modern AI goes beyond chat. Learn what makes an AI agentic, how agent workflows are structured (goals → plans → actions → feedback), and practical patterns for building reliable automations.', 'Jacobs Room 2315', '2026-04-14 18:00:00', '2026-04-14 19:30:00', 'workshop'),
  (2, 'ACM AI Stellatro AI Competition', 'Train AI bots to choose winning poker hands in this spring AI competition. Open to all experience levels. Prizes include Qualcomm AI Development Kits and Snapdragon X-Elite Laptops.', 'CSE Basement', '2026-05-17 11:00:00', '2026-05-17 18:00:00', 'competition');

-- ACM Cyber (club_id = 3)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (3, 'AI Anarchy', 'Learn about AI security and the weaknesses of modern AI systems. ACM Cyber''s event covering the latest in AI vulnerabilities and security research.', 'Henry Booker Room', '2026-04-08 18:00:00', '2026-04-08 20:00:00', 'workshop'),
  (3, 'San Diego CTF Spring Competition', 'ACM Cyber''s annual 48-hour jeopardy-style Capture the Flag competition open to participants worldwide. No experience required. Work in teams to find flags across cybersecurity challenges.', 'Online + CSE Building', '2026-05-15 18:00:00', '2026-05-17 18:00:00', 'competition'),
  (3, 'Cybersecurity Career Panel', 'Industry professionals from cybersecurity firms discuss career paths, internship opportunities, and how to break into the field. Q&A session included.', 'CSE B225 (Fishbowl)', '2026-04-22 17:00:00', '2026-04-22 19:00:00', 'panel');

-- Triton Robotics (club_id = 4)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (4, 'Robotics Interest Meeting', 'Learn about Triton Robotics, our RoboMaster competition team, open positions, and how to get involved. Open to all experience levels and majors.', 'EBU1 2315', '2026-04-10 18:00:00', '2026-04-10 19:30:00', 'seminar'),
  (4, 'RoboMaster Scrimmage Practice', 'Internal practice session for RoboMaster North America preparation. Watch the team compete in a live scrimmage and learn about the engineering behind our robots.', 'UCSD Warren Mall', '2026-05-02 14:00:00', '2026-05-02 17:00:00', 'workshop'),
  (4, 'Intro to Embedded Systems Workshop', 'Hands-on workshop covering microcontrollers, sensors, and actuators used in competitive robotics. Bring your laptop — no prior experience required.', 'EBU1 Lab', '2026-05-09 15:00:00', '2026-05-09 17:00:00', 'workshop');

-- DS3 (club_id = 5)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (5, 'DataHacks 2026', 'A 36-hour hackathon bringing together 400+ undergraduate and graduate students to tackle real-world challenges in data science, AI, hardware engineering, design, and entrepreneurship.', 'Jacobs School of Engineering', '2026-05-01 18:00:00', '2026-05-03 06:00:00', 'competition'),
  (5, 'Intro to Machine Learning Workshop', 'A beginner-friendly workshop covering the fundamentals of supervised learning, model training, and evaluation using Python and scikit-learn.', 'CSE 1202', '2026-04-16 18:00:00', '2026-04-16 20:00:00', 'workshop'),
  (5, 'Data Science Career Panel', 'Data scientists and analysts from industry share their career journeys, day-to-day work, and advice for breaking into the field. Networking opportunity after the panel.', 'DIB 202', '2026-04-30 17:00:00', '2026-04-30 19:00:00', 'panel');

-- WIC (club_id = 6)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (6, 'WIC x Women''s Center Social', 'A mixer with succulent planting and watching WALL-E! First 20 UCSD student RSVPs get succulent planting and decorating supplies provided.', 'Women''s Center', '2026-04-07 16:00:00', '2026-04-07 18:00:00', 'social'),
  (6, 'Beginner''s Programming Competition', 'An algorithmic problem-solving competition open only to students who have yet to take upper-division CS classes. A great way to practice coding in a low-pressure environment.', 'CSE B225 (Fishbowl)', '2026-05-08 14:00:00', '2026-05-08 17:00:00', 'competition'),
  (6, 'Tech Talk: Women in Industry', 'Professionals from leading tech companies share their experiences as women in computing, career advice, and insights into the industry. Networking and Q&A included.', 'Jacobs Hall 2315', '2026-05-14 17:00:00', '2026-05-14 19:00:00', 'panel');

-- The Basement (club_id = 7)
INSERT INTO events (club_id, name, description, venue, start_time, end_time, event_type)
VALUES
  (7, 'Demo Day 2026', 'The Basement''s annual spring showcase celebrating student innovation. Teams from Blackstone LaunchPad and Innovating for X (i4X) present their startups and projects to the UCSD community.', 'Design and Innovation Building', '2026-05-21 13:00:00', '2026-05-21 17:00:00', 'panel'),
  (7, 'Pitch Practice Night', 'Practice your startup pitch in front of a live audience and get feedback from mentors and peers. Open to all UCSD students with an idea at any stage.', 'The Basement Co-Working Space', '2026-04-23 18:00:00', '2026-04-23 20:00:00', 'workshop'),
  (7, '3D Printing & Prototyping Lab Workshop', 'Introduction to 3D modeling and CAD using OnShape. Learn how to design and print your own prototype using The Basement''s in-house prototyping lab. No prerequisites required.', 'The Basement Prototyping Lab', '2026-05-05 16:00:00', '2026-05-05 18:00:00', 'workshop');
