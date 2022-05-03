import random

lower = "abcdefghijklmnopqrstuvqxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVQXYZ"
nums = "0123456789"
symbols = "!@#$%^&*"

all_tokens = lower + upper + nums + symbols
length = 4
password_chain= ""
for x in range(0,3):
    pw_block = "".join(random.sample(all_tokens,length))
    password_chain = pw_block + "-" + password_chain

print(password_chain[:-1])