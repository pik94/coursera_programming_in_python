import sys
from math import sqrt


def solve_quadratic_equation(a, b, c):
    if not a:
        print("It's not a quadratic equation")
        return
    else:
        d = b ** 2 - 4 * a * c
        if d > 0:
            x_1 = (-b + sqrt(d)) / (2*a)
            x_2 = (-b - sqrt(d)) / (2*a)
            return (x_1, x_2)
        else:
            print("D <= 0. This case isn't considered")
            return

if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    result = solve_quadratic_equation(a, b, c)
    print(int(result[0]))
    print(int(result[1]))