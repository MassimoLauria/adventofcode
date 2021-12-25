
start=108457
end=562041

def criteria1(n):
    t=str(n)
    twodigits=False
    for i in range(len(t)-1):
        if t[i]>t[i+1]:
            return False
        elif t[i]==t[i+1]:
            twodigits=True
    return twodigits

def criteria2(n):
    t=str(n)
    counts=[1]
    for i in range(1,len(t)):
        if t[i]<t[i-1]:
            return False
        elif t[i]==t[i-1]:
            counts[-1] += 1
        else:
            counts.append(1)
    return 2 in counts


def solve(criteria):
    count=0
    for n in range(start,end+1):
        if criteria(n):
            count+=1
    return count


print(solve(criteria1))
print(solve(criteria2))
