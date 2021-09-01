#################################################################################
 # Name        : Solution.py
 # Author      : Abderahim Salhi, Siddhanth Patel, Yakov Kazinets
 # Date        : 05/04/2021
 # Description : Hackerrank Lego Blocks
 # Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 #################################################################################
import sys
# import time

Total = [0 for x in range(0, 1001)]
Solid = [0 for x in range(0, 1001)]
memo = {}

#function that returns the power of num ^ exponent. Memoized to speed up power function
def power_memoized(num, exp):
    key = str(num) +"," + str(exp) #store key as "num,exponent" in memo dictionary
    if key in memo: #if key already exists, return the value of the key
        return memo[key]
    else: #if key doesn't already exist, find the power and store in memo[key] by dividing and conquering the exponent
        if exp <= 2: # if exponent is small like 2 just find the power mod 1000000007 and store it
            memo[key] = (num ** exp) % 1000000007
        else: #otherwise, recursively call power_memoized function to divide up the powers and store it
            if exp % 2 == 0:
                memo[key] = (power_memoized(num, exp / 2) ** 2) % 1000000007
            else: #if power is odd, multiply num to the result of recursive call
                memo[key] = ((power_memoized(num, exp / 2) ** 2) * num) % 1000000007
        return memo[key]

def totallegoblocks(Height, Width):
    track = [1] # Holds the tetranacci sequence
    cur_width = 1 # First find out all possible ways to build a single row of a wall of a certain Width.
    while (cur_width < Width + 1): #Treat each row seperately since they are independent and can be multiplied by count later
        if cur_width >= len(track): # Create a tetranacci sequence as follows: if x > 0: T(X) = T(X-1)+T(X-2)+T(X-3)+T(X-4), otherwise T(X)=1 if X=0
            if cur_width - 4 >= 0: #checking if the index exists (all past four exist) in the tetranacci sequence to create the next number by adding past 4 numbers
                track.append((track[cur_width - 4] + track[cur_width - 3] + track[cur_width - 2] + track[cur_width - 1]) % 1000000007)
            elif cur_width - 3 >= 0: #checks if past 3 numbers exist
                track.append((track[cur_width - 3] + track[cur_width - 2] + track[cur_width - 1]) % 1000000007)
            elif cur_width - 2 >= 0: #checks if past 2 numbers exist
                track.append((track[cur_width - 2] + track[cur_width - 1]) % 1000000007)
            elif cur_width - 1 >= 0: #checks if previous number exists
                track.append((track[cur_width - 1]) % 1000000007)
            else: #if not, then track(x) = 0
                track.append(0)
        Total[cur_width] = power_memoized(track[cur_width], Height) # The number of total Width * Height walls is Total(w,h)=track(w)^h. Since we treated each row seperately, we are multiplying the count for all rows.
        cur_width+=1
            
if __name__ == "__main__":
    next(sys.stdin) # skip first line of input file
    for line in sys.stdin: # for each test case
        if not line.strip(): # if there is no new line then break
            break
        (Height, Width) = line.split() #split the line to get width and height
        (Height, Width) = (int(Height), int(Width)) #cast string values to int
        totallegoblocks(Height, Width) #call function to get all lego block layouts
        
        cur_width = 1
        while (cur_width < Width + 1): #Finally, using the array of Total Walls, we must figure out the total solid/unbreakable walls
            off = (1000000007 * 1000000007)
            Solid[cur_width] = Total[cur_width] + cur_width*off #Since the total number of walls is the number of solid walls * Total({W-X}*H) for all values of X + number of solid walls, we can rearrange to just get solid walls
            for i in range(1, cur_width):
                Solid[cur_width] = ((Solid[cur_width]) - Solid[i] * Total[cur_width - i]) # Number of solid walls = Total(W,H) - sum(Solid(X,H)*Total(current_Width-X,H))
            Solid[cur_width] = Solid[cur_width] % 1000000007
            cur_width+=1
        print(Solid[Width]) #return output