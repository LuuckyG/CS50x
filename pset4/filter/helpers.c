#include "helpers.h"
#include <math.h>

void swap(RGBTRIPLE *left, RGBTRIPLE *right);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00);

            // Set all channels equal to this average
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Swap pixels
void swap(RGBTRIPLE *left, RGBTRIPLE *right)
{
    RGBTRIPLE tmp = *left;
    *left = *right;
    *right = tmp;
}


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // Only loop untill middle is reached
        for (int j = 0; j < width/2; j++)
        {
            // Swap left with right side of image
            swap(&image[i][j], &image[i][(width - 1) - j]);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create image with blurred intensities
    RGBTRIPLE blurred_image[height][width];

    float neighbors = 9.00;

    int x_min;
    int x_max;
    int y_min;
    int y_max;

    for (int i = 0; i < height; i++)
    {
        // Determine boundaries based on row
        if (i == 0)
        {
            y_min = i;
            neighbors -= 3.00;
        }
        else if (i == height - 1)
        {
            y_max = height;
            neighbors -= 3.00;
        }
        else
        {
            y_min = i - 1;
            y_max = i + 1;
        }

        for (int j = 0; j < width; j++)
        {
            // Determine boundaries based on column
            if (j == 0)
            {
                x_min = j;
                neighbors -= 3.00;
            }
            else if (j == width - 1)
            {
                x_max = width;
                neighbors -= 3.00;
            }
            else
            {
                x_min = j - 1;
                x_max = j + 1;
            }

            // Initialize total RGB values of neighbors
            int total_blue = 0;
            int total_green = 0;
            int total_red = 0;

            // Calculate total of each color in neighboring pixels
            for (int x = x_min; x < x_max; x++)
            {
                for (int y = y_min; y < y_max; y++)
                {
                    total_blue += image[y][x].rgbtBlue;
                    total_green += image[y][x].rgbtGreen;
                    total_red += image[y][x].rgbtRed;
                }
            }

            // Set values in blurred image to average value by dividing total by #neighbors
            blurred_image[i][j].rgbtBlue = round(total_blue / neighbors);
            blurred_image[i][j].rgbtGreen = round(total_green/ neighbors);
            blurred_image[i][j].rgbtRed = round(total_red/ neighbors);

            // Reset #neighbors
            neighbors = 9.00;
        }
    }

    // Copy blurred image onto original image
    image = blurred_image;

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
