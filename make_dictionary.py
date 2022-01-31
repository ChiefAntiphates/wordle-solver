file = open('full-dictionary.txt', 'r')
bad = [str(i) for i in range(0,10)]
bad.extend(['.','-',',','/'])
f = open("wordle-dictionary.txt", "w")
for line in file:
    word = line.strip()
    valid = True
    for c in bad:
        if c in word:
            valid = False
            break
    if valid and len(word) == 5:
        f.write(f'{word}\n')
