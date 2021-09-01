/**********************************************************************************
 * Name        : Solution.java
 * Author      : Abderahim Salhi, Siddhanth Patel, Yakov Kazinets
 * Date        : 04/25/2021
 * Description : Hackerrank Running Median
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 **********************************************************************************/
import java.io.*;
import java.math.*;
import java.text.*;
import java.util.*;
import java.util.regex.*;
import java.util.PriorityQueue;
import java.util.Collections;

public class Solution {

    /*
     * Complete the runningMedian function below.
     */
    static double[] runningMedian(int[] a) {
        double currmedian = a[0]; //The current Median
        //declaration of Min Heap and Max Heap with the names of each accordingly
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder()); 
        maxHeap.add(a[0]);// since the first iteration is just the first item, it is added to the array.
        double[] doublearr = new double[a.length];
        doublearr[0] = currmedian;
        for (int i =1; i<a.length; i++){ //for loop that iterates through the 
            int currint = a[i];
            // <---------------- 1----------------> The MaxHeap has more elements
            if (maxHeap.size() > minHeap.size()){
                if (currint < currmedian){
                    minHeap.add(maxHeap.remove());
                    maxHeap.add(currint);
                } else {
                    minHeap.add(currint);
                }
                currmedian = (double) (maxHeap.peek() + minHeap.peek())/2;
            }
            // <----------------2 ----------------> The heaps are balanced 
            else if (maxHeap.size() == minHeap.size()){
                if (currint < currmedian){
                    maxHeap.add(currint);
                    currmedian = (double)maxHeap.peek();
                } else {
                    minHeap.add(currint);
                    currmedian = (double)minHeap.peek();
                }
            }
            // <----------------3 ---------------->
            else { //maxHeap.size() > minHeap.size()  All other cases fall under The MinHeap having more elements
                if (currint > currmedian){
                    maxHeap.add(minHeap.remove());
                    minHeap.add(currint);
                } else {
                    maxHeap.add(currint);
                }
                currmedian = (double) (maxHeap.peek() + minHeap.peek())/2;
            }
            doublearr[i] = currmedian; //Adding the current median value to the double array to be returned
        }
        return doublearr;
    }
    //used the hacckerrank method of taking the input in and printing due to weird outputing
    //mainly caused due to not understanding how the site wanted the values printed
    private static final Scanner scanner = new Scanner(System.in);
    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int aCount = Integer.parseInt(scanner.nextLine().trim());

        int[] a = new int[aCount];

        for (int aItr = 0; aItr < aCount; aItr++) {
            int aItem = Integer.parseInt(scanner.nextLine().trim());
            a[aItr] = aItem;
        }

        double[] result = runningMedian(a); //an array of doubles is returned from runningMedian of the given values
        for (int resultItr = 0; resultItr < result.length; resultItr++) {
            bufferedWriter.write(String.valueOf(result[resultItr]));

            if (resultItr != result.length - 1) {
                bufferedWriter.write("\n");
            }
        }
        
        bufferedWriter.newLine();
        bufferedWriter.close();
    }
}