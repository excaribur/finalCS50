Symbol	Name	Note	Sector	Resistance	Price	Support	Status

CREATE TABLE stock (
    id  INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    symbol TEXT NOT NULL,
    note TEXT,
    resistance NUMERIC,
    support NUMERIC,
    status TEXT NOT NULL DEFAULT "unfollow",
    user_id int,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    username TEXT NOT NULL, 
                    hash TEXT NOT NULL, 
                    percent NUMERIC NOT NULL DEFAULT 0
                    );
