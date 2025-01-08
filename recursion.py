import time
from math import factorial
from functools import lru_cache

# Memoization dictionary for storing the results of states
memo = {}

# Recursive function to calculate the number of ways to form groups


def solve_config(count_group):
    # Check if all groups are empty
    if all(x == 0 for x in count_group):
        return 1

    # Check memo
    tuple_state = tuple(count_group)
    if tuple_state in memo:
        return memo[tuple_state]

    ways = 0
    N = len(count_group)

    # Try selecting 3 different groups (x < y < z) that still have members
    for x in range(N):
        if count_group[x] == 0:
            continue
        for y in range(x + 1, N):
            if count_group[y] == 0:
                continue
            for z in range(y + 1, N):
                if count_group[z] == 0:
                    continue

                # Number of ways to pick 1 member from groups x, y, z
                pick_count = count_group[x] * count_group[y] * count_group[z]

                # Reduce 1 member from each group and proceed recursively
                count_group[x] -= 1
                count_group[y] -= 1
                count_group[z] -= 1

                ways += pick_count * solve_config(count_group)

                # Backtrack to restore the state
                count_group[x] += 1
                count_group[y] += 1
                count_group[z] += 1

    # Store the result in memo and return
    memo[tuple_state] = ways
    return ways


def main():
    N = int(input("Enter the number of groups: "))  # Number of groups in TB1

    # Assume each group starts with 3 members
    count_group = [3] * N

    # Start measuring time
    start_time = time.time()

    # Solve the configuration
    result = solve_config(count_group)

    # Divide by N! to ignore the order of group formation
    res_without_order = result // factorial(N)

    # End measuring time
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds

    # Output the result and the time taken
    print("Possibilities: ", res_without_order)
    print(f"Time taken: {duration:.2f} ms")


if __name__ == "__main__":
    main()
