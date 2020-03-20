#include "helpers.h"
#include <math.h>
#include <stdlib.h>

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
        for (int j = 0; j < width / 2; j++)
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
    // Allocate memory for blurred image
    float blurred_image[height][width][3];

    // Neighbors
    int n = 0;

    // Initialize total RGB values of neighbors
    float avg_values[3];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Set RGB values
            avg_values[0] = 0.0;
            avg_values[1] = 0.0;
            avg_values[2] = 0.0;

            // Calculate total of each color in neighboring pixels
            for (int x = i - 1; x <= i + 1; x++)
            {
                if (x < 0 || x >= height)
                {
                    continue;
                }

                for (int y = j - 1; y <= j + 1; y++)
                {
                    if (y < 0 || y >= width)
                    {
                        continue;
                    }

                    avg_values[0] += image[x][y].rgbtBlue;
                    avg_values[1] += image[x][y].rgbtGreen;
                    avg_values[2] += image[x][y].rgbtRed;
                    n++;
                }
            }

            // Check if averages are not over the maximum of 255.0
            for (int k = 0; k < 3; k++)
            {
                avg_values[k] = (avg_values[k] / (float) n > 255.0) ? 255.0 : round(avg_values[k] / (float) n);
            }

            // Set values in blurred image to average value
            blurred_image[i][j][0] = avg_values[0];
            blurred_image[i][j][1] = avg_values[1];
            blurred_image[i][j][2] = avg_values[2];

            // Reset #neighbors
            n = 0;
        }
    }

    // Copy blurred image onto original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = blurred_image[i][j][0];
            image[i][j].rgbtGreen = blurred_image[i][j][1];
            image[i][j].rgbtRed = blurred_image[i][j][2];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
