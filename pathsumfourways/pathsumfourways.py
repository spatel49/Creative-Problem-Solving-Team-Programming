
#################################################################################
 # Name        : pathsumfourways.py
 # Author      : Abderahim Salhi, Siddhanth Patel, Yakov Kazinets
 # Date        : 04/6/2021
 # Description : Modified project EULER83 
 # Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 #################################################################################

#!/usr/bin/python3

import sys
import os

# We need exactly one argument besides the program name itself
if len(sys.argv) != 2:
    print("Usage: python3.7 pathsumfourways <input file>")
    sys.exit(0)

# Check if provided argument is a name of existing file
if not os.path.exists(sys.argv[1]):
    print("Error: File '%s' not found." % sys.argv[1])
    sys.exit(0)

# Read the matrix from the file
matrix = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        l = l.strip()
        # Every line of the matrix is an array obtained
        # by splitting the line read from file by commas
        # Not forget to convert all strings to integers
        matrix.append([int(s) for s in l.split(",")])

num_rows = len(matrix)
num_cols = len(matrix[0])

# min_sum will store minimal sum from top-left corner to any given matrix element
# Let's fill it with Inf values - Infinity indicates that we don't know the sum yet
min_sum = [[float('inf') for col in range(num_cols)] for row in range(num_rows)]

# for every matirx element, min_path will contain its predecessor in the minimal path
min_path = [[None for col in range(num_cols)] for row in range(num_rows)]

min_sum[0][0] = matrix[0][0]

#
# Aux function - compare min_sum[x][y] with (min_sum[r][c] + matrix[x][y])
# if the former is not yet set or lower than the second value,
# then set it to the (min_sum[r][c] + matrix[x][y])
# 
def adjust_sum(r, c, x, y, matrix, min_sum, min_path):
    # Nothing to do if we don't know min_sum[r][c] yet
    if min_sum[x][y] > min_sum[r][c] + matrix[x][y]:
        min_sum[x][y] = min_sum[r][c] + matrix[x][y]
        min_path[x][y] = (r,c)

# Number of matrix elements
size = num_rows * num_cols

# # This is a variation of Bellman–Ford algorithm (https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
# for v in range(size+1):
#     for r in range(num_rows):
#         for c in range(num_cols):
#             # working with matrix element at [r][c]
#             # in terms of Bellman–Ford algorithm, it has 4 neighbors -
#             # items in the matrix at the right, at the left, up and down
#             # (unless we are not at the border)
#             if c > 0:
#                 adjust_sum(r, c, r, c-1, matrix, min_sum, min_path)
#             if c < num_cols-1:
#                 adjust_sum(r, c, r, c+1, matrix, min_sum, min_path)
#             if r > 0:
#                 adjust_sum(r, c, r-1, c, matrix, min_sum, min_path)
#             if r < num_rows-1:
#                 adjust_sum(r, c, r+1, c, matrix, min_sum, min_path)

# This is a Dijkstra's algorithm (https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
check_dist = lambda u: min_sum[u[0]][u[1]]
#unvisited =  [(i,j) for i in range(num_rows) for j in range(num_cols)]
#check_dist = lambda u: u[2]
unvisited = [(0,0)]
processed = []
while unvisited:
    u = min(unvisited, key = check_dist)
    unvisited.remove(u)

    c = u[1]
    r = u[0]
    if (r,c) in processed:
        continue

    processed.append((r,c))

    if c > 0:
        if min_sum[r][c-1] > min_sum[r][c] + matrix[r][c-1]:
            min_sum[r][c-1] = min_sum[r][c] + matrix[r][c-1]
            min_path[r][c-1] = (r,c)
#        adjust_sum(r, c, r, c-1, matrix, min_sum, min_path)
            unvisited.append((r,c-1))
    if c < num_cols-1:
        if min_sum[r][c+1] > min_sum[r][c] + matrix[r][c+1]:
            min_sum[r][c+1] = min_sum[r][c] + matrix[r][c+1]
            min_path[r][c+1] = (r,c)
#        adjust_sum(r, c, r, c+1, matrix, min_sum, min_path)
            unvisited.append((r,c+1))
    if r > 0:
        if min_sum[r-1][c] > min_sum[r][c] + matrix[r-1][c]:
            min_sum[r-1][c] = min_sum[r][c] + matrix[r-1][c]
            min_path[r-1][c] = (r,c)
#       adjust_sum(r, c, r-1, c, matrix, min_sum, min_path)
            unvisited.append((r-1,c))
    if r < num_rows-1:
        if min_sum[r+1][c] > min_sum[r][c] + matrix[r+1][c]:
            min_sum[r+1][c] = min_sum[r][c] + matrix[r+1][c]
            min_path[r+1][c] = (r,c)
            unvisited.append((r+1,c))
    #    adjust_sum(r, c, r+1, c, matrix, min_sum, min_path)


# Build full path from upper-left corner to the lower-right one
# which gives minimal sum. In min_path, we store predecessors of every node
# in the path, so we will start with lower-right element and build "reversed"
# path
px = num_rows-1
py = num_cols-1
path_to_corner = []
while px > 0 or py > 0:
    path_to_corner.append(matrix[px][py])
    (px, py) = min_path[px][py]
path_to_corner.append(matrix[0][0])

print("Min sum: %d" % min_sum[num_rows-1][num_cols-1])
# '::-1' will reverse the array since we have reversed path there at the moment
print("Values:  " + str(path_to_corner[::-1]))
