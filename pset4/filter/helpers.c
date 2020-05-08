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
    float(*blurred_image)[width][3] = calloc(height, 3 * width * sizeof(float));

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
    
    free(blurred_image);
    
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Horizontal and vertical filters
    int filter_x[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int filter_y[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};

    // Placeholders for Gx and Gy values
    float Gx[3];
    float Gy[3];
    float squared[3];

    // Allocate memory for edge filtered image
    float(*edge_image)[width][3] = calloc(height, 3 * width * sizeof(float));

    // Initialize neighbors
    int n = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Set Gx and Gy values
            Gx[0] = Gy[0] = 0.0;
            Gx[1] = Gy[1] = 0.0;
            Gx[2] = Gy[2] = 0.0;

            squared[0] = 0.0;
            squared[1] = 0.0;
            squared[2] = 0.0;

            // Calculate total of each color in neighboring pixels
            for (int x = i - 1; x <= i + 1; x++)
            {
                // Add a zero (equal to doing nothing but adding an 'imaginary' neighbor)
                if (x < 0 || x >= height)
                {
                    n = n + 3;
                    continue;
                }

                for (int y = j - 1; y <= j + 1; y++)
                {
                    if (y < 0 || y >= width)
                    {
                        n++;
                        continue;
                    }

                    // Compute Gx using x-filter
                    Gx[0] += image[x][y].rgbtBlue * filter_x[n];
                    Gx[1] += image[x][y].rgbtGreen * filter_x[n];
                    Gx[2] += image[x][y].rgbtRed * filter_x[n];

                    // Compute Gy using y-filter
                    Gy[0] += image[x][y].rgbtBlue * filter_y[n];
                    Gy[1] += image[x][y].rgbtGreen * filter_y[n];
                    Gy[2] += image[x][y].rgbtRed * filter_y[n];

                    n++;
                }
            }

            // Check if squared pixel values are not over the maximum of 255.0
            for (int k = 0; k < 3; k++)
            {
                squared[k] = round(sqrtf(pow(Gx[k], 2) + pow(Gy[k], 2))) > 255.0 ? 255.0 : round(sqrtf(pow(Gx[k], 2) + pow(Gy[k], 2)));
            }

            // Set values in edge image to rounded values of (Gx^2 + Gy^2) ^ 0.5
            edge_image[i][j][0] = squared[0];
            edge_image[i][j][1] = squared[1];
            edge_image[i][j][2] = squared[2];

            // Reset neighbors
            n = 0;
        }
    }

    // Copy edge filtered image onto original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = edge_image[i][j][0];
            image[i][j].rgbtGreen = edge_image[i][j][1];
            image[i][j].rgbtRed = edge_image[i][j][2];
        }
    }
    
    free(edge_image);
    
    return;
}
