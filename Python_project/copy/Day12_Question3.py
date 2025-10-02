 # 3. Compress String
def compress_string(string: str) -> str:

    if not string:
        return string
    compressed = []
    count = 1
    for index in range(1, len(string)):
        if string[index] == string[index-1]:
            count += 1
        else:
            compressed.append(f"{string[index-1]}{count}")
            count = 1
    compressed.append(f"{string[-1]}{count}")
    compressed_string = ''.join(compressed)
    return compressed_string if len(compressed_string) < len(string) else string

# Example :
if __name__ == "__main__":
    print(compress_string("aabcccccaaa")) 
    print(compress_string("abc"))          
    print(compress_string("aabbcc"))      