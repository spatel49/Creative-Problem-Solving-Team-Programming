#################################################################################
 # Name        : resistancematcher.py
 # Author      : Abderahim Salhi, Siddhanth Patel, Yakov Kazinets
 # Date        : 04/20/2021
 # Description : Resistance Matcher
 # Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 #################################################################################
####################version 4 all successfull #############################
import sys


def get_args():
    # Validate arguments
    args = sys.argv[1:]
    if len(args) != 4:
        print("Usage: python3.7 resistancematcher <target> <tolerance %> <num resistors> <input file>")
        return None
    try:
        target = float(args[0])
        assert target > 0
    except:
        print(f"Error: Invalid target value '{args[0]}'.")
        return None
    try:
        tolerance = float(args[1])
        assert tolerance >= 0
    except:
        print(f"Error: Invalid tolerance value '{args[1]}'.")
        return None
    try:
        max_n = int(args[2])
        assert max_n > 0
    except:
        print(f"Error: Invalid number of resistors '{args[2]}'.")
        return None
    try:
        file = args[3]
        open(file)
    except:
        print(f"Error: Input file '{args[3]}' not found.")
        return None
    return target, tolerance, max_n, file


def get_resistors(file):
    # Read a list of resistors from a file
    resistors = set()
    for i, line in enumerate(open(file), 1):
        line = line.strip()
        try:
            r = float(line)
            assert r > 0
            # If a resistor has resistance lower than target_min,
            # then it won't be able to contribute to the solution
            if r >= target_min:
                resistors.add(r)
        except:
            print(f"Error: Invalid value '{line}' on line {i}.")
            return None
    return list(resistors)

if __name__ == '__main__':
    args = get_args()
    if args is not None:
        target, tolerance, max_n, file = args
        # Allowed diviation from the target value
        target_min = target * ((100 - tolerance) / 100)
        target_max = target * ((100 + tolerance) / 100)

        resistors = get_resistors(file)
        if resistors is not None:
            # Sort resistors in descending order
            resistors.sort(reverse=True)
            # Inverse of a target
            target_inv = 1 / target
            target_inv_max = 1 / target_min
            target_inv_min = 1 / target_max
            # Inverse resistances
            resistors_inv = [1/r for r in resistors]

            # The original formula is:  target = 1 / (1/R1 + 1/R2 + ... 1/Rn)
            # By inverting the target and resitances, the formula that we need to match
            # becomes: target_inv = R1_inv + R2_inv + ... + Rn_inv

            # Answer will store indices of resistors in the solution combination
            answer = None
            # Error of the current answer (plain difference between resistances, not percentage)
            error = float('inf')
            # Table will store sums of combinations of n resistors
            # Initial table with 1 resistor
            table = {(i, ): resistors_inv[i] for i in range(len(resistors_inv))}
            for i in table:
                # Difference between resistance of the current combination and the target
                dif = round(abs(target - 1/table[i]), 10)
                if target_inv_min <= table[i] <= target_inv_max:
                    if dif < error:
                        # New best solution
                        answer = i
                        error = dif
            # Loop for n from 2 to maximum number of resistors
            for n in range(2, max_n+1):
                # Table from previous iteration
                table_prev = table
                # Create a new table in this iteration
                table = {}
                # Loop through combinations from previous iteration (of size n-1)
                for combo in sorted(table_prev):
                    sum_r = table_prev[combo]
                    # Try all new combinations of size n
                    for i in range(combo[-1], len(resistors_inv)):
                        # Find inverted resistance of that combination
                        r = resistors_inv[i]
                        new_sum_r = sum_r + r
                        dif = round(abs(target - 1/new_sum_r), 10)
                        # If it is a valid solution, then write it down
                        if target_inv_min <= new_sum_r <= target_inv_max:
                            if dif < error:
                                # New best solution
                                c = (combo, i)
                                answer = c
                                error = dif
                                table[c] = new_sum_r
                        # If it is bigger than target_inv_max, then ignore it and all
                        # resistors further in the list (the list was sorted)
                        elif new_sum_r > target_inv_max:
                            break
                        # Else add this combination to the table
                        else:
                            c = (combo, i)
                            table[c] = new_sum_r
            # Show the result
            print(f'Max resistors in parallel: {max_n}')
            print(f'Tolerance: {tolerance} %')
            if answer is None:
                print(f'Target resistance of {target} ohms is not possible.')
            else:
                # Unpack answer
                res = []
                while type(answer) is tuple:
                    res.append(resistors[answer[-1]])
                    answer = answer[0]
                print(f'Target resistance of {target} ohms is possible with {res} ohm resistors.')
                res_par = 1/sum(1/r for r in res)
                print(f'Best fit: {res_par:.4f} ohms')
                error = abs(res_par - target)/target * 100
                print(f'Percent error: {error:.2f} %')

