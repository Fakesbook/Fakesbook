
# Remember lists start at 0 not 1
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# Fill in your code to encode a string of characters here
# s will be the string of characters to encode and
# offset will be the amount that each character should be shifted
def encode(s, offset):
    # Since strings in python cannot be changed directly
    # you will need to create a new variable to keep track of
    # the new encoded string

    # Next you need to loop over every character in s
    # (remember you can do this using a for loop
    #   it will probably look something like this:
    #   for character in string: )

    # Inside the for loop you will need to find the
    # replacement character based off of the offset

    # Hint: use alphabet.index(character) to find
    #   the index number of the character in the alphabet

    # Remember you can access a letter of the alphabet using
    # alphabet[the index number of the letter]
    # i.e. alphabet[25] = 'z'

    # Once you have figured out the new letter you should add
    # it to the variable you created to keep track of the new
    # string
    # You can add characters to a string with: string = string + character

    # Now at the very end you just need tor return your new string
    return

# Fill in your code to decode a string of characters here
# s will be the string of characters to decode and
# offset will be the amount that each character should be shifted
def decode(s, offset):
    # You should be able to copy your code from encode
    # and it should work

    # just remember to subtract the offset instead of adding it
    return
