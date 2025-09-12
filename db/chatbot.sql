-- Active: 1756880765923@@dpg-d2rrovp5pdvs73eckql0-a.ohio-postgres.render.com@5432@todo_huws@public

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_users (
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

-- Insert a dummy user with a bcrypt password (matches your earlier one)
INSERT INTO chat_users (email, password)
VALUES (
  'test@example.com',
  '$2a$10$E6mJ9O.Yeje8TokTs6UjKOrX.YbAELdpXfUdj.L.0HfCygsVcLcze'
)