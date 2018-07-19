
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def encode(s, offset):
    out = ""
    for c in s:
        if c in alphabet:
            out += alphabet[(alphabet.index(c) + offset) % 26]
        else:
            out += c
    return out

def decode(s, offset):
    out = ""
    for c in s:
        if c in alphabet:
            out += alphabet[(alphabet.index(c) - offset) % 26]
        else:
            out += c
    return out

if __name__ == '__main__':
    code = encode("z", 1)
    print(code)
    out = decode(code, 1)
    print(out)
