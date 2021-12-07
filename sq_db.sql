/*
Для динамического меню(header) потом
CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
login text NOT NULL,
password text NOT NULL
);
*/

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name txt NOT NULL,
email text NOT NULL,
password text NOT NULL,
time integer NOT NULL
);
