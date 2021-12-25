
def getpassports(fname):
    '''Read the passport files

Produces list of dictionaries, each containing
all the entries of a passport, according to
https://adventofcode.com/2020/day/4
'''
    passportlist=[]
    pport=None
    with open(fname) as f:
        for line in f:
            if line in ['\n','']:
                if pport is not None: # finish passport
                    passportlist.append(pport)
                    pport=None
                continue
            
            if pport is None: # create passport if needed
                pport ={}
            
            for items in line.split():
                field,data = items.split(':')
                field = field.strip()
                data  = data.strip()
                pport[field]=data
        
        if pport is not None:
            passportlist.append(pport)
    return passportlist


def valid_byr(pport):
    return ('byr' in pport) and len(pport['byr'])==4 and (1920 <= int(pport['byr']) <=2002)
    
def valid_iyr(pport):
    return 'iyr' in pport and len(pport['iyr'])==4 and 2010 <= int(pport['iyr']) <=2020

def valid_eyr(pport):
    return 'eyr' in pport and len(pport['eyr'])==4 and 2020 <= int(pport['eyr']) <=2030

def valid_hgt(pport):
    if 'hgt' not in pport:
        return False
    unit=pport['hgt'][-2:]
    value=pport['hgt'][:-2]
    if not value.isdigit():
        return False
    else:
        value=int(value)
    if unit=='cm':
        return 150 <= value <= 193
    elif unit=='in':
        return 59 <= value <= 76
    else:
        return False


def valid_hcl(pport):
    if 'hcl' not in pport:
        return False
    text=pport['hcl']
    if text[0]!='#':
        return False
    for c in text[1:]:
        if c not in '0123456789abcdef':
            return False
    return True
    

def valid_ecl(pport):
    return 'ecl' in pport and pport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def valid_pid(pport):
    return 'pid' in pport and len(pport['pid'])==9 and pport['pid'].isdigit()


def valid_cid(pport):
    return True


def part1():
    D = getpassports('aoc4input.txt')
    valid=0
    for pport in D:
        if len(pport)==8 or len(pport)==7 and 'cid' not in pport:
            valid += 1
        
    print(valid)
    

def part2():
    D = getpassports('aoc4input.txt')

    vfunc = [valid_byr,
             valid_iyr,
             valid_eyr,
             valid_hgt,
             valid_hcl,
             valid_ecl,
             valid_pid,
             valid_cid]

    valid=0
    for pport in D:
        X= [f(pport) for f in vfunc]
        if all(X):
            valid += 1
        
    print(valid)
    
part1()
part2()