####################version 3 test case 17 fail #############################
# sort combinations in table_prev when looping through combinations in table_prev and
#  when looping through resistances in resistors_inv to start from index
#  that is last in the combination
# import sys


# def get_args():
#     # Validate arguments
#     args = sys.argv[1:]
#     if len(args) != 4:
#         print("Usage: python3.7 resistancematcher <target> <tolerance %> <num resistors> <input file>")
#         return None
#     try:
#         target = float(args[0])
#         assert target > 0
#     except:
#         print(f"Error: Invalid target value '{args[0]}'.")
#         return None
#     try:
#         tolerance = float(args[1])
#         assert tolerance >= 0
#     except:
#         print(f"Error: Invalid tolerance value '{args[1]}'.")
#         return None
#     try:
#         max_n = int(args[2])
#         assert max_n > 0
#     except:
#         print(f"Error: Invalid number of resistors '{args[2]}'.")
#         return None
#     try:
#         file = args[3]
#         open(file)
#     except:
#         print(f"Error: Input file '{args[3]}' not found.")
#         return None
#     return target, tolerance, max_n, file


# def get_resistors(file):
#     # Read a list of resistors from a file
#     resistors = set()
#     for i, line in enumerate(open(file), 1):
#         line = line.strip()
#         try:
#             r = float(line)
#             assert r > 0
#             # If a resistor has resistance lower than target_min,
#             # then it won't be able to contribute to the solution
#             if r >= target_min:
#                 resistors.add(r)
#         except:
#             print(f"Error: Invalid value '{line}' on line {i}.")
#             return None
#     return list(resistors)

# if __name__ == '__main__':
#     args = get_args()
#     if args is not None:
#         target, tolerance, max_n, file = args
#         # Allowed diviation from the target value
#         target_min = target * ((100 - tolerance) / 100)
#         target_max = target * ((100 + tolerance) / 100)

#         resistors = get_resistors(file)
#         if resistors is not None:
#             # Sort resistors in descending order
#             resistors.sort(reverse=True)
#             # Inverse of a target
#             target_inv = 1 / target
#             target_inv_max = 1 / target_min
#             target_inv_min = 1 / target_max
#             # Inverse resistances
#             resistors_inv = [1/r for r in resistors]

#             # The original formula is:  target = 1 / (1/R1 + 1/R2 + ... 1/Rn)
#             # By inverting the target and resitances, the formula that we need to match
#             # becomes: target_inv = R1_inv + R2_inv + ... + Rn_inv

