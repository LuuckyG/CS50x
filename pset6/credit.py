def main():
    # Get user input (assume correct input)
    card_nr = input("Number: ")

    length = len(card_nr)
    if length not in [13, 15, 16]:
        return "INVALID"

    card_sum = check_sum(card_nr)

    # Check sum of card number
    if card_sum % 10 != 0:
        return "INVALID"

    # Determine credit card provider
    if (length == 15) and (card_nr[:2] == '34' or card_nr[:2] == '37'):
        return "AMEX"
    elif length == 16 and card_nr[:2] in ['51', '52', '53', '54', '55']:
        return "MASTERCARD"
    elif (length == 13 or length == 16) and (card_nr[0] == '4'):
        return "VISA"
    else:
        return "INVALID"


def check_sum(card_nr):
    """
    Function to calculate sum of card number digits,
    based on Luhn’s algorithm.
    """
    result = 0

    # Traverse the credit card number in reversed order
    for i, digit in enumerate(card_nr[::-1]):
        # Change string input to integer
        digit = int(digit)

        # Check location of digit in number
        if i % 2 == 1:
            digit *= 2

            # Get remainder and add 1
            # If digit = 12 --> total + 1 and total + 2 --> total + 3
            if digit >= 10:
                digit -= 9

        result += digit

    return result


print(main())
