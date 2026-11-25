
CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    balance NUMERIC(10, 2) NOT NULL
);

INSERT INTO accounts (id, name, balance)
VALUES
    (1, 'Arun', 10000),
    (2, 'Priya', 5000)
ON CONFLICT (id)
DO UPDATE SET
    name = EXCLUDED.name,
    balance = EXCLUDED.balance;


SELECT * FROM accounts;
