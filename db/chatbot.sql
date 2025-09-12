-- Active: 1757557610145@@172.20.0.2@5432@chatbot_db@public

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Insert a dummy user with a bcrypt password (matches your earlier one)
INSERT INTO users (email, password)
VALUES (
  'test@example.com',
  '$2a$10$E6mJ9O.Yeje8TokTs6UjKOrX.YbAELdpXfUdj.L.0HfCygsVcLcze'
)
ON CONFLICT (email) DO NOTHING;