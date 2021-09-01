/*******************************************************************************
 * Name        : largesum.cpp
 * Author      : Siddhanth Y. Patel
 * Version     : 1.0
 * Date        : Feburary 14, 2021
 * Description : Adds large numbers from an input text file.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;


//function to find sum of all strings in inputfile vector
void findsum(const vector<string> &inputfile, int maxNumOfDigits){
    //keep track of total in string form because unsigned long long is too small for 50 digits
    string total = "";
	int currentSum = 0;
	int carry = 0;
    int numLen = 0;
    //loop through 50 digits to add last most digit to perform basic addition
    for(int i = 0; i < maxNumOfDigits; i++){
        currentSum = carry; // Current sum starts with carry from previous sum
        for(long unsigned int j = 0; j < inputfile.size(); j++){ //loop through all numbers to add the current digit place
            numLen = (int)inputfile[j].length();
            if (i < numLen){ //check whether current digit place exists for the number we're working with so we can add it, if not skip
                currentSum += inputfile[j][numLen - 1 - i] - '0';
            }
        }
        carry = currentSum / 10; //Update carry with new one from the sum of all digits in ith place
        total = to_string(currentSum % 10) + total; //Update the total string by placing new digit left hand side
    }
    total = to_string(currentSum/10) + total; //Update whatever sum is left to the total because there are no more digits to add
	
    //Find num of leading zeros to remove
    int i = 0;
    if (total[0] == '0'){
        while (total[i]=='0'){
            i++;
        }
    }
    //final variable without leading zeros
    string actualfinal = total.substr(i,total.length());
    if (actualfinal.length()==0){
        cout << "Full sum: " << 0 << endl;
	    cout << "First 10 digits: " << 0 << endl;
    } else {
        cout << "Full sum: " << actualfinal << endl;
	    cout << "First 10 digits: " << actualfinal.substr(0,10) << endl;
    }
}

int main(int argc, char *argv[]){
    //Getting input from text file line by line and storing in vector named inputfile
    string line;
    vector<string> inputfile;
    ifstream myfile ("input.txt");
    int maxNumOfDigits = 0;
    if (myfile.is_open()){
        int i = 0;
        while (getline(myfile, line)){
            maxNumOfDigits = max(maxNumOfDigits, (int)line.length());
            if (line[line.length()-1] - '0' == -35){ //if a '\n' exists, remove it in the inputfile vector string
                inputfile.push_back(line.substr(0,line.length()-1));
            } else {
                inputfile.push_back(line);
            }
            i++;
        }
        myfile.close();
        findsum(inputfile, maxNumOfDigits);
        return 0;
    } else {
        //error if no file is found
        cout << "Error: File 'nofile.txt' not found." << endl;
        return 1;
    }
}

