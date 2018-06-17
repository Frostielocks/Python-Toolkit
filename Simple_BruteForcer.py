from BruteForcer import BruteForcer
import math
import string
import sys
import time


def calculate_depth(max, safe=True, debug=False):
    base = len(characters)
    d = (int(math.log(max, base)) if safe else int("%0.f" % math.log(max, base)))
    if debug:
        print("Maximum Depth: %f" % math.log(max, base))
    return d


def main():
    password = sys.argv[1]
    depth = calculate_depth(max, safe, debug)
    start = time.time()
    output = func(password, depth)
    end = time.time()
    print(output)
    if debug:
        print("Running time: %0.3f" % (end - start))


debug = True # Print debug  output
characters = string.printable
#characters = string.ascii_letters
#characters = string.ascii_lowercase
#characters = string.ascii_uppercase
#characters = string.hexdigits
#characters = string.digits
bf = BruteForcer(characters)
func = bf.mem_bruteforce # What kind of bruteforce function
max = math.pow(10, 7) # Maximum amount of strings in memory
safe = True # Safe rounding
main()
