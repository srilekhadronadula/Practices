def mis(num):
    num=str(num)
    m=[]
    for i in range(10):
        if str(i) not in num:
            m.append(i)
    return m
num=int(input())
print(mis(num))
