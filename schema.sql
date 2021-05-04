CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT not null,
    start_date TEXT not null,
    end_date TEXT not null,
    lectures INTEGER not null
);