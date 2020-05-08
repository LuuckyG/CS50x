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
        dna = file.read()

    # Open database
    with open(sys.argv[1], newline='') as database:

        # Initialize
        STR_count = []
        reader = csv.reader(database)
        header = next(reader)
        
        if header != None:
            # Check DNA on STR sequences
            for dna_segment in header[1:]:
                repeats = find_repeats(dna_segment, dna)
                STR_count.append(str(repeats))       

            # Check if found repeats match with someone in database
            for row in reader:
                if row[1:] == STR_count:
                    return row[0]
                
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


if __name__ == '__main__':
    print(main())
