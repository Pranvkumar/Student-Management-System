# Day 13 Question 3
def reverse_words(s):
    words = s.strip().split()
    return ' '.join(reversed(words))

# Example usage:
if __name__ == "__main__":
    # Q3 Examples
    examples_q3 = [
        "Hello World Programming",
        "The quick brown fox",
        "Java Python C++"
    ]
    for ex in examples_q3:
        result = reverse_words(ex)
        print(f'Input: "{ex}"')
        print(f'Output: "{result}"\n')