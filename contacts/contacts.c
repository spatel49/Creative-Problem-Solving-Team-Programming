/*******************************************************************************
 * Name        : contacts.c
 * Author      : Yakov Kazinets, Abderahim Salhi, Siddhanth Patel
 * Date        : 2/19/21
 * Description : Solving HackerRank contacts problem.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_LENGTH 26
#define OPERATION_BUF_SIZE 7 /* Large enough to cover the word 'search' and '\0' */
#define NAME_BUF_SIZE 22

/* Basic trie node -- also, keep track of number of nodes below this one. */

typedef struct node
{
    int prefix_count;
    /* Allocate +1 for the the pointer to the end-of-string marker. 
       Needed for the search feature. */
    struct node *children[ALPHABET_LENGTH + 1];
} trie_node;

// recursive function to free all memory allocated by all nodes
void node_delete(trie_node *root)
{
    if (root)
    {
        // for each child
        for (int i = 0; i < ALPHABET_LENGTH; ++i)
        {
            // recursively delete this child
            if (root->children[i])
                node_delete(root->children[i]);
        }
        // after all children have been deleted, delete parent
        free(root);
    }
}

// put the word into the "trie", given as root node
void add_word_to_trie(char *word, trie_node *root)
{
    // counter at the root node contains the total of all added words
    root->prefix_count += 1;

    // iterate word letter-by-letter
    while (*word)
    {
        int i = *word - 'a'; // index of the children

        // create new node if does not exist yet
        if (root->children[i] == NULL)
        {
            root->children[i] = (trie_node *)calloc(1, sizeof(trie_node));
        }
        // update prefix counter
        root->children[i]->prefix_count += 1;

        // go to next node
        root = root->children[i];
        // go to next letter
        ++word;
    }
    // mark this node as "word" by assigning non-NULL value

    root->children[ALPHABET_LENGTH] = root;
}
// find the number of words that start with the prefix in the "trie", given as root node
int find_prefix_count(char *prefix, trie_node *root)
{
    // iterate prefix letter-by-letter
    while (*prefix)
    {
        int i = *prefix - 'a'; // index of the children
        if (root->children[i] == NULL)
            return 0; // not found

        // go to next node
        root = root->children[i];
        // go to next letter
        ++prefix;
    }
    return root->prefix_count;
}

// search the word in the "trie", given as root node
// return 1 if the trie contains the word and 0 otherwise.
int search_word_in_trie(char *word, trie_node *root)
{
    // iterate word letter-by-letter
    while (*word)
    {
        int i = *word - 'a'; // index of the children
        if (root->children[i] == NULL)
            return 0; // not found

        root = root->children[i];
        // go to next letter
        ++word;
    }

    if (root->children[ALPHABET_LENGTH] != NULL)
        return 1; // found
    return 0;     // not found
}

int main()
{
    char operation[OPERATION_BUF_SIZE]; // buffer for reading operation
    char name[NAME_BUF_SIZE];           // buffer for reading name (word or prefix)
    int row, nRows;

    // read number of rows in the input
    fscanf(stdin, "%d", &nRows);

    // create empty root node of the trie
    trie_node *root = (trie_node *)calloc(1, sizeof(trie_node));

    // read and parse input
    for (row = 0; row < nRows; ++row)
    {
        fscanf(stdin, "%s %s", operation, name);

        // perform operation
        if (strcmp(operation, "add") == 0)
        {
            add_word_to_trie(name, root);
        }
        else if (strcmp(operation, "find") == 0)
        {
            printf("%d\n", find_prefix_count(name, root));
        }
        else if (strcmp(operation, "search") == 0)
        {
            printf("%s\n", search_word_in_trie(name, root) ? "yes" : "no");
        }
    }

    // free all memory allocated by the trie
    node_delete(root);

    return 0;
}
