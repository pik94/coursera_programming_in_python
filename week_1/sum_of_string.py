import sys


def get_sum(digit_str):
    sum = 0
    if not digit_str.isdigit():
        return 0
    for i in digit_str:
        sum += int(i)
    return sum

if __name__ == "__main__":
    input_str = sys.argv[1]

    sum = get_sum(input_str)
    print(sum)
