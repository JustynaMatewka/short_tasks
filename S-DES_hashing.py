def ls(key):    #przeniesienie 1 znaku na koniec
    h = key[0]
    h_2 = key[1:]
    key = h_2 + h
    return key

def per_extange(r, per):    #dowolna permutacja
    per_text = ""
    for x in per:
        per_text += r[int(x - 1)]
    return per_text

def value1_xor_value2(value_1, value_2):    #dowolny xor 2 wartości jednakowej długości
    values_xor = ""
    for x in range(len(value_1)):
        values_xor += str(int(value_1[x]) ^ int(value_2[x]))
    return values_xor

def bin_to_int(string):
    i = 0
    for x in range(len(string)):
        i += int(string[-(x + 1)]) * pow(2, x)
    return i

def sboxs(text, sbox):
    a = sbox[bin_to_int(text[0] + text[-1])][bin_to_int(text[1:-1])]
    return a

def int_to_bin(n):
    bin_n = ""
    while n >= 1:
        bin_n = str(n % 2) + bin_n
        n = n // 2
    
    while len(bin_n) != 2:
        bin_n = "0" + bin_n
    
    return bin_n

def sbox_tab(sbox): #z pobranych sboxów tworzy tablicę 2-wymiarową
    generated_sbox_tab = []
    for row in sbox:
        help_tab = []

        for value in row:
            help_tab.append(int_to_bin(int(value)))
        generated_sbox_tab.append(help_tab)
    
    return generated_sbox_tab

def generate_keys(key, p_10, p_8, p_4): #generuje 2 klucze poprawnie
    result = ""
    result = per_extange(key, p_10)

    result = ls(result[0:(len(result) // 2)]) + ls(result[(len(result) // 2):])
    k_1 = per_extange(result, p_8)

    result = ls(ls(result[0:(len(result) // 2)])) + ls(ls(result[(len(result) // 2):]))
    k_2 = per_extange(result, p_8)

    return [k_1, k_2]

def round(text, ip, ep, p_4, key, sbox_1, sbox_2):
    half_2 = text[(len(text) // 2):]
    half_2 = per_extange(half_2, ep)
    half_2 = value1_xor_value2(half_2, key)

    s_0 = half_2[0:(len(half_2) // 2)]
    s_0 = sbox_1[bin_to_int(s_0[0] + s_0[-1])][bin_to_int(s_0[1:-1])]

    s_1 = half_2[(len(half_2) // 2):]
    s_1 = sbox_2[bin_to_int(s_1[0] + s_1[-1])][bin_to_int(s_1[1:-1])]

    half_2 = per_extange((s_0 + s_1), p_4)
    return value1_xor_value2(text[0:(len(text) // 2)], half_2) + text[(len(text) // 2):]

def inverse_ip(ip):
    return [ip[4], ip[3], ip[2], ip[6], ip[7], ip[0], ip[5], ip[1]]

def prepare_image(image_path, tryb):
    with open(image_path, 'rb') as f:
        special_lines = []

        for line in f:
            if len(line) < 12: 
                #print(line, len(line))
                special_lines.append(line)
            else:
                #print(line[:-1], len(line))
                line = ''.join(format(byte, '08b') for byte in line)  #Konwersja na binarną
                
                while len(line) % 12 != 0:  #Odrzucenie niepotrzebnych bitów
                    line = line[0:-1]

                blocks = [line[i:i+12] for i in range(0, len(line), 12)] #Podział tekstu jawnego na bloki

                write_image_result(blocks, special_lines, tryb)

def write_image_result(hash_part, special_lines, tryb):
    with open("C:/Users/hp/Downloads/washington_hash_result.pbm", 'ab') as wf:
        for x in special_lines:
            wf.write(x)
        h = hash_image(hash_part, tryb)
        hash_bytes = int(h, 2).to_bytes((len(h) + 7) // 8, byteorder='big')
        wf.write(hash_bytes)
        wf.write(b'\n')

def hash_image(blocks, tryb):
    key = "1010000010"
    iv = "11101010"
    p_10 = [3,5,2,7,4,10,1,9,8,6]
    p_8 = [6,3,7,4,8,5,10,9]
    p_4 = [2,4,3,1]
    ip = [2,6,3,1,4,8,5,7]
    ep = [4,1,2,3,2,3,4,1]
    sbox_1 = ("1032 3210 0213 3132").split()
    sbox_1 = sbox_tab(sbox_1)
    sbox_2 = ("0123 2013 3010 2103").split()
    sbox_2 = sbox_tab(sbox_2)
    result = ""

    for block in blocks:

        #IV  XOR l + r (block)
        if tryb == "CBC":
            block = value1_xor_value2(iv, block)
        
        key_new = key
        #Generowanie 2 kluczy:
        keys = generate_keys(key_new, p_10, p_8, p_4)

        #Obie rundy:
        block = per_extange(block, ip)
        block = round(block, ip, ep, p_4, keys[1], sbox_1, sbox_2)
        block = block[(len(block) // 2):] + block[0:(len(block) // 2)]
        block = round(block, ip, ep, p_4, keys[0], sbox_1, sbox_2)
        block = per_extange(block, inverse_ip(ip))

        iv = block[(len(block) // 2):] + block[0:(len(block) // 2)]
        result += block
    
    return result


if __name__ == '__main__':
    image_path = "C:/Users/hp/Downloads/washington.pbm"
    tryb = input()
    prepare_image(image_path, tryb)
