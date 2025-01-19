-- if the "version" table does not exist, create it
CREATE TABLE IF NOT EXISTS version (
    id INTEGER PRIMARY KEY,
    version INTEGER NOT NULL
);

INSERT INTO version (id, version) VALUES (1, 1);

-- delete alembic_version table
DROP TABLE IF EXISTS alembic_version;