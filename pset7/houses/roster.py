import sys
import sqlite3


def main():
    """
    Main function that prints a list of students
    for a given house in alphabetical order.
    """

    # Check input
    if len(sys.argv) != 2:
        print("Usage: python roster.py [house]")
        sys.exit(1)

    # Set the house to be searched
    house = sys.argv[-1]

    # Open the database for SQlite
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Query
    query = "SELECT first, middle, last, birth \
               FROM students \
              WHERE house=? \
              ORDER BY last ASC, first;"

    cursor.execute(query, (house,))

    # Fetch and print result
    result = cursor.fetchall()

    # Row contains: first, middle, last, birth
    for row in result:
        if not row[1]:
            print(f"{row[0]} {row[2]}, born {row[3]}")
        else:
            print(f"{row[0]} {row[1]} {row[2]}, born {row[3]}")

    # Close connection
    conn.close()


if __name__ == '__main__':
    main()
