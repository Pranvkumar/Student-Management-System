# Day 10 (25/06/2025)

# 1. String Comparison
def compare_strings(str1, str2):
    if str1 == str2:
        eq = "Equal"
        eq_ignore = "Equal ignoring case"
        lex = "Strings are identical"
    elif str1.lower() == str2.lower():
        eq = "Not equal"
        eq_ignore = "Equal ignoring case"
        lex = f'"{str1}" comes before "{str2}"' if str1 < str2 else f'"{str2}" comes before "{str1}"'
    else:
        eq = "Not equal"
        eq_ignore = "Not equal ignoring case"
        if str1 < str2:
            lex = f'"{str1}" comes before "{str2}"'
        elif str1 > str2:
            lex = f'"{str2}" comes before "{str1}"'
        else:
            lex = "Strings are identical"
    return eq, eq_ignore, lex

examples = [
    ("Hello", "hello"),
    ("apple", "banana"),
    ("test", "test")
    ]
for s1, s2 in examples:
    eq, eq_ignore, lex = compare_strings(s1, s2)
    print(f'Input: String1: "{s1}", String2: "{s2}"')
    print(f'Output:\n{eq}, {eq_ignore}, {lex}\n')

    
    