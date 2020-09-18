import random

# print(random.randrange(0,10,2))  # rand in range with step
# print(random.randint(5,10))
# print(random.random())         # rand value
# x = [1,2,3,4,5]
# print(random.shuffle(x), x)    # shuffle in-place
# print(random.choices(x, k=3))  # k choices
# print(random.choice(x))        # 1 choice

list_1 = [7, 1]
h = int(bool(list_1)) and max(list_1) # h=0 when list is empty or h=max if list has values - BOOL AND SHORT CIRCUIT
# h = min if bool(list_1) if bool(list_1) else 0
print(h)
print(1 and 7)
