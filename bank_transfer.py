
import psycopg2


# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="",
    port="5432"
)


# Function to transfer money
def transfer(from_id, to_id, amount, force_failure=False):

    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    # Start a transaction
    with conn:

        with conn.cursor() as cur:

            # Debit money from the sender
            cur.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE id = %s AND balance >= %s
                """,
                (amount, from_id, amount)
            )

            # Check whether the sender has enough money
            if cur.rowcount != 1:
                raise ValueError("Insufficient balance or account not found")

            # Force an error after debit for testing
            if force_failure:
                raise RuntimeError("Forced failure after debit")

            # Credit money to the receiver
            cur.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE id = %s
                """,
                (amount, to_id)
            )

            # Check whether the receiver exists
            if cur.rowcount != 1:
                raise ValueError("Receiver account not found")


# Function to show account balances
def show_balances():

    with conn.cursor() as cur:

        cur.execute(
            "SELECT name, balance FROM accounts ORDER BY id"
        )

        rows = cur.fetchall()

        for row in rows:
            print(row[0], ":", row[1])


try:

    # Normal transfer
    print("Normal transfer: 2000")

    transfer(1, 2, 2000)

    show_balances()

    print("\nTesting rollback")

    # Force an error after debit
    try:
        transfer(1, 2, 1000, force_failure=True)

    except RuntimeError as e:
        print("Error:", e)

    # Balances should remain unchanged
    print("Balances after rollback:")
    show_balances()

    print("\nTesting insufficient balance")

    # Arun does not have 20000
    try:
        transfer(1, 2, 20000)

    except ValueError as e:
        print("Error:", e)

    # Balances should remain unchanged
    print("Balances after insufficient balance:")
    show_balances()

finally:
    conn.close()
