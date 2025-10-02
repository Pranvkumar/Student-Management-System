# Day 15 - Sorting Problems


# 2. Sort by String Length
def sort_by_length(strings):
#Sorts a list of strings by their length (shortest to longest).
#Maintains relative order for equal-length strings.

    return sorted(strings, key=len)

# Example:
if __name__ == "__main__":
    # 2. Sort by String Length
    print(sort_by_length(["apple", "pie", "washington", "cat"]))
    print(sort_by_length(["hello", "world", "a", "programming", "fun"]))
    print(sort_by_length(["java", "python", "c", "javascript"]))