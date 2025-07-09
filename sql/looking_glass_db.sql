-- Drop and recreate the database
DROP DATABASE IF EXISTS looking_glass;
CREATE DATABASE looking_glass DEFAULT CHARACTER SET = utf8mb4 DEFAULT COLLATE = utf8mb4_general_ci;
USE looking_glass;

-- Create the daily_log table
CREATE TABLE IF NOT EXISTS daily_log (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    entries TEXT,
    log_date DATE,  -- actual date being logged about
    tags JSON,
    mood VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- Dummy data
INSERT INTO daily_log (id, title, entries, log_date, tags, mood)
VALUES
(
    'f12a234c-d45b-11ec-9d64-0242ac120002',
    'Monday Entry',
    '- Worked on the API setup today.',
    '2025-07-07',
    '["work", "api", "python"]',
    'productive'
),
(
    'a02c8b7e-d45c-11ec-9d64-0242ac120002',
    'Tuesday Entry',
    '- Connected API to MySQL.',
    '2025-07-08',
    '["learning", "sql"]',
    'chill'
);

COMMIT;