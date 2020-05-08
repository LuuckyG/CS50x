# Get height
while True:
    height = input("Height: ")
    try:
        height = int(height)
    except:
        continue

    # Check if height is in correct range
    if 0 < height <= 8:
        break

# Print pyramid
for i in range(1, height + 1):
    # Left side
    print(' ' * (height - i), end='')
    print('#' * i, end='')

    # Middle gap
    print(' ' * 2, end='')

    # Right side
    print('#' * i)
