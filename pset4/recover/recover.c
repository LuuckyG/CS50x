#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

bool check_byte(uint8_t b);

int main(int argc, char *argv[])
{
    int BUFFERSIZE = 512;
    uint8_t *bytes = malloc(BUFFERSIZE);

    // Check input
    if (argc != 2)
    {
        printf("Usage: ./recover [filename] \n");
        return 1;
    }

    char *fname = argv[1];

    // Open input file
    FILE *inptr = fopen(fname, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", fname);
        return 1;
    }

    // Number of JPEG images in memory
    int i = 0;

    // Create output file and filename
    FILE *outptr = NULL;
    char outfile[7];

    // Read blocks of 512 bytes of memory from input file
    while (fread(bytes, BUFFERSIZE, 1, inptr))
    {
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && check_byte(bytes[3]))
        {

            // Close any open file
            if (outptr != NULL)
            {
                fclose(outptr);

                // Increase number of found JPEG images
                i++;
            }

            // Define output filename
            sprintf(outfile, "%03d.jpg", i);

            // Open output file
            outptr = fopen(outfile, "w");

        }

        // Write to output file
        if (outptr != NULL)
        {
            fwrite(bytes, sizeof(uint8_t), BUFFERSIZE, outptr);
        }

    }

    // Close last output file
    if (outptr != NULL)
    {
        fclose(outptr);
    }

    // Close input file
    fclose(inptr);

    // Free allocated memory
    free(bytes);

    return 0;
}

bool check_byte(uint8_t b)
{
    unsigned char bits[16] = {0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef};

    for (int i = 0; i < 16; i++)
    {
        if (b == bits[i])
        {
            return true;
        }
    }

    return false;
}
