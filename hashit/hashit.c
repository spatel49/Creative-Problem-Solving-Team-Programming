/*******************************************************************************
 * Name        : hashit.c
 * Author      : Yakov Kazinets, Abderahim Salhi, Siddhanth Patel
 * Date        : 03/16/21
 * Description : Solving SPOJ Hash it! problem.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>


#define TABLE_SIZE 101
#define MAX_INPUT_SIZE 20 //ADD or DEL and : then followed by max string size of 15
char *myArray[TABLE_SIZE];

typedef struct {
    char* keys[TABLE_SIZE];
    int num_keys;
} hash_set;

int hash(char *key){ //creates the hash
    char * t; // create new pointer to assign to key
    int index = 1;
    int finalint = 0;
    for (t = key; *t != '\0'; t++) {
        finalint = finalint + (((int) *t) * index);
        index++;
    }

    return (19*finalint) % TABLE_SIZE;
}

int insert_key(hash_set *set, char *key){ //inserts the key specified
		int hkey = hash(key);
		if (hkey >= 0){
			int tempj = 0;
			int tempy = 0;
			while (tempj < 20){
				if (set->keys[tempy] != NULL){
					if (strcmp(set->keys[tempy],key) != 0){
						tempy = (hkey + (tempj*tempj) + (23*tempj)) % 101;
						tempj++;
					} else {
						break;
					}
					tempj++;
				} else {
					tempy = (hkey + (tempj*tempj) + (23*tempj)) % 101;
					tempj++;
				}
			}
			if (set->keys[tempy] != NULL){
		        return 0;
		    }
		}
        char copykey[strlen(key)];
        for(int i = 0; i < strlen(key); i++){
            copykey[i] = key[i];
        }
        copykey[strlen(key)] = '\0';
        int j =0;
        int y = hkey;
        while (j<20){
        	if (j != 0){
        		y = (hkey + (j*j) + (23*j)) % 101;
        	}
            if(set->keys[y] == NULL){
            	set->keys[y] = malloc(sizeof(char) * (strlen(copykey) + 1));
            	strcpy(set->keys[y],copykey);
                set->num_keys +=1;
                return 0;
            } else {
                if (strcmp(set->keys[y],copykey) == 0){
                    return 0;
                } else {
                    j++;
                }
            }
        }
        return 0;
}

int delete_key(hash_set *set, char *key){ //deletes the key specified
	int hkey = hash(key);
	int y = hkey;
	int j = 0;
	while (j<20){
		if (set->keys[y] != NULL){
			if (strcmp(set->keys[y],key) != 0){
				y = (hkey + (j*j) + (23*j)) % 101;
				j++;
			} else {
				break;
			}
		} else {
			y = (hkey + (j*j) + (23*j)) % 101;
			j++;
		}
	}
	if (set->keys[y] != NULL){
        set->keys[y] = NULL;
        set->num_keys -= 1;
    }
	return 0;
}

void clear_table(hash_set *set){ //clears the table 
    for (int i = 0; i<TABLE_SIZE; i++){
        set->keys[i] = NULL;
    }
    set->num_keys = 0;
}

void display_keys(hash_set *set){ //displays the table
    printf("%d\n", set->num_keys);
    for (int i = 0; i<TABLE_SIZE; i++){
        if(set->keys[i] != NULL){
            printf("%d:%s\n", i, set->keys[i]);
        }
    }


}

int main (int argc, char *argv[]){
    char operation[MAX_INPUT_SIZE]; //buffer for reading operation
    char s[MAX_INPUT_SIZE];
    char* token;
    //char * operation = (char*) malloc(sizeof(char) * 19);
    bool valid = false;
    fgets(s, sizeof(s), stdin); //takes in the number of test cases
    int ntests = atoi(s);
    int len = strlen(s);
    while (len > 0 && isspace(s[len - 1]))
        len--;     // strip trailing newline or other white space
        if (len > 0){
        valid = true;
        for (int i = 0; i < len; ++i){
            if (!isdigit(s[i])){
                valid = false;
                return 0;
            }
        }
    }//ensures given input is correct and not simply empty stdin

    if(ntests ==0){
        return 0;
    }
    while (ntests > 0) {
        hash_set *ourtable = (hash_set *)calloc(1, sizeof(hash_set));
        int row, nRows;
        fscanf(stdin, "%d", &nRows); //takes in how many operations are going to be used
        for (row = 0; row < nRows; ++row){
            fscanf(stdin, "%s", operation); //takes in the complete operation line
            char * op = strtok(operation, ":");             //ADD or DEL
            token = (char*) malloc(sizeof(char) * 15);      //The actual contents ment for the hash 
            strncpy(token, operation + 4, 15);
            if (strcmp(op, "ADD") == 0){
            	if (token != NULL){
            		insert_key(ourtable,token);
            	} else {
            		insert_key(ourtable,"\0");
            	}
            }
            else if (strcmp(op, "DEL") == 0){
            	if (token != NULL){
            		delete_key(ourtable,token);
            	} else {
            		delete_key(ourtable, "\0");
            	}
            } else {
                return 0;
            }
            free(token);
    }
        ntests--;
        display_keys(ourtable);
        clear_table(ourtable);
        free(ourtable);
        
    }
    
    return 0;
}