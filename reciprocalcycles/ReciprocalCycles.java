/*******************************************************************************
 * Name        : ReciprocalCycles.java
 * Author      : Yakov Kazinets, Abderahim Salhi, Siddhanth Patel
 * Date        : 03/23/2021
 * Description : Modified Reciprocal Cycles Euler #26
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

import java.util.*;

public class ReciprocalCycles {
    public static void main(String[] args) {
        //Error Checking. Takes in only 1 integer as argument between 1-2000.
        int denominator = 0;
        if (args.length <= 0 || args.length > 1) {
            System.out.println("Usage: java ReciprocalCycles <denominator>");
            return;
        } else {
            try{
                denominator = Integer.parseInt(args[0]);
                if (denominator < 1 || denominator > 2000) {
                    System.out.println("Error: Denominator must be an integer in [1, 2000]. Received '" + args[0] + "'.");
                    return;
                }
            } catch(Exception e){
                System.out.println("Error: Denominator must be an integer in [1, 2000]. Received '" + args[0] +"'.");
				return;
			}
        }
        // If denominator is 1, then just output the obvious solution: 1/1 because otherwise digitList will be empty
        if (denominator == 1){
            System.out.println("1/1 = 1");
            return;
        }
        ArrayList<Integer> digitList = new ArrayList<>(); // digitList keeps track of all digits after '0.' from simple division
        ArrayList<Integer> remainderList = new ArrayList<>(); //remainderList keeps track of all remainders from division so that we can find any repeating remainders or a recurring pattern
        int remainder = 1; //Initialize the remainder to 1 because the numerator starts with 1
        int reccurPosition = -1; //Initialize reccuring position as -1 because the digits can repeat at index 0 onwards

        while (!remainderList.contains(remainder % denominator) && (remainder % denominator)!= 0){ //While there are no repeating remainders and the remainder is not 0 (no more digits left to add)
            remainder %= denominator;
            remainderList.add(remainder); //add remainder to remainderList
            remainder *= 10; //multiply remainder by 10 since remainder is not 0 yet (like you would do in basic division)
            digitList.add(remainder / denominator); // add the new decimal place into the digitList
            if (remainderList.contains(remainder % denominator)){ // if the remainderlist already contains the current remainder, mark that index with reccurPosition
                reccurPosition = remainderList.indexOf(remainder % denominator);
            }
        }

        //Outputs the final output by storing all digitvalues in a string
        //If there is a repeating group of digits, it will place parathensis around them and output the cycle length
        String finaloutput = "0.";
        for (int i = 0; i < digitList.size(); i++) {
            if (i == reccurPosition) { //if the index is equal to the reccuring index then put paranthesis, otherwise ignore
                finaloutput += "(";
            }
            finaloutput += digitList.get(i);
        }
        if (reccurPosition > -1){
            finaloutput = finaloutput + "), cycle length " + (digitList.size() - reccurPosition);
        }
        System.out.println("1/" + denominator + " = " + finaloutput);
    }
}