#             # Answer will store indices of resistors in the solution combination
#             answer = None
#             # Error of the current answer (plain difference between inversed resistances, not percentage)
#             error = float('inf')
#             # Table will store sums of combinations of n resistors
#             # Initial table with 1 resistor
#             table = {(i, ): resistors_inv[i] for i in range(len(resistors_inv))}
#             for i in table:
#                 # Difference between resistance of the current combination and the target
#                 dif = abs(table[i] - target_inv)
#                 if target_inv_min <= table[i] <= target_inv_max:
#                     if dif < error:
#                         # New best solution
#                         answer = i
#                         error = dif
#             # Loop for n from 2 to maximum number of resistors
#             for n in range(2, max_n+1):
#                 # Table from previous iteration
#                 table_prev = table
#                 # Create a new table in this iteration
#                 table = {}
#                 # Loop through combinations from previous iteration (of size n-1)
#                 for combo in sorted(table_prev):
#                     sum_r = table_prev[combo]
#                     # Try all new combinations of size n
#                     for i in range(combo[-1], len(resistors_inv)):
#                         # Find inverted resistance of that combination
#                         r = resistors_inv[i]
#                         new_sum_r = sum_r + r
#                         dif = abs(new_sum_r - target_inv)
#                         # If it is a valid solution, then write it down
#                         if target_inv_min <= new_sum_r <= target_inv_max:
#                             if dif < error:
#                                 # New best solution
#                                 c = (combo, i)
#                                 answer = c
#                                 error = dif
#                                 table[c] = new_sum_r
#                         # If it is bigger than target_inv_max, then ignore it and all
#                         # resistors further in the list (the list was sorted)
#                         elif new_sum_r > target_inv_max:
#                             break
#                         # Else add this combination to the table
#                         else:
#                             c = (combo, i)
#                             table[c] = new_sum_r
#             # Show the result
#             print(f'Max resistors in parallel: {max_n}')
#             print(f'Tolerance: {tolerance} %')
#             if answer is None:
#                 print(f'Target resistance of {target} ohms is not possible.')
#             else:
#                 # Unpack answer
#                 res = []
#                 while type(answer) is tuple:
#                     res.append(resistors[answer[-1]])
#                     answer = answer[0]
#                 print(f'Target resistance of {target} ohms is possible with {res} ohm resistors.')
#                 res_par = 1/sum(1/r for r in res)
#                 print(f'Best fit: {res_par:.4f} ohms')
#                 error = abs(res_par - target)/target * 100
#                 print(f'Percent error: {error:.2f} %')




####################version 2  test case 17 and 19 fail #############################
# For #17, the resistors are the same as expected, but they are printed in the different order.
# For #19, the program found a valid solution (0% error with 5 resistors), but it is different from the expected solution.

# import sys


# def get_args():
#     # Validate arguments
#     args = sys.argv[1:]
#     if len(args) != 4:
#         print("Usage: python3.7 resistancematcher <target> <tolerance %> <num resistors> <input file>")
#         return None
#     try:
#         target = float(args[0])
#         assert target > 0
#     except:
#         print(f"Error: Invalid target value '{args[0]}'.")
#         return None
#     try:
#         tolerance = float(args[1])
#         assert tolerance >= 0
#     except:
#         print(f"Error: Invalid tolerance value '{args[1]}'.")
#         return None
#     try:
#         max_n = int(args[2])
#         assert max_n > 0
#     except:
#         print(f"Error: Invalid number of resistors '{args[2]}'.")
#         return None
#     try:
#         file = args[3]
#         open(file)
#     except:
#         print(f"Error: Input file '{args[3]}' not found.")
#         return None
#     return target, tolerance, max_n, file


# def get_resistors(file):
#     # Read a list of resistors from a file
#     resistors = []
#     for i, line in enumerate(open(file), 1):
#         line = line.strip()
#         try:
#             r = float(line)
#             assert r > 0
#             # If a resistor has resistance lower than target_min,
#             # then it won't be able to contribute to the solution
#             if r >= target_min:
#                 resistors.append(r)
#         except:
#             print(f"Error: Invalid value '{line}' on line {i}.")
#             return None
#     return resistors

# if __name__ == '__main__':
#     args = get_args()
#     if args is not None:
#         target, tolerance, max_n, file = args
#         # Allowed diviation from the target value
#         target_min = target * ((100 - tolerance) / 100)
#         target_max = target * ((100 + tolerance) / 100)

