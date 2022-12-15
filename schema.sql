Symbol	Name	Note	Sector	Resistance	Price	Support	Status

CREATE TABLE stock (
    id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    symbol TEXT NOT NULL,
    note TEXT NOT NULL,
    resistance NUMERIC,
    support NUMERIC,
    status TEXT NOT NULL DEFAULT "prepare"
);


INSERT INTO stock (symbol, note)
            VALUES ("D",
             "ooooo oooooo ooooo oooooo oooooo ooooo");

