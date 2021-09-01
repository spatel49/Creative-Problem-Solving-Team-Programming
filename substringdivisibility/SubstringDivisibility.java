//  *******************************************************************************
//  * Name        : SubstringDivisibility.java
//  * Author      : Yakov Kazinets, Abderahim Salhi, Siddhanth Patel
//  * Date        : 2/16/21
//  * Description : Solving Modified Project Euler Problem 43.
//  * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
//  ******************************************************************************/

import java.util.Arrays;
import java.util.ArrayList;
import java.util.Collections;

public class SubstringDivisibility {
    // Attributes...
	private ArrayList<String> permutations;
    private long sum;
    private String input;
    
    
    // constructors...
    public SubstringDivisibility(String input) {    
        long start = System.nanoTime();
		permutations = new ArrayList<>();
        this.input = input;

        //function to find the possible permutations
        this.sum = 0;
		if (input.length() == 10){//Since Permutations function runs faster for smaller number of digits, split up the work using 7 digits each.
            //We know that the last three digits will be 867 or 289 because of the divisibility rules.
			findTenthPermutations("0134567"); //numbers excluding 289
			findTenthPermutations("0123459"); //numbers excluding 867
			Collections.sort(permutations); // sort Arraylist so they are in order
			for(String option: permutations) { //print Arraylist
				System.out.println(option);
			}
            System.out.println("Sum: "+ this.sum);
            System.out.printf("Elapsed time: %.6f ms\n", (System.nanoTime() - start) / 1e6);
		} else if (input.length() == 9){
			findNinthPermutations(input, false);
            System.out.println("Sum: "+ this.sum);
            System.out.printf("Elapsed time: %.6f ms\n", (System.nanoTime() - start) / 1e6);
		} else {
			findPermutations();
            System.out.println("Sum: "+ this.sum);
            System.out.printf("Elapsed time: %.6f ms\n", (System.nanoTime() - start) / 1e6);
		}

        
    }
    //is euler..
    private boolean isEuler(String option){
    	while(option.length() >=4) {
                switch(option.length()) {
                    case 4:
    				// If length is 4 then check if it is divisible by 2 or not.
    				if(((Long.parseLong(option.substring(1)) + Long.parseLong(option.substring(2))) & 2) != 0) {
    					return false;
    				}
    				break;
    			case 5:
    				// If length is 5 then check if it is divisible by 3 or not.
    				if(Long.parseLong(option.substring(2)) % 3 != 0) {
    					return false;
    				}
    				break;
    			case 6:
    				// If length is 6 then check if it is divisible by 5 or not.
    				if(Long.parseLong(option.substring(3)) % 5 != 0) {
    					return false;
    				}
    				break;
    			case 7:
    				// If length is 7 then check if it is divisible by 7 or not.
    				if(Long.parseLong(option.substring(4)) % 7 != 0) {
    					return false;
    				}
    				break;
    			case 8:
    				// If length is 8 then check if it is divisible by 11 or not.
    				if(Long.parseLong(option.substring(5)) % 11 != 0) {
    					return false;
    				}
    				break;
    			case 9:
    				// If length is 9 then check if it is divisible by 13 or not.
    				if(Long.parseLong(option.substring(6)) % 13 != 0) {
    					return false;
    				}
    				break;
    			case 10:
    				// If length is 10 then check if it is divisible by 17 or not.
    				if(Long.parseLong(option.substring(7)) % 17 != 0) {
    					return false;
    				}
    				break;
    			}
                int optint = option.length();
        		option = option.substring(0,optint-1);
        		optint--;
            }
    		
    	return true;
    	
    }
    
    private void swap(char[] arr, int i, int j) {
        char c = arr[i];
        arr[i] = arr[j];
        arr[j] = c;
    }
 
    // Utility function to reverse a char array between specified indices
    private void reverse(char[] arr, int i, int j)
    {
        // do till two endpoints intersect
        while (i < j) {
            swap(arr, i++, j--);
        }
    }
 
