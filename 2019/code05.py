
from intcode import IntCode

 
if __name__=="__main__":
    with open("input05.txt") as f:
        output=IntCode(f,[1],printcode=False)  # Part 1
        print(output[-1])        
        output=IntCode(f,[5],printcode=False)  # Part 2
        print(output[-1])        
    