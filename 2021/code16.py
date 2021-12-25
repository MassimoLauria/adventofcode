from collections import defaultdict

def loadbinary(data=None):
    digits=defaultdict(lambda:'')
    for x in "0123456789ABCDEF":
        digits[x]="{:04b}".format(int(x,16))
    
    if data is None:
        with open("input16.txt") as f:
            data=f.read()
    res=[digits[x] for x in data]
    return "".join(res)

def parseliteral(packet,s):
    acc=0
    i=s
    while True:
        acc *= 16
        i += 5
        acc += int(packet[i-4:i],2)
        if packet[i-5]=='0':
            break
    return i,acc
        

def parsepacket(packet,s=0):
    "Returns the cursor positions and the value of the packet"
    version = int(packet[s+0:s+3],2)
    typeID  = int(packet[s+3:s+6],2)
    
    if typeID==4: # literal
        i,value=parseliteral(packet,s+6)
        return i,version,typeID,[value]
    
    # operations
    lengthtypeID=packet[s+6:s+7]
    if lengthtypeID=='0':
        bitlength=int(packet[s+7:s+22],2)
        i=s+22
        operands=[]
        while i<s+22+bitlength:
            i,v,t,d=parsepacket(packet,i)
            operands.append((i,v,t,d))
        assert i == s+22+bitlength
    else:
        npackets=int(packet[s+7:s+18],2)
        i=s+18
        operands=[]
        for _ in range(npackets):
            i,v,t,d=parsepacket(packet,i)
            operands.append((i,v,t,d))
    return i,version,typeID,operands


def sumversionhierarchy(hierarchy):
    if isinstance(hierarchy,int):
        return 0
    _,ver,_,branch = hierarchy
    acc=0
    if isinstance(branch,list):
        for h in branch:
            acc+=sumversionhierarchy(h)
    acc+=ver
    return acc


def evalhierarchy(hierarchy):
    if isinstance(hierarchy,int):
        return hierarchy

    _,_,typeID,branch = hierarchy

    assert isinstance(branch,list)
    operands = [evalhierarchy(h) for h in branch ] 

    if typeID==0:
        return sum(operands)
    elif typeID==1:
        acc=1
        for v in operands:
            acc*=v
        return acc
    elif typeID==2:
        return min(operands)
    elif typeID==3:
        return max(operands)
    elif typeID == 4:
        return branch[0]
    elif typeID==5:
        return 1 if operands[0]>operands[1] else 0
    elif typeID==6:
        return 1 if operands[0]<operands[1] else 0
    elif typeID==7:
        return 1 if operands[0]==operands[1] else 0
    else:
        raise ValueError
    

def part1(data=None):
    packet=loadbinary(data)
    hierarchy=parsepacket(packet)
    print(sumversionhierarchy(hierarchy))

def part2(data=None):
    packet=loadbinary(data)
    hierarchy=parsepacket(packet)
    print(evalhierarchy(hierarchy))


if __name__ == "__main__":
    # sum versions
    part1("8A004A801A8002F478")             # 16
    part1("620080001611562C8802118E34")     # 12
    part1("C0015000016115A2E0802F182340")   # 23
    part1("A0016C880162017C3686B18A3D4780") # 31
    print("part1 = ", end='')
    part1() # 986
    
    # eval expression
    part2("C200B40A82")  # 3
    part2("04005AC33890")  # 54
    part2("880086C3E88112")  # 7
    part2("CE00C43D881120")  # 9
    part2("D8005AC2A8F0") # 1
    part2("F600BC2D8F")   # 0
    part2("9C005AC2F8F0") # 0
    part2("9C0141080250320F1802104A08") # 1
    print("part2 = ", end='')
    part2()
    
