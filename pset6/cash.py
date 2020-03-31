# Get change input
while True:
    change = input("Change owed: ")
    try:
        change = float(change)
    except:
        continue

    # Check if height is in correct range
    if change > 0.00:

        # To overcome floating point precision limitations
        change *= 100
        break

# Available coins
coins = [25, 10, 5, 1]

# Number of coins returned as change
num_coins = 0

# Calculate number of returned coins
for coin in coins:
    n = change // coin
    if n >= 1.00:
        num_coins += n

        # Update remaining change
        change -= n * coin
        if change == 0.00:
            break

# Print result
print(int(num_coins))
