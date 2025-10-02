# 1. String Rotation
def is_rotation(string1: str, string2: str) -> bool:

    if len(string1) != len(string2):
        return False
    return string2 in (string1 + string1)

# Example usage:
if __name__ == "__main__":
    print(is_rotation("abcde", "cdeab"))  # True
    print(is_rotation("hello", "world"))  # False
    print(is_rotation("waterbottle", "erbottlewat"))  # True