#         resistors = get_resistors(file)
#         if resistors is not None:
#             # Sort resistors in descending order
#             resistors.sort(reverse=True)
#             # Inverse of a target
#             target_inv = 1 / target
#             target_inv_max = 1 / target_min
#             target_inv_min = 1 / target_max
#             # Maximum diviation alloved
#             max_dif_inv = target_inv_max - target_inv
#             # Inverse resistances
#             resistors_inv = [1/r for r in resistors]

#             # The original formula is:  target = 1 / (1/R1 + 1/R2 + ... 1/Rn)
#             # By inverting the target and resitances, the formula that we need to match
#             # becomes: target_inv = R1_inv + R2_inv + ... + Rn_inv

#             # Answer will store indices of resistors in the solution combination
#             answer = None
#             # Error of the current answer (plain difference between inversed resistances, not percentage)
#             error = float('inf')
#             # Table will store sums of combinations of n resistors
#             # Initial table with 1 resistor
#             table = {(i, ): resistors_inv[i] for i in range(len(resistors_inv))}
#             for i in table:
#                 # Difference between resistance of the current combination and the target
#                 dif = abs(table[i] - target_inv)
#                 if max_dif_inv >= dif:
#                     if dif < error:
#                         # New best solution
#                         answer = i
#                         error = dif
#             # Loop for n from 2 to maximum number of resistors
#             for n in range(2, max_n+1):
#                 # Table from previous iteration
#                 table_prev = table
#                 # Create a new table in this iteration
#                 table = {}
#                 # Loop through combinations from previous iteration (of size n-1)
#                 for combo in table_prev:
#                     sum_r = table_prev[combo]
#                     # Try all new combinations of size n
#                     for i in range(len(resistors_inv)):
#                         # Find inverted resistance of that combination
#                         r = resistors_inv[i]
#                         new_sum_r = sum_r + r
#                         dif = abs(new_sum_r - target_inv)
#                         # If it is a valid solution, then write it down
#                         if max_dif_inv >= dif:
#                             if dif < error:
#                                 # New best solution
#                                 c = (combo, i)
#                                 answer = c
#                                 error = dif
#                                 table[c] = new_sum_r
#                         # If it is bigger than target_inv_max, then ignore it and all
#                         # resistors further in the list (the list was sorted)
#                         elif new_sum_r > target_inv_max:
#                             break
#                         # Else add this combination to the table
#                         else:
#                             c = (combo, i)
#                             table[c] = new_sum_r

#             # Show the result
#             print(f'Max resistors in parallel: {max_n}')
#             print(f'Tolerance: {tolerance} %')
#             if answer is None:
#                 print(f'Target resistance of {target} ohms is not possible.')
#             else:
#                 # Unpack answer
#                 res = []
#                 while type(answer) is tuple:
#                     res.append(resistors[answer[-1]])
#                     answer = answer[0]
#                 print(f'Target resistance of {target} ohms is possible with {res} ohm resistors.')
#                 res_par = 1/sum(1/r for r in res)
#                 print(f'Best fit: {res_par:.4f} ohms')
#                 error = abs(res_par - target)/target * 100
#                 print(f'Percent error: {error:.2f} %')


####################################version 1 only test validation works #################################
# import sys


# def get_args():
#     # Validate arguments
#     args = sys.argv[1:]
#     if len(args) != 4:
#         print("Usage: python3.7 resistancematcher <target> <tolerance %> <num resistors> <input file>")
#         return None
#     try:
#         target = float(args[0])
#         assert target > 0
#     except:
#         print(f"Error: Invalid target value '{args[0]}'.")
#         return None
#     try:
#         tolerance = float(args[1])
#         assert tolerance >= 0
#     except:
#         print(f"Error: Invalid tolerance value '{args[1]}'.")
#         return None
#     try:
#         max_n = int(args[2])
#         assert max_n > 0
#     except:
#         print(f"Error: Invalid number of resistors '{args[2]}'.")
#         return None
#     try:
#         file = args[3]
#         open(file)
#     except:
#         print(f"Error: Input file '{args[3]}' not found.")
#         return None
#     return target, tolerance, max_n, file


