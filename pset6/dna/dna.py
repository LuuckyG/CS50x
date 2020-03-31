import re
import csv
import sys


def main():
    """
    Main function to find longest consecutive repeating STR sequences in full DNA sequence
    """

    # Check command-line input
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Load DNA sequence
    with open(sys.argv[2], "r") as file:
        dna = file.readline()

    # Open database
    with open(sys.argv[1], newline='') as database:

        # Initialize
        reader = csv.reader(database)
        line_count = 0
        STR_count = []

        # Check if found repeats match with someone in database
        for row in reader:

            # Header of csv file
            if line_count == 0:
                # Check DNA on STR sequences
                for dna_segment in row[1:]:
                    repeats = find_repeats(dna_segment, dna)
                    STR_count.append(str(repeats))

            # Rest of csv
            else:
                if row[1:] == STR_count:
                    return row[0]

            # Update
            line_count += 1

    return "No match"


def find_repeats(substring, string):
    """
    Function to find longest consecutive repeats of substring in main string.
    """

    # Initialize
    repeats = 0
    longest_repeat = 1
    last_repeat = None

    # Find all occurances of the substring (STR) in whole string (DNA)
    for term in re.finditer(substring, string):

        # Set first repeat
        if last_repeat is None:
            last_repeat = term.end()

        # Check if substring is directly after last substring
        if last_repeat == term.start():
            repeats += 1
            last_repeat = term.end()
            if repeats > longest_repeat:
                longest_repeat = repeats
        else:
            # Reset repeat index
            repeats = 1
            last_repeat = term.end()

    return longest_repeat


print(main())
