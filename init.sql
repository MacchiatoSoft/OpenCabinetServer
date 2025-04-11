create schema main;
CREATE EXTENSION "pgcrypto";

CREATE TABLE main.users (
    user_id UUID PRIMARY KEY UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_name TEXT NOT NULL,
    password TEXT
);


create table main.files(
    file_id UUID PRIMARY KEY UNIQUE DEFAULT gen_random_uuid(),
    owner_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,
    file_dir TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table main.drawers(
    drawer_id UUID PRIMARY KEY UNIQUE DEFAULT gen_random_uuid(),
    owner_id INTEGER NOT NULL,
    drawer_name TEXT NOT NULL,
    drawer_type TEXT NOT NULL,
    drawer_files INTEGER[] NOT NULL
);

-- For test purposes only
INSERT INTO main.users ("user_name", "password") VALUES ('guest', 'guest');
INSERT INTO main.users ("user_name", "password") VALUES ('admin', 'admin');