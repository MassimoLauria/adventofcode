from intcode import IntCode

test1="109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
test2="1102,34915192,34915192,7,4,7,99,0"
test3="104,1125899906842624,99"

if __name__=="__main__":
    print(IntCode(test1,[]))
    print(IntCode(test2,[]))
    print(IntCode(test3,[]))
    print(IntCode(open("input09.txt"),[1]))
    print(IntCode(open("input09.txt"),[2]))
