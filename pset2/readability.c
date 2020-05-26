#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>


int coleman_liau(int letters, int words, int sentences);

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    int grade;

    // Get user input
    string text = get_string("Text: ");

    // Count the number of letters, words and sentences in the text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;

        }
        else if (text[i] == ' ')
        {
            words++;
        }
    }

    // Calculate grade based on number of letters, words and sentences
    grade = coleman_liau(letters, words, sentences);

    // Determine the output to the screen based on the grade
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade < 16)
    {
        printf("Grade %i\n", grade);
    }
    else
    {
        printf("Grade 16+\n");
    }

}

int coleman_liau(int letters, int words, int sentences)
{
    // Calculate the Coleman-Liau index for an input text,
    // based on the number of letters, words and sentences in the text.
    float L;
    float S;

    L = ((float) letters / (float) words) * 100;
    S = ((float) sentences / (float) words) * 100;

    return round((0.0588 * L) - (0.296 * S) - 15.8);
}
