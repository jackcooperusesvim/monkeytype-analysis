CREATE TABLE tests(
	-- Can index either by the test id or the timestamp
	id TEXT PRIMARY KEY,
	timestamp INTEGER UNIQUE NOT NULL, 
	-- typing quality measurements
	isPb BOOLEAN,
	wpm DECIMAL NOT NULL,
	rawWpm DECIMAL NOT NULL,
	consistency DECIMAL NOT NULL,
	incorrectLetters INTEGER NOT NULL,
	extraLetters INTEGER NOT NULL,
	missed INTEGER NOT NULL,
	-- Behavioral and AFK Detection Fields
	restartCount INTEGER,
	bailedOut BOOLEAN,
	testDuration DECIMAL,
	afkDuration DECIMAL,
	incompleteTestSeconds DECIMAL,
	-- Test Settings
	mode TEXT,
	mode2 TEXT,
	punctuation BOOLEAN,
	numbers BOOLEAN,
	language TEXT,
	difficulty TEXT,
	blindMode BOOLEAN
);

CREATE INDEX timestamp_id ON tests (timestamp);
