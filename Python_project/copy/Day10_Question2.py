# 2. Remove Spaces
def remove_all_spaces(s):
    return s.replace(" ", "")

def trim_spaces(s):
    return s.strip()

def single_spaces(s):
    return ' '.join(s.strip().split())

# 2. Remove Spaces Examples
space_examples = [
    " hello world ",
    "programming is fun",
    " a b c "
    ]
for s in space_examples:
    print(f'Input: "{s}"')
    print(f'Remove all: "{remove_all_spaces(s)}", Trim: "{trim_spaces(s)}", Single spaces: "{single_spaces(s)}"\n')
