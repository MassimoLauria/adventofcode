
from intcode import IntCode,IntCodeCPU
from itertools import permutations


testcode1="3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
testcode2=[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
testcode3=[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
testcode4=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
testcode5=[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

def trysetting1(setting,code):
    signal=0    
    for amp in setting:
        signal=IntCode(code,[amp,signal])[0]
    return signal

def trysetting2(setting,code):
    signal=0
    CPUS=[]
    for i in range(5):
        #print(f"Init CPU {i} with phase {setting[i]}")
        CPU=IntCodeCPU(code)
        CPU.add_input([setting[i]])
        CPUS.append(CPU)

    data=[0]
    active_amp=0
    while True:
        #print(f"CPU {active_amp}: gets {data}")
        CPUS[active_amp].add_input(data)
        #print(f"CPU {active_amp}: runs")
        CPUS[active_amp].run()
        data=CPUS[active_amp].get_output()
        CPUS[active_amp].flush_output()
        #print(f"CPU {active_amp}: sends {data}")
        
        if active_amp==4 and CPUS[4].halted():
            return data[0]
        
        active_amp += 1
        active_amp %= 5


def bruteforce(code=None,part2=True):
    
    if code is None:
        code=open("input07.txt")
    
    bestsignal=0
    bestsetting=None
    
    if part2:
        settings=permutations([5,6,7,8,9])
        trysetting=trysetting2
    else:
        settings=permutations([0,1,2,3,4])
        trysetting=trysetting1
    
    for setting in settings:
        s=trysetting(setting,code)
        if s > bestsignal:
            bestsignal = s
            bestsetting = setting
    return bestsignal,bestsetting
    

if __name__=="__main__":
    print(bruteforce(code=testcode1,part2=False)) # test 1
    print(bruteforce(code=testcode2,part2=False)) # test 2
    print(bruteforce(code=testcode3,part2=False)) # test 3
    print(bruteforce(part2=False)) # part 1
    print(bruteforce(code=testcode4,part2=True)) # test 3
    print(bruteforce(code=testcode5,part2=True)) # test 3
    print(bruteforce()) # part 2