CREATE TABLE IF NOT EXISTS leads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id        TEXT UNIQUE NOT NULL,      -- Google's unique ID, prevents duplicates
    business_name   TEXT NOT NULL,
    industry        TEXT,                       -- Category we searched for
    address         TEXT,
    city            TEXT,
    country         TEXT,
    phone           TEXT,
    website         TEXT,
    google_rating   REAL,
    total_reviews   INTEGER,
    search_query    TEXT,                       -- What query found this lead
    search_location TEXT,                       -- Where we searched
    status          TEXT DEFAULT 'new',         -- new | contacted | qualified | disqualified
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_industry ON leads(industry);
CREATE INDEX IF NOT EXISTS idx_city ON leads(city);
CREATE INDEX IF NOT EXISTS idx_status ON leads(status);