# def get_resistors(file):
#     # Read a list of resistors from a file
#     resistors = []
#     for i, line in enumerate(open(file), 1):
#         line = line.strip()
#         try:
#             r = float(line)
#             assert r > 0
#             # If a resistor has resistance lower than target_min,
#             # then it won't be able to contribute to the solution
#             if r >= target_min:
#                 resistors.append(r)
#         except:
#             print(f"Error: Invalid value '{line}' on line {i}.")
#             return None
#     return resistors

# if __name__ == '__main__':
#     args = get_args()
#     if args is not None:
#         target, tolerance, max_n, file = args
#         # Allowed diviation from the target value
#         target_min = target * ((100 - tolerance) / 100)
#         target_max = target * ((100 + tolerance) / 100)

#         resistors = get_resistors(file)
#         if resistors is not None:
#             # Sort resistors in descending order
#             resistors.sort(reverse=True)
#             # Inverse of a target
#             target_inv_max = 1 / target_min
#             target_inv_min = 1 / target_max
#             # Inverse resistances
#             resistors_inv = [1/r for r in resistors]

#             # The original formula is:  target = 1 / (1/R1 + 1/R2 + ... 1/Rn)
#             # By inverting the target and resitances, the formula that we need to match
#             # becomes: target_inv = R1_inv + R2_inv + ... + Rn_inv

#             # answer will store indices of resistors in the solution combination
#             answer = None
#             # Table to store sums of combinations of n resistors
#             # Initial table with 1 resistor 
#             table = {(i, ): resistors_inv[i] for i in range(len(resistors_inv))}
#             for i in table:
#                 if target_inv_min <= table[i] <= target_inv_max:
#                     answer = i
#                     break
#             # Loop for n from 2 to maximum number of resistors
#             for n in range(2, max_n+1):
#                 # Table from previous iteration
#                 table_prev = table
#                 # Create a new table in this iteration
#                 table = {}
#                 if answer is None:
#                     # Loop through combinations from previous iteration
#                     for combo in table_prev:
#                         if answer is None:
#                             sum_r = table_prev[combo]
#                             # Create new combinations of size n
#                             for i in range(len(resistors_inv)):
#                                 # Find inverted resistance of that combination
#                                 r = resistors_inv[i]
#                                 new_sum_r = sum_r + r
#                                 # If it is a valid solution, then write it down and stop looping
#                                 if target_inv_min <= new_sum_r <= target_inv_max:
#                                     c = (combo, i)
#                                     answer = c
#                                     break
#                                 # If it is bigger than target_inv_max, then ignore it and all
#                                 # resistors further in the list (the list was sorted)
#                                 elif new_sum_r > target_inv_max:
#                                     break
#                                 # Else add this combination to the table
#                                 else:
#                                     c = (combo, i)
#                                     table[c] = new_sum_r


#             print(f'Max resistors in parallel: {max_n}')
#             print(f'Tolerance: {tolerance} %')
#             if answer is None:
#                 print(f'Target resistance of {target} ohms is not possible.')
#             else:
#                 # Unpack answer
#                 res = []
#                 while type(answer) is tuple:
#                     res.append(resistors[answer[-1]])
#                     answer = answer[0]
#                 print(f'Target resistance of {target} ohms is possible with {res} ohm resistors.')
#                 res_par = 1/sum(1/r for r in res)
#                 print(f'Best fit: {res_par:.4f} ohms')
#                 error = abs(res_par - target)/target * 100
#                 print(f'Percent error: {error:.2f} %')
