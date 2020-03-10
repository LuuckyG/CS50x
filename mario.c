// Program that prints out a pyramid from the Mario game of a height specified by the user

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height; 

    do 
    {
        // Get input
        height = get_int("Height: ");
    } 
    // check correctness input
    while (height < 1 || height > 8);
    
    // Run loop until height (inclusive) is reached
    for (int i = 1; i <= height; i++)
    {        
        
        for (int j = 0; j < height; j++)       
        {   
            // Print left side of pyramid
            if (j < (height - i)) 
            {
                printf(" ");
            }
            else 
            {
                printf("#");
            }
        }

        // Print gap
        printf("  ");

        // Print right side of pyramid
        for (int j = 0; j < i; j++)        
        {
            printf("#");
        }

        printf("\n");
    }
}
