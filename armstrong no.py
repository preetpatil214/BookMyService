def count(n):
    num=n
    sum=0
    while n >0:
        sum=sum+1
        num=num//10
    return sum
print(count(1537))
