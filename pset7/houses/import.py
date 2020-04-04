import sys
import csv
import cs50


def main():
    """
    Main function that imports data from a CSV spreadsheet and
    puts it into a SQLite database.
    """

    # Check input
    if len(sys.argv) != 2:
        print("Usage: python import.py [filename.csv]")
        sys.exit(1)

    # Create empty database
    open("students.db", "w").close()

    # Open the database for SQlite and initialize values
    db = cs50.SQL("sqlite:///students.db")
    db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

    # Read student database
    with open(sys.argv[-1], "r") as f:

        # Create reader
        reader = csv.DictReader(f, delimiter=',')

        # Iterate through database
        for row in reader:
            names = row['name'].split(' ')

            # Check name
            if len(names) != 3:
                names.insert(1, None)

            # Insert into database
            db.execute("INSERT INTO  students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       names[0], names[1], names[-1], row['house'], int(row['birth']))


if __name__ == '__main__':
    main()
