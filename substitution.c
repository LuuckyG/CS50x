// Program that takes in a key of 26 alphabetic characters and a plain text
// and converts this plain text to a cipher text using the given key.

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


int main(int argc, string argv[])
{
    // Function that encyphers messages using a substitution cipher

    // Create ascii array that will look for ascii codes of uppercased alphabetic letters
    int ascii_array[26] = {0};

    // Check for correctness of input
    // Input should contain 1 cmd line argument, which is the key.
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        // Check whether the key contains only alphabetic characters,
        // and if each alphabetic character only exists once in the key.

        char *key = argv[1];

        for (int i = 0; i < strlen(key); i++)
        {
            if (!isalpha(key[i]))
            {
                printf("All characters in the key should be alphabetic.\n");
                return 1;
            }

            // Check for dublicates
            int c = (int) toupper(key[i]);

            ascii_array[c - 65]++;

            if (ascii_array[c - 65] > 1)
            {
                printf("Key contains dublicate values\n");
                return 1;
            }
        }

        // Get plain input text
        char *plaintext = get_string("plaintext: ");

        printf("ciphertext: ");

        // Convert plain text to enciphered text using the key
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {

            // If not alphabetic char, print original char
            if (!isalpha(plaintext[i]))
            {
                printf("%c", plaintext[i]);
                continue;
            }

            // Calculate offset to change original char to cipher char
            int ascii_offset = isupper(plaintext[i]) ? 65 : 97;

            // Determine enciphered ciphertext
            char cipher = key[(int) plaintext[i] - ascii_offset];

            // Check if input text is upper or lower case
            if (islower(plaintext[i]))
            {
                printf("%c", tolower(cipher));
            }
            else
            {
                printf("%c", toupper(cipher));
            }
        }

        printf("\n");
        return 0;
    }
}
