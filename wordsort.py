import classes
import time
import tracemalloc
sort=classes.Sort()
filen = r"test files\hp1.txt"
with open(filen, 'rb') as file:
    content = file.read()

content = content.decode("ascii", "ignore")
print(filen)
# remove all non-alphabetical symbols from the text
for i in range(33, 127):
    if not (91>i>64 or 123>i>96):
        content = content.replace(chr(i), "")
content = content.replace("\r", "\n")
content = content.split("\n")
temp = []

# convert to a list of words
for i in content:
    temp += i.split(" ")

# find max len
maxlen = 0
for i in temp:
    if len(i) > maxlen:
        maxlen = len(i)

# pad words with reference to maxlen, change words in temp to numbers and cache repeating words
alphabet = "abcdefghijklmnopqrstuvwxyz"
cache = {}
translated = []
for i in temp:
    word = i + " "*(maxlen-len(i))
    if i not in cache:
        num = 0
        multi = 0
        rev = word[::-1]
        for l in rev:
            if l.lower() in alphabet:
                num += (ord(l.lower()) - 95) * (27 ** multi)
                multi += 1
            elif l == " ":
                num += (27 ** multi)
                multi += 1
        cache[i] = num
    else:
        num = cache[i]
    translated += [num]

"""# sort with quicksort algorithm
val, key = sort.quicksort(translated, temp)
print(val[::-1])
print(key[::-1])"""

# weave translated and temp into dict and send to heapsort for testing
foo = {}
for i in range(len(translated)):
    foo[temp[i]] = translated[i]


tracemalloc.start()

start = time.perf_counter()
returndict = sort.heapsort(foo)
"""print(list(returndict.values()))
print(list(returndict.keys()))"""
print("heapsort: " + str(time.perf_counter()-start))

start = time.perf_counter()
returndict = sort.quickdictsort(foo)
"""print(list(returndict.values()))
print(list(returndict.keys()))"""
print("quickdictsort: " + str(time.perf_counter()-start))

for i in tracemalloc.take_snapshot().statistics('lineno'):
    print(i)
