-- Intentionally insecure database design for SQL/security scanning exercises.
CREATE TABLE app_users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password_plaintext VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'user'
);

INSERT INTO app_users (id, username, password_plaintext, role)
VALUES
    (1, 'alice', 'Password123!', 'user'),
    (2, 'admin', 'Admin123!', 'admin');

-- Overly broad grant; syntax is illustrative and scanner-oriented.
GRANT ALL PRIVILEGES ON app_users TO PUBLIC;
