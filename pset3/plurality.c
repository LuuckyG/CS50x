#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
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
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        // Check for given name in candidate list
        if (strcmp(name, candidates[i].name) == 0)
        {
            // When name is found
            candidates[i].votes++;
            return true;
        }
    }

    // When name is not found
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // If there is only one candidate, he/she is automatically
    // the winner.
    if (candidate_count == 1)
    {
        printf("%s\n", candidates[0].name);
        return;
    }
    else if (candidate_count == 2)
    {
        // If there are two candidates, just compare the two vote counts.
        if (candidates[0].votes == candidates[1].votes)
        {
            printf("%s\n", candidates[0].name);
            printf("%s\n", candidates[1].name);
        }
        else if (candidates[0].votes > candidates[1].votes)
        {
            printf("%s\n", candidates[0].name);
        }
        else
        {
            printf("%s\n", candidates[1].name);
        }
        return;
    }

    // If more candidates, we need to sort the candidates on votes
    candidate tmp[1];

    // Sort candidates on votes (using bubble sort) in DESCENDING order
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (candidates[i].votes < candidates[j].votes)
            {
                // Make temporary candidate
                tmp[0].name = candidates[i].name;
                tmp[0].votes = candidates[i].votes;

                // Swap candidates
                candidates[i] = candidates[j];
                candidates[j] = tmp[0];
            }
        }
    }

    int most_votes = 0;

    // Check votes of candidates
    // When votes is less than max, break out of loop
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes >= most_votes)
        {
            most_votes = candidates[i].votes;
            printf("%s\n", candidates[i].name);
        }
        else
        {
            return;
        }
    }
}
