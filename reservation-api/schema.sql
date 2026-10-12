CREATE TABLE IF NOT EXISTS reservations (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
  reservation_date TEXT NOT NULL,
  reservation_time TEXT NOT NULL,
  guests INTEGER NOT NULL CHECK (guests BETWEEN 1 AND 20),
  message TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  updated_by TEXT
);

CREATE INDEX IF NOT EXISTS reservations_date_idx ON reservations (reservation_date DESC, created_at DESC);

CREATE TABLE IF NOT EXISTS reservation_rate_limits (
  client_hash TEXT NOT NULL,
  window_hour INTEGER NOT NULL,
  count INTEGER NOT NULL,
  PRIMARY KEY (client_hash, window_hour)
);
