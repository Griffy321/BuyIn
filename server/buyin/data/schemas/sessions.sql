-- Sessions and the players in them. Both tables live in the same .db file
-- so SessionPlayers.SessionId can be a real foreign key to Sessions.
--
-- Run on startup by config.run_schema(...). Every statement uses IF NOT EXISTS,
-- so running it again against an existing database does nothing.
--
-- Conventions (same as the Players table):
--   column names are PascalCase      e.g. session_player_id -> SessionPlayerId
--   booleans are INTEGER 0 / 1       SQLite has no real boolean type
--   timestamps are TEXT, ISO 8601 UTC e.g. 2026-11-11T19:30:00+00:00
--   money is INTEGER                 whole amounts, same as SessionPlayer.buyin

CREATE TABLE IF NOT EXISTS Sessions (
    SessionId       TEXT    PRIMARY KEY,
    HostPlayerId    TEXT    NOT NULL,     -- a PlayerId from BuyInPlayer.db (different file, so not a foreign key)
    InitializedAt   TEXT    NOT NULL,
    IsSettled       INTEGER NOT NULL DEFAULT 0 CHECK (IsSettled IN (0, 1)),
    EndedAt         TEXT                  -- null until the session is settled
);

CREATE TABLE IF NOT EXISTS SessionPlayers (
    SessionPlayerId TEXT    PRIMARY KEY,
    SessionId       TEXT    NOT NULL REFERENCES Sessions (SessionId),
    PlayerId        TEXT    NOT NULL,     -- a PlayerId from BuyInPlayer.db (different file, so not a foreign key)
    Buyin           INTEGER NOT NULL,
    JoinedAt        TEXT,
    Status          TEXT,
    IsSettled       INTEGER NOT NULL DEFAULT 0 CHECK (IsSettled IN (0, 1)),
    CashOut         INTEGER,              -- null until the player cashes out
    LeftAt          TEXT                  -- null until the player cashes out
);

-- Looking up everyone in a session is the most common query, so index it.
CREATE INDEX IF NOT EXISTS IX_SessionPlayers_SessionId ON SessionPlayers (SessionId);
