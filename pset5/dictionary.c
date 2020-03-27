// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 123456;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
/**
 * Horner's rule for generating a polynomial of 11 using ASCII
 * values of characters as hash function
 *
 * Adapted from:
 * https://www.geeksforgeeks.org/hash-function-for-string-data-in-c-sharp/?ref=rp.
 */
unsigned int hash(const char *word)
{
    long total = 0;
    int n = strlen(word);

    // Horner's rule, using polynomial of 11 and ASCII values
    for (int i = 0; i < n; i++)
    {
        total += 11 * total + (int) word[i];
    }

    // Get modulo of total, based on number of buckets in hash table
    total = total % N;

    if (total < 0)
    {
        total += N;
    }

    return (int) total;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // Create hashtable with nodes, initialize as NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // Scan each word in the dictionary
    char *word = NULL;

    while (fscanf(file, "%s", word) != EOF)
    {
        // Create node
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            unload();
            free(new_node);
            fclose(file);
            return false;
        }

        strcpy(new_node->word, word);
        new_node->next = NULL;

        // Hash input
        unsigned int key = hash(word);

        // Insert into the hashtable
        new_node->next = table[key];
        table[key] = new_node;
        free(new_node);
    }

    // Close dictionary
    fclose(file);
    free(word);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Free hashtable
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i]->next;

        // Destroy every linked list in hash bucket
        while (table[i] != NULL)
        {
            free(table[i]);
            table[i] = tmp;
        }

        free(tmp);
    }

    // Check if final element is correctly removed
    if (table[N-1] == NULL)
    {
        return true;
    }

    return false;
}
