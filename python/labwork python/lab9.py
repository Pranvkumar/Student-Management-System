# Step 1: Create a file and write about yourself
file_name = "prometheus.text"

# Writing 10 lines to the file
with open(file_name, "w") as file:
    file.write("""In Greek mythology, Prometheus ; \nAncient Greek: , possibly meaning forethought[1] is a Titan.[2]\n He is best known for defying the Olympian gods by taking fire from them and giving it to humanity in the form of technology, knowledge and, more generally, civilization.\nIn some versions of the myth, Prometheus is also credited with the creation of humanity from clay.[3]\n He is known for his intelligence and for being a champion of mankind[4] \nand is also generally seen as the author of the human arts and sciences.[5]\n He is sometimes presented as the father of Deucalion, the hero of the flood story.\n""")

# Step 2: Display the content of the file line by line
print("Content of the file:")
with open(file_name, "r") as file:
    for line in file:
        print(line.strip())

# Step 3: Count lines not starting with 'A'
with open(file_name, "r") as file:
    lines = file.readlines()
    Not_A = sum(1 for line in lines if not line.startswith("A"))
print(f"\nNumber of lines not starting with 'A': {Not_A}")

# Step 4: Count total number of words in the file
with open(file_name, "r") as file:
    words = file.read().split()
print(f"Total number of words in the file: {len(words)}")

# Step 5: Count words with length less than 4
short_words_count = sum(1 for word in words if len(word) < 4)
print(f"Number of words with length less than 4: {short_words_count}")