// Program to check credit card number according to Luhn's Algorithm

#include <cs50.h>
#include <stdio.h>

int checksum(long x);
int checklen(long x);

int main(void)
{
    int sum;
    long number;
    int card_length;
    int first_two_digits;
    int first_digit;

    number = get_long("Number: ");
    sum = checksum(number);
    card_length = checklen(number);
    
    // Make cardnumber smaller, such that modulo 10 and modulo 100 give first and first two digits
    for (int i = 2; i < card_length; i++)       
    {
        number = number / 10;
    }

    first_digit = (number / 10) % 10;
    first_two_digits = number % 100; 

    // Check if card length and first (two) digits match any of the card companies
    if ((sum % 10) != 0)
    {
        printf("INVALID\n");
    }
    else if (card_length == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        printf("AMEX\n");
    }
    else if (card_length == 16 && (first_two_digits > 50 && first_two_digits < 56))  // 51, 52, 53, 54, 55
    {
        printf("MASTERCARD\n");
    }
    else if ((card_length == 13 || card_length == 16) && first_digit == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}

int checksum(long x)
{
    // Function to check credit card number following Luhn's Algorithm
    // Returns 1 (true) if correct, 0 (false) if incorrect

    int value;
    int sum = 0;

    for (int i = 0; ; i++)
    {
        value = x % 10;

        if (i % 2 == 1)
        {
            // Add the products digits to result
            value *= 2;

            if (value >= 10)
            {
                // Remove 10 to get second digit, add back 1 for first digit --> equal to -9
                value -= 9; 
            }

            sum += value;
        } 
        else
        {
            // Just add the digit itself
            sum += value;
        }

        x = x / 10;
        
        // We have checked all numbers, return result
        if (x < 1)  
        {
            return sum;
        }
    }
}

int checklen(long x)
{
    // Function to get length of credit card number
    int length = 0;

    while (x > 1)
    {
        x = x / 10;
        length += 1;
    }

    return length;
}
