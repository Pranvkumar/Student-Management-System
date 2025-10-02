import os

# # write and read

# f = open('example.txt', 'w+')
# try:
#     f.write('\nTempering is a heat treatment technique applied to ferrous alloys, such as steel or cast iron, to achieve greater toughness by decreasing the hardness of the alloy. \nThe reduction in hardness is usually accompanied by an increase in ductility, thereby decreasing the brittleness of the metal. ')
#     f.seek(0)  # Move the cursor to the beginning of the f
#     content = f.read()
#     print(content)
# finally:
#     f.close()

# # Appending 
# f = open('example.txt', 'a')
# try:
#     f.write('\nThis is also called the lower transformation temperature or lower arrest (A1) temperature:\n the temperature at which the crystalline phases of the alloy, called ferrite and cementite, begin combining to form a single-phase solid solution referred to as austenite. ')
# finally:
#     f.close()

# # Example 4: Reading line by line
# f = open('example.txt', 'r')
# try:
#     for line in f:
#         print(line.strip())
# finally:
#     f.close()

# # try-except 
# try:
#     f = open('example.txt', 'r')
#     try:
#         content = f.read()
#         print(content)
#     finally:
#         f.close()
# except FileNotFoundError:
#     print("File not found.")

# # Example 6: Writing a list of lines to a f
# lines = ['\nHeating above this temperature is avoided, so as not to destroy the very-hard, quenched microstructure, called martensite.[3]', '\nTempering is accomplished by controlled heating of the quenched workpiece to a temperature below its "lower critical temperature". ', ' \nTempering is usually performed after quenching, which is rapid cooling of the metal to put it in its hardest state.']
# f = open('example.txt', 'w')
# try:
#     f.writelines('\n'.join(lines))
# finally:
#     f.close()

# # Example 7: Reading a f into a list of lines
# f = open('example.txt', 'r')
# try:
#     lines = f.readlines()
#     for line in lines:
#         print(line.strip())
# finally:
#     f.close()

# Deleting
try:
    os.remove('example.txt')
    print("File deleted successfully.")
except FileNotFoundError:
    print("File not found.")
