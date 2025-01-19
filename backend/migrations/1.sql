-- Step 1: Create a new table with the updated schema
CREATE TABLE item_temp (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT 0,
    notes TEXT,
    quantity REAL, -- Updated column type
    unit TEXT,
    category_id INTEGER NOT NULL
);

-- Step 2: Copy data from the old table to the new table
INSERT INTO item_temp (id, name, is_active, notes, quantity, unit, category_id)
SELECT id, name, is_active, notes, quantity, unit, category_id
FROM item;

-- Step 3: Drop the old table
DROP TABLE item;

-- Step 4: Rename the new table to the old table's name
ALTER TABLE item_temp RENAME TO item;

-- Step 5: Create the new user table
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    disabled BOOLEAN NOT NULL DEFAULT 0
);

-- if the "version" table does not exist, create it
CREATE TABLE IF NOT EXISTS version (
    id INTEGER PRIMARY KEY,
    version INTEGER NOT NULL
);

-- add version 1 to the "version" table
INSERT INTO version (id, version) VALUES (1, 1);