def main():
    # Get input text
    text = input("Text: ")

    # Count number of letters, words and sentences
    letters = 0
    words = 1
    sentences = 0

    for c in text:
        # print(c)
        if c.isalpha():
            letters += 1
        elif c in '.?!':
            sentences += 1
        elif c == ' ':
            words += 1

    # Get Coleman-Liau index of the input text
    grade = coleman_liau(letters, words, sentences)

    if grade < 1:
        print("Before Grade 1")
    elif grade < 16:
        print(f"Grade {grade}")
    else:
        print("Grade 16+")


def coleman_liau(letters, words, sentences):
    """
    Function to calculate the Coleman-Liau index of a text.
    """
    L = letters / words * 100
    S = sentences / words * 100

    return round((0.0588 * L) - (0.296 * S) - 15.8)


main()