    // Iterative function to find permutations of a string in Java
    public void findPermutations()
    {
        // sort the string in a natural order
        char[] s = this.input.toCharArray();
        int n = this.input.length();
        Arrays.sort(s);
 
        while (true)
        {
        	if(isEuler(String.valueOf(s))) { //if current Permutation works
				System.out.println(String.valueOf(s));
				this.sum += Long.parseLong(String.valueOf(s));
			}
            // Find the largest index `i` such that `s[i-1]` is less than `s[i]`
            int i = n - 1;
            while (s[i-1] >= s[i])
            {
                // if `i` is the first index of the string, we are
                // already at the last possible permutation
                // (string is sorted in reverse order)
                if (--i == 0) {
                    return;
                }
            }
 
            // find the highest index `j` to the right of index `i` such that
 
            int j = n - 1;
            while (j > i && s[j] <= s[i-1])
                j--;
 
            // swap character at index `i-1` with index `j`
            swap(s, i - 1, j);
            
 
            // reverse substring `
            reverse (s, i, n - 1);
          
        }
    }

	public void findNinthPermutations(String input, boolean isTenth)
    {
        // sort the string in a natural order
        char[] s = input.toCharArray();
        int n = input.length();
        Arrays.sort(s);
 
        while (true)
        {  
            if (s[5]=='5' && (s[3] == '0' || s[3]=='6')){ //d6 must be 5, and d4 must be 0 or 6 so we don't have to check
                if(isEuler(String.valueOf(s))) { //check if the permutation is valid
                    System.out.println(String.valueOf(s));
                    this.sum += Long.parseLong(String.valueOf(s));
                }
            }
            // Find the largest index `i` such that `s[i-1]` is less than `s[i]`
            int i = n - 1;
            while (s[i-1] >= s[i])
            {
                // if `i` is the first index of the string, we are
                // already at the last possible permutation
                // (string is sorted in reverse order)
                if (--i == 0) {
                    return;
                }
            }
 
            // find the highest index `j` to the right of index `i` such that
 
            int j = n - 1;
            while (j > i && s[j] <= s[i-1])
                j--;
 
            // swap character at index `i-1` with index `j`
            swap(s, i - 1, j);
            
 
            // reverse substring `
            reverse (s, i, n - 1);
          
        }
    }


    public void findTenthPermutations(String input)
    {
        // sort the string in a natural order
        char[] s = input.toCharArray();
        int n = input.length();
        Arrays.sort(s);
 
        while (true)
        {
			if (s[5] == '5' && (s[0]=='4' || s[0] == '1')) { //d6 must be 5, and d1 must be 4 or 1 so we don't have to check
                if(isEuler(String.valueOf(s))) {
                    if (s[6]=='2'){ //Means the input fed into the function did not have 678
                        this.permutations.add(String.valueOf(s) + "867"); //Add the 867 (divisible by 17) to the number
                        this.sum += Long.parseLong(String.valueOf(s)+"867");
                    } else if (s[6] == '7') {//Means the input fed into the function did not have 289
                        this.permutations.add(String.valueOf(s) + "289"); //Add the 289 (divisible by 17) to the number
                        this.sum += Long.parseLong(String.valueOf(s)+"289");
                    }
                }
            }
            // Find the largest index `i` such that `s[i-1]` is less than `s[i]`
            int i = n - 1;
            while (s[i-1] >= s[i])
            {
                // if `i` is the first index of the string, we are
                // already at the last possible permutation
                // (string is sorted in reverse order)
                if (--i == 0) {
                    return;
                }
            }
 
            // find the highest index `j` to the right of index `i` such that
 
            int j = n - 1;
            while (j > i && s[j] <= s[i-1])
                j--;
 
            // swap character at index `i-1` with index `j`
            swap(s, i - 1, j);
            
 
            // reverse substring `
            reverse (s, i, n - 1);
          
        }
    }

	
        //Main method to run the program..
    public static void main(String[] args)  { 
    	String input = args[0];
        new SubstringDivisibility(input);
    }
    
}
