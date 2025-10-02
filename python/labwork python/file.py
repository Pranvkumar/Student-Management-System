def write_squares_to_file(filename):
    with open(filename, 'w') as file:
        for i in range(51):
            file.write(f"{i**2}\n")

write_squares_to_file('square.txt')
