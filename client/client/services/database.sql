
-- CREATE TABLE IF NOT EXISTS sponsor (
--  id               INTEGER PRIMARY KEY AUTOINCREMENT,
--  name             TEXT NOT NULL
--);

CREATE TABLE IF NOT EXISTS competition (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  sponsor          TEXT NOT NULL,
  name             TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS driver (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  name             TEXT NOT NULL,
  suranme          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS race_type (
  name             TEXT PRIMARY KEY,
  ru_text          TEXT
);

CREATE TABLE IF NOT EXISTS race (
  -- Attributes
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  competition_id   INTEGER NOT NULL,
  race_type        TEXT    NOT NULL,
  started_at         INTEGER NOT NULL,
  finish_at        INTEGER DEFAULT NULL,
  data             TEXT,

  -- F.K.
  FOREIGN KEY(race_type) REFERENCES race_type(name)
);

CREATE TABLE IF NOT EXISTS driver_has_race (
  -- Attributes
  driver_id        INTEGER NOT NULL,
  race_id          INTEGER NOT NULL,
  PRIMARY KEY(driver_id, race_id),
  -- F.K.
  FOREIGN KEY(driver_id) REFERENCES driver(id),
  FOREIGN KEY(race_id) REFERENCES race_type(race_id)
);
