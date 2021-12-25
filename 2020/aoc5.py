
def getbpasses(fname):
    with open(fname) as f:
        for line in f:
            
            bits = [ 0 if c in 'FL' else 1 for c in line.strip() ]
            
            sid = 0
            for b in bits:
                sid = 2*sid + b
            
            yield sid
    
    
    
def part1():
    B = list(getbpasses('aoc5input.txt'))
    print(max(B))
    
def part2():
    B = list(getbpasses('aoc5input.txt'))
    B.sort()
    # Print the missing seat.
    for i in range(1,len(B)):
        if B[i-1] != B[i] - 1:
            print(B[i]-1)
            return
 
part1()
part2()

