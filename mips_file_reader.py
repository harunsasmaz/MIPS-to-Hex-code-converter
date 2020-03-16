from mips_converter import convert

def inst_txt_to_inst_list(file_name: str) -> 'List':
    
    inst_list = []
    
    with open(file_name, 'r') as file:
    
        for line in file:
            inst = line.split('#')[0].strip()
            if len(inst) != 0: 
                inst_list.append(inst)
                
    return inst_list
    

def change_label_to_int(inst: str, labels: dict) -> 'String':
    
    """j loop -> j <int:lineNumber>"""

    inst_list = inst.split()
    
    for label in labels.keys():
        if label in inst_list:
            inst_list = inst_list[:-1]
            inst_list.append(str(labels[label]))
    
    return " ".join(inst_list)


def detect_labels_and_remove(inst_list: list) -> 'List':
    
    new_inst_list = []
    labels = {}
    
    for inst in inst_list:
        if inst[-1] == ':':
            labels[inst.split()[-1][:-1]] = inst_list.index(inst) - len(labels)
    
    for inst in inst_list:
        if inst[-1] != ':':
            new_inst_list.append(change_label_to_int(inst, labels))
            
    return new_inst_list


def inst_to_out_txt(inst_list: list, file_name: str) -> 'Instruction Hex Txt':
    
    with open(file_name, 'w') as file:
        file.write('v2.0 raw' + '\n')
        for inst in inst_list:
            file.write(convert(inst) + '\n')    


def convert_to_hex(input_file: str, output_file: str) -> 'Instruction Hex Txt':

    inst_list = inst_txt_to_inst_list(input_file)
    inst_list_wo_labels = detect_labels_and_remove(inst_list)
    inst_to_out_txt(inst_list_wo_labels, output_file)

if __name__ == "__main__":
    
    try:

        input_file = input("Enter the file name: ")
        output_file = input("Enter output hex file name: ")

        output_file += "_hex.txt"

        convert_to_hex(input_file, output_file)
        print("Convertion is done.")

    except:

        print("Check the file name!")
        





