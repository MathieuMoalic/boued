CREATE TABLE category_new (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    "order" INTEGER UNIQUE
);

INSERT INTO category_new (id, name, "order")
SELECT id, name, id  -- Default value: Assign 'order' values based on 'id'
FROM category;

DROP TABLE category;

ALTER TABLE category_new RENAME TO category;