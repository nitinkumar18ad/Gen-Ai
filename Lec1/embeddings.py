import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("vocab Size",encoder.n_vocab)

text = "The cat sat on the mat"
tokens = encoder.encode(text)

print("Token",tokens)

my_token = [976, 9059, 10139, 402, 290, 2450]
decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450])
print("Decoded", decoded)
