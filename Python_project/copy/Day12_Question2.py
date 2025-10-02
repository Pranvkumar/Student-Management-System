# 2. Remove Duplicate Characters
def remove_duplicates(string: str) -> str:
    seen_characters = set()
    result_characters = []
    for character in string:
        if character not in seen_characters:
            seen_characters.add(character)
            result_characters.append(character)
    return ''.join(result_characters)

# Example :
if __name__ == "__main__":
    print(remove_duplicates("programming")) 
    print(remove_duplicates("hello"))      
    print(remove_duplicates("aabbcc"))       