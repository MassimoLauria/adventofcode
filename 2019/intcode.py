#Intcode



def IntCode(code,Input,printcode=False):
    CPU=IntCodeCPU(code)
    CPU.add_input(Input)
    CPU.run(printcode=printcode)
    if CPU.is_waiting():
        raise ValueError("Not enough input to finish the computation")
    return CPU.get_output()

class IntCodeCPU():

    def __init__(self,code):
        self.code=None
        self.Output=[]
        self.Input=[]
        self.Inputptr=0
        self.pc=0;
        self.status="READY"
        self.relative_base=0
        if isinstance(code,str):
            # use strings "32,1,4,6,-4,2" as input
            self.code=[int(x) for x in code.split(',')]
        elif hasattr(code, "readlines"):
            code.seek(0)
            lines=[l.strip() for l in code.readlines()]
            text="".join(lines)
            data=text.split(",")
            self.code=[int(x) for x in data]
        else:
            self.code=code[:]
        # Turn it into a dict
        dcode={}
        for i in range(len(self.code)):
            dcode[i]=self.code[i]
        self.code=dcode
        

    @staticmethod
    def decmask(x,pos):
        x //= 10**pos
        return x % 10
    
    def getmem(self,i,mode):
        codei=self.code.get(i,0)
        if mode==0: # position mode
            return self.code.get(codei,0)
        elif mode==1: # immediate mode
            return codei
        elif mode==2: # relative mode
            return self.code.get(codei+self.relative_base, 0)
        else:
            raise ValueError("Invalid read mode {mode}")
        
    def writemem(self,i,mode,data):
        codei=self.code.get(i,0)
        if mode==0: # position mode
            dest = codei
        elif mode==2: # relative mode
            dest = codei+self.relative_base
        else:
            raise ValueError("Invalid write mode {mode}")
        self.code[dest]=data

    def is_waiting(self):
        return self.status=="WAITING"
    
    def halted(self):
        return self.status=="HALT"
    
    def add_input(self,x):
        self.Input.extend(x)
        
    def get_output(self):
        return self.Output[:]
    
    def flush_output(self):
        self.Output=[]
    
    def run(self,printcode=False):
        
        if self.status=="READY":
            self.pc=0

        i = self.pc
        code=self.code
        while True:
            opcode = code[i] % 100
            modep1=self.decmask(code[i],2)
            modep2=self.decmask(code[i],3)
            modep3=self.decmask(code[i],4)
        
            if opcode==1: # sum
                if printcode: print("sum  - ",code[i:i+4])
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                self.writemem(i+3,modep3,p1+p2)
                i += 4
            
            elif opcode==2: # mult
                if printcode: print("mult - ",code[i:i+4])
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                self.writemem(i+3,modep3,p1*p2)
                i += 4
                 
            elif opcode==3: # read at address
            
                if printcode: print("read - ",code[i:i+2],end="")
            
                if self.Inputptr >= len(self.Input):
                    #raise ValueError("Input read at address {} invalid: no more data".format(i))
                    self.status="WAITING"
                    self.pc=i
                    return
            
                val = self.Input[self.Inputptr]
                self.writemem(i+1,modep1,val)
                #dest=code[i+1]
                #code[dest] = self.Input[self.Inputptr]
                if printcode: print(" - reading ", self.Input[self.Inputptr])
                self.Inputptr += 1
                i +=2
            
            elif opcode==4: # output from addess
                if printcode: print("prnt - ",code[i:i+2], end="")
                p1=self.getmem(i+1,modep1)
                self.Output.append(p1)
                if printcode: print(" - printing output:", p1)
                i +=2
            
            elif opcode==5: # jump if non zero
                if printcode: print("jnz  - ",code[i:i+3], end="")
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                i = p2 if p1!=0 else i+3
        
            elif opcode==6: # jump if zero
                if printcode: print("jz   - ",code[i:i+3], end="")
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                i = p2 if p1==0 else i+3

            elif opcode==7: # less
                if printcode: print("less - ",code[i:i+4])
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                self.writemem(i+3,modep3,1 if p1<p2 else 0)
                i += 4

            elif opcode==8: # equal
                if printcode: print("equ  - ",code[i:i+4])
                p1=self.getmem(i+1,modep1)
                p2=self.getmem(i+2,modep2)
                self.writemem(i+3,modep3,1 if p1==p2 else 0)
                i += 4
        
            elif opcode==9: # relative base
                if printcode: print("base - ",code[i:i+2])
                p1=self.getmem(i+1,modep1)
                self.relative_base += p1
                i += 2
        
            elif opcode==99:
                if printcode: print("halt - ",code[i:i+1])
                self.status="HALT"
                return
            else:
                raise ValueError("Unrecognized opcode {} at address {}".format(opcode,i))

