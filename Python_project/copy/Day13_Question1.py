# Day 13 Question 1
def word_count_and_longest(s):
    # Split by whitespace, ignore empty strings
    words = s.strip().split()
    count = len(words)
    longest = max(words, key=len) if words else ""
    return count, longest

# Example usage:
if __name__ == "__main__":
    # Q1 Examples
    examples_q1 = [
        "Hello world programming",
        " Java Python C++ ",
        "a bb ccc dddd"
    ]
    for ex in examples_q1:
        count, longest = word_count_and_longest(ex)
        print(f'Input: "{ex}"')
        print(f'Word count: {count}, Longest word: "{longest}"\n')
