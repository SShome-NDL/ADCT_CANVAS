a = 3

def update_a(x):
	a = x
	update_b(a)
	return a

def update_b(x):
	a = x + 1
	return a

print(a)
a = update_a(4)
b = update_b(1)
print(a)
print(b)
