CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  role TEXT NOT NULL,
  password TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'alice', 'alice@example.test', 'user', 'Password123!');
INSERT INTO users VALUES (2, 'bob', 'bob@example.test', 'admin', 'Admin123!');
INSERT INTO users VALUES (3, 'charlie', 'charlie@example.test', 'user', 'letmein');
