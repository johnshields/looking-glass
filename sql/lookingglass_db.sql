-- Drop and recreate the database --
DROP DATABASE IF EXISTS lookingglass_db;
CREATE DATABASE lookingglass_db DEFAULT CHARACTER SET = utf8mb4 DEFAULT COLLATE = utf8mb4_general_ci;
USE lookingglass_db;

-- Create the users table --
CREATE TABLE users (
  user_id INT unsigned AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(512) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  role ENUM('user', 'admin') DEFAULT 'user',
  last_login TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert a test user
INSERT INTO users (email, username, password_hash)
VALUES
('user@test.com', 'usertest', '$2b$12$ZrMEn4eN5pl5aQOw.JHn5.K/7Dw7WZs93fplUsfqMPz09ANf6OZFu'),
('john@test.com', 'johntest', 'p4ssword');

-- Session table for login sessions --
CREATE TABLE session
(
    id           VARCHAR(255)        NOT NULL, -- UUID
    user         INT unsigned NOT NULL,
    expire_after INT(8)              NOT NULL, -- Unix epoch time store

    PRIMARY KEY (id),
    FOREIGN KEY (user) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = INNODB;

INSERT INTO session (id, user, expire_after)
VALUES (
  'session-uuid-1234',
  1,
  UNIX_TIMESTAMP() + 3600  -- 1 hour from now
);

-- Create the daily_log table with user_id foreign key --
CREATE TABLE IF NOT EXISTS daily_log (
    id CHAR(36) PRIMARY KEY,
    user_id INT unsigned DEFAULT 1,
    title VARCHAR(100) NOT NULL,
    entries TEXT,
    log_date DATE,
    tags JSON,
    mood VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- Dummy data --
INSERT INTO daily_log (id, user_id, title, entries, log_date, tags, mood)
VALUES
(
    'f12a234c-d45b-11ec-9d64-0242ac120002',
    1,
    'Test Entry',
    '- Tested SQL script.',
    '2025-07-11',
    '["test", "sql", "lookingglass"]',
    'accomplished'
);


COMMIT;