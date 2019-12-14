from collections import Counter

def iter_layer(img, width, height):
    for n in range(len(img) // (width * height)):
        yield img[n * width * height: (n + 1) * width * height]

def first_non_two(s):
    for ch in s:
        if ch != '2':
            return ch
    return '2'

IMG = open('./data/input.txt', 'r').read().strip()
layer_counts = [Counter(layer) for layer in iter_layer(IMG, width=25, height=6)]
min_zero_layer = min(layer_counts, key=lambda d: d['0'])
print(min_zero_layer)
print(f"The product of 1's and 2's in the minumum zero layer is {min_zero_layer['1'] * min_zero_layer['2']}")

layers = list(iter_layer(IMG, width=25, height=6))

message = []
for i in range(25 * 6):
    pixels = [layer[i] for layer in layers]
    message.append(int(first_non_two(pixels)))

for i in range(6):
    print(''.join([['.', '#'][i] for i in message[i*25: (i+1)*25] ]))
