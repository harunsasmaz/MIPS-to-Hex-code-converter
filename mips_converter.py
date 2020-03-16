opcode_dict = {
    'add':  '000000',
    'sub':  '000001',
    'mult': '000010',
    'and':  '000011',
    'or':   '000100',
    'addi': '000101',
    'sll':  '000110',
    'slt':  '000111',
    'mfhi': '001000',
    'mflo': '001001',
    'lw':   '001010',
    'sw':   '001011',
    'beq':  '001100',
    'blez': '001101',
    'j':    '001110',
    'mod':  '001111'
}

operation_type = {
    'add':  'r_type',
    'sub':  'r_type',
    'mult': 'r_type',
    'and':  'r_type',
    'or':   'r_type',
    'addi': 'i_type_branch',
    'sll':  'i_type_branch',
    'slt':  'r_type',
    'mfhi': 'r_type',
    'mflo': 'r_type',
    'lw':   'i_type_mem',
    'sw':   'i_type_mem',
    'beq':  'i_type_branch',
    'blez': 'i_type_branch',
    'j':    'j_type',
    'mod':  'r_type'
}


def decToBin(a: int, width: int) -> 'String':
    return (width - len(bin(a)[2:])) * '0' + bin(a)[2:]


def binToHex(_bin: str) -> 'String':
    return '{:0{width}x}'.format(int(_bin, 2), width=8)


def r_type(inst: str) -> '32 - Bit Word':
    
    """ 'add $5, $3, $4'\n
        'mult $5, $3'\n
        'mflo $5'\n
        'mfhi $5'"""
    
    parts = inst.split()
    
    operation = parts[0].strip(',')
    rd = parts[1].strip(',$')
    
    opcode = opcode_dict[operation]
    rd_bin = decToBin(int(rd), 5)
    
    total = opcode + rd_bin

    if operation not in ['mult', 'mfhi', 'mflo']:
        
        rs = parts[2].strip(',$')
        rt = parts[3].strip(',$')
    
        rs_bin = decToBin(int(rs), 5)
        rt_bin = decToBin(int(rt), 5)
        
        total += rs_bin + rt_bin
        full_bin = opcode + rs_bin + rt_bin + rd_bin + (32 - len(total)) * '0'
    
    elif operation == 'mult':
    
        rt = parts[2].strip(',$')
        
        rt_bin = decToBin(int(rt), 5)
    
        total += rt_bin
        full_bin = opcode + rd_bin + rt_bin + (32 - len(total)) * '0'

    else:
        total = opcode + 10 * '0' + rd_bin
        full_bin = opcode + 10 * '0' + rd_bin + (32 - len(total)) * '0'

    return binToHex(full_bin)


def j_type(inst: str) -> '32 - Bit Word':
    
    """'j <int:label>'"""
    
    parts = inst.split()
    
    operation = parts[0]
    address = parts[1]
    
    opcode = opcode_dict[operation]
    address_bin = decToBin(int(address), 26)
 
    full_bin = opcode + address_bin

    return binToHex(full_bin)


def i_type_mem(inst: str) -> '32 - Bit Word':
    
    """i_type for lw and sw -> 'lw-sw rd-rs, i(rs-rd)'"""
    
    parts = inst.split()
    
    operation = parts[0]
    reg_add_1 = parts[1].strip('$,')
    reg_add_2 = parts[2].strip(')').split('(')[1].strip('$')
    offset = parts[2].strip(')').split('(')[0]
    
    opcode = opcode_dict[operation]
    reg_add_1_bin = decToBin(int(reg_add_1), 5)
    reg_add_2_bin = decToBin(int(reg_add_2), 5)
    offset_bin = decToBin(int(offset), 16)
    
    full_bin = opcode + reg_add_2_bin + reg_add_1_bin + offset_bin
 
    return binToHex(full_bin)


def i_type_branch(inst: str) -> '32 - Bit Word':
    
    """
    i_type for branch -> beq and blez. 
    beq -> 'beq rs rt label<int>'.
    blez -> 'blez rs label<int>'.
    """
    
    parts = inst.split()
    operation = parts[0]
    
    full_bin = opcode_dict[operation]
    
    if operation == 'beq' or operation == 'addi' or operation == 'sll':
        
        rs = parts[1].strip('$,')
        rt = parts[2].strip('$,')
        address = parts[3]
        
        rs_bin = decToBin(int(rs), 5)
        rt_bin = decToBin(int(rt), 5)
        address_bin = decToBin(int(address), 16)
         
        full_bin += rt_bin + rs_bin + address_bin
    
    elif operation == 'blez':
        
        rs = parts[1].strip('$,')
        address = parts[2]
        
        rs_bin = decToBin(int(rs), 5)
        address_bin = decToBin(int(address), 21)
        
        full_bin += rs_bin + address_bin

    return binToHex(full_bin)


def convert(inst: str) -> '32 - Bit Word':

    try:
        operation = inst.split(" ")[0]

        inst_type = operation_type[operation]

        if inst_type == 'r_type':
            return r_type(inst)
        elif inst_type == 'i_type_mem':
            return i_type_mem(inst)
        elif inst_type == 'i_type_branch':
            return i_type_branch(inst)
        elif inst_type == 'j_type':
            return j_type(inst)
        else:
            return "Unknown"

    except:
        
        return "Something went wrong!"


if __name__ == "__main__":
    
    input_ = input("Enter a instruction: ('exit' to leave!): ")

    while input_ != 'exit':

        print(convert(input_))
        input_ = input("Enter a instruction: ('exit' to leave!): ")
