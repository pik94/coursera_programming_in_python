import sys


def print_stairs(number):
    for i in range(0, number):
        print(" " * (number - 1 - i), end='')
        print("#" * (i + 1))

if __name__ == "__main__":
    input_str = sys.argv[1]
    print_stairs(int(input_str))
