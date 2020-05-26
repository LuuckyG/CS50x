#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
int preference(int n);
void swap(int i, int j);
int partition(int low, int high);
void quick_sort(int low, int high);
void sort_pairs(void);
bool check_cycle(int n, int m);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        // Check for given name in candidate list
        if (strcmp(name, candidates[i]) == 0)
        {
            // When name is found
            ranks[rank] = i;
            return true;
        }
    }

    // When name is not found
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Loop over given ranks
    for (int i = 0; i < candidate_count; i++)
    {
        // Calculate preference compared to other candidates
        for (int j = candidate_count; j > i; j--)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Loop over given ranks
    for (int i = 0; i < candidate_count; i++)
    {
        // Only look at bottom half of preference matrix.
        for (int j = 0; j < candidate_count; j++)
        {
            // Skip diagonal
            if (i == j)
            {
                break;
            }
            // Create pair, if it is not a tie
            else if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Helper function to calculate preference for winner of pair
int preference(int n)
{
    return preferences[pairs[n].winner][pairs[n].loser];
}

// Helper function to swap two elements in pairs array
void swap(int i, int j)
{
    pair tmp = pairs[i];
    pairs[i] = pairs[j];
    pairs[j] = tmp;
}

// Find pivot point index of the array
int partition(int low, int high)
{
    // Index of smaller element
    int i = low - 1;

    int pivot = preference(high);

    for (int j = low; j < high; j++)
    {
        // Swap if preference is of i'th element is smaller than current pivot
        // Sort in DESCENDING order
        if (preference(j) > pivot)
        {
            i++;
            swap(i, j);
        }
    }

    swap(i + 1, high);

    return i + 1;
}

// Implementation of quick sort sorting algorithm
void quick_sort(int low, int high)
{
    if (low < high)
    {
        int pivot = partition(low, high);

        // Left half of array
        quick_sort(low, pivot - 1);

        // Right half of array
        quick_sort(pivot + 1, high);
    }

    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // No pairs or no need for sorting
    if (pair_count == 0 || pair_count == 1)
    {
        return;
    }

    // Sort using quick sort
    quick_sort(0, pair_count - 1);

    return;
}

bool check_cycle(int n, int m)
{
    if (locked[m][n])
    {
        return true;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[i][n])
        {
            return check_cycle(i, m);
        }
    }

    return false;
}


// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Set first locked pair
    if (pair_count > 0)
    {
        locked[pairs[0].winner][pairs[0].loser] = true;
    }

    bool cycle;

    for (int i = 1; i < pair_count; i++)
    {
        // Check for cycle in graph
        cycle = false;
        if (check_cycle(pairs[i].winner, pairs[i].loser))
        {
            cycle = true;
            continue;
        }

        // If the edge does not create cycle, create edge
        if (!cycle)
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    bool winner = true;

    // Winner is column in locked with only false elements
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                winner = false;
                break;
            }
        }

        // Print winner
        if (winner)
        {
            printf("%s\n", candidates[i]);
            return;
        }

        // Reset condition
        winner = true;
    }
    return;
}
