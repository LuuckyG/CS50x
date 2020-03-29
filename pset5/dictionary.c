// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
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
const unsigned int N = 12345;

// Hash table
node *table[N];

// Words in dictionary
int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Get hashkey of word
    unsigned int key = hash(word);

    // Traverse linked lists at 'key' bucket of hashtable
    node *trav = malloc(sizeof(node));
    trav = table[key];

    while(trav != NULL)
    {
        if (strcasecmp(trav->word, word) == 0)
        {
            free(trav);
            return true;
        }

        trav = trav->next;
    }

    free(trav);

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
//     return (int) tolower(word[0]) - (int) 'a';
// }

    long total = 0;

    // Horner's rule, using polynomial of 11 and ASCII values of lowercased letters
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (word[i] == '\'' )
        {
            total += 11 * total + (int) word[i];
        }
        else
        {
            total += 11 * total + (int) tolower(word[i]);
        }
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
        fclose(file);
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // Initialize word variable
    char word[LENGTH + 1];

    // Scan each word in the dictionary
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
        if (table[key] == NULL)
        {
            table[key] = new_node;
        }
        else
        {
            new_node->next = table[key];
            table[key] = new_node;
        }

        memset(word, 0, sizeof word);
        word_count++;
    }

    // Close dictionary
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Free hashtable
    for (int i = 0; i < N; i++)
    {
        // Traverse linked lists in hashtable
        node *trav = malloc(sizeof(node));
        trav = table[i];

        // Destroy every linked list in hash bucket
        while (trav != NULL)
        {
            node *tmp = trav;
            trav = trav->next;
            free(tmp);
        }

        free(trav);
    }

    return true;
}
