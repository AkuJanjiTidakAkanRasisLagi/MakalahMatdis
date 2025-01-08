import time
from functools import lru_cache

# Precomputed factorials
factorials = [1] * 105
for i in range(1, 105):
    factorials[i] = factorials[i - 1] * i

# Predefined use array
use = [
    [0, 0, 0],
    [1, 1, 1],
    [2, 2, 2],
    [0, 0, 1],
    [0, 0, 2],
    [0, 1, 1],
    [1, 1, 2],
    [0, 2, 2],
    [1, 2, 2],
    [0, 1, 2],
]

# Recursive function with memoization


@lru_cache(None)
def solve(a, b, c):
    if a == 0 and b == 0 and c == 0:
        return 1

    ret = 0
    for l in range(10):
        arr = [a, b, c]
        valid = True

        # Update arr based on use[l]
        for m in range(3):
            arr[use[l][m]] -= 1

        # Check validity
        for x in arr:
            if x < 0:
                valid = False

        # Undo part of the decrement for repeated indices
        for m in range(3):
            if use[l][m] > 0:
                arr[use[l][m] - 1] += 1

        if valid:
            mul = 1
            div = 1
            if use[l][0] == use[l][1] == use[l][2]:
                div = factorials[3]
            elif use[l][0] == use[l][1] or use[l][1] == use[l][2]:
                div = factorials[2]

            num = [a, 2 * b, 3 * c]
            for m in range(3):
                mul *= num[use[l][m]]
                num[use[l][m]] -= (use[l][m] + 1)

            ret += (mul * solve(arr[0], arr[1], arr[2])) // div

    return ret


if __name__ == "__main__":
    n = int(input("Enter the number of groups: "))  # Number of groups in TB1

    start_time = time.time()
    result = solve(0, 0, n) // factorials[n]
    end_time = time.time()

    print("Possibilities: ", result)
    print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
