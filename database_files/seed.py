import csv
import asyncio
import asyncpg

async def main():
    # Connect to the database
    conn = await asyncpg.connect(
        database="postgres",
        user="postgres",
        password="Postgres7981",
        host="group-5-p2-db.c76rpf8ygv4l.us-east-1.rds.amazonaws.com",
        port="5432"
    )

    # Delete all rows from tables
    await conn.execute("DELETE FROM rating;")
    await conn.execute("DELETE FROM book;")
    await conn.execute("DELETE FROM author;")

    # Insert authors
    with open("database_files/authors.csv", 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            row[0] = row[0][9:-1]
            await conn.execute(
                "INSERT INTO author (openlibrary_key, name) VALUES ($1, $2)",
                row[0], row[1]
            )
    print("authors.csv done")

    # Insert books
    with open("database_files/books.csv", 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            row[0] = row[0][7:-1]
            row[1] = row[1][9:-1]
            author_id = await conn.fetchval(
                "SELECT id FROM author WHERE openlibrary_key = $1",
                row[1]
            )
            author_id = int(author_id)
            await conn.execute(
                "INSERT INTO book (openlibrary_key, author_id, title, description) VALUES ($1, $2, $3, $4)",
                row[0], author_id, row[2], row[3]
            )
    print("books.csv done")
    # Insert ratings
    with open("database_files/ratings.csv", 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            row[0] = row[0][7:-1]
            book_id = await conn.fetchval(
                "SELECT id FROM book WHERE openlibrary_key = $1",
                row[0]
            )
            book_id = int(book_id)
            row[1] = int(row[1])
            await conn.execute(
                "INSERT INTO rating (book_id, score) VALUES ($1, $2)",
                book_id, row[1]
            )
    print("ratings.csv done")

    # Close the connection
    await conn.close()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
