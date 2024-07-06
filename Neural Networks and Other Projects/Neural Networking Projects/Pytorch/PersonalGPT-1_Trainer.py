# Open and Read the File
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of Characters In Dataset', len(text))

# Characters in Set
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(''.join(chars))
print(vocab_size)

# Character Mapping
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s]   # Take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # Take a list of integers, output a string

print(encode('Hello There'))
print(decode(encode('Hello There')))

# Importing Pytorch and registering the dataset
import torch
data = torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)
#print(data[:1000]) # First 1000 Characters as it is viewed by the GPT

# Splitting the data into training, and validation sets
n = int(0.9*len(data)) # First 90% is used for training, all the rest will be for validation
train_data = data[:n]
val_data = data[n:]

# We train the model using chunks of data at a time to not overload your system
# We call these chunks "Blocks"

block_size = 8
train_data[block_size+1]

x = train_data[:block_size]
y = train_data[1:block_size+1]
for t in range(block_size):
    context = x[:t+1]
    target = y[t]
    print(f"when input is {context} the target: {target}")

# Batches of chunks of data
torch.manual_seed(1337)
batch_size = 4 # how many independent sequences will we process in parallel?
block_size = 8 # what is the maximum context length for predictions?

def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y
xb, yb = get_batch('train')
print('inputs:')
print(xb.shape)
print(xb)
print('targets:')
print(yb.shape)
print(yb)

print('----')

for b in range(batch_size): # batch dimension
    for t in range(block_size): # time dimension
        context = xb[b, :t+1]
        target = yb[b, t]
        print(f'when input is {context.tolist()} the target: {target}')
        
