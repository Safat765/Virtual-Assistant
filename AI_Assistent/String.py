a = "Hi, I am Safat. I am a CSE student."
print(a[1])

for x in "banana":
    print(x)

convert = a.lower()
keep = input("what you want to search is :")
search = keep.lower()
if search in convert:
    print("Yes, it's present")
else:
    print("Not present")

# Slicing String

word = "   Hello World"
print(len(word)) # string length

print(word[2:5]) # Slicing word index number [from:to]
print(word[:5]) # Slicing word form 1st to index 5
print(word[7:]) # Slicing word from index 7 to last

#  H    e  l  l  o     W  o  r  d
#  0    1  2  3  4  5  6  7  8  9
# -10  -9 -8 -7 -6 -5 -4 -3 -2 -1

### Modify Strings ###
# (Upper Case)

name = "A,B,C,D,E,F"
print(word.upper()) # upper case
print(word.lower()) # lower case
print(word.strip()) # remove whitespace
print(word.replace("H","S")) # replace string
print(name.split(",")) # Split string as ['..', '..']

### String Concatenation ###

name1 = "Hello"
name2 = "World"
FullName = name1 + name2
print(FullName)
full_name = name1 + " " + name2
print(full_name)

### Format String ###

age = 21