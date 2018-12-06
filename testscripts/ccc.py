def summation(number):
    summ = 0
    for num in number:
        summ += int(num)
    return str(summ)

p, q = input().split()
i = p * int(q)
while len(i) != 1:
    i = summation(i)
print(i)