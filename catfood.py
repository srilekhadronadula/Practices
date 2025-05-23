def catfood(c,n,u,arr):
    if(n==0):
        return -1
    else:
        sum=0
        a=c*u
        for i in range(n):
            sum+=arr[i]
            if(sum>=a):
                return i+1
        if sum<a:
            return 0
n=int(input())
c=int(input())
u=int(input())
arr=[]
for i in range(n):
    arr.append(int(input()))
print(catfood(c,n,u,arr))
