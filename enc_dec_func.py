import random
import hashlib

Code = {-15-15j: '5b', -15-13j: '5a', -15-11j: 'd1', -15-9j: '54', -15-7j: '99', -15-5j: 'cc', -15-3j: 'b1', -15-1j: 'e4', -15+1j: '20', -15+3j: 'b3', -15+5j: '61', -15+7j: '79', -15+9j: '1d', -15+11j: 'd3', -15+13j: '10', -15+15j: '6e',
        -13-15j: '9e', -13-13j: '63', -13-11j: 'dd', -13-9j: '7e', -13-7j: 'f6', -13-5j: '3d', -13-3j: 'f5', -13-1j: '06', -13+1j: '72', -13+3j: '7f', -13+5j: '38', -13+7j: '64', -13+9j: '00', -13+11j: '77', -13+13j: '04', -13+15j: '1a',
        -11-15j: 'e2', -11-13j: '5d', -11-11j: 'd4', -11-9j: '3f', -11-7j: '0d', -11-5j: '4a', -11-3j: '0f', -11-1j: '6f', -11+1j: 'f7', -11+3j: 'c0', -11+5j: '8c', -11+7j: 'c3', -11+9j: '91', -11+11j: '2d', -11+13j: 'd2', -11+15j: '93',
        -9-15j: '70', -9-13j: '22', -9-11j: '8d', -9-9j: '3b', -9-7j: '36', -9-5j: '11', -9-3j: 'f0', -9-1j: '1f', -9+1j: '31', -9+3j: '9c', -9+5j: '44', -9+7j: '92', -9+9j: '74', -9+11j: 'ec', -9+13j: '71', -9+15j: '98',
        -7-15j: 'e1', -7-13j: 'e7', -7-11j: 'e3', -7-9j: 'b5', -7-7j: '7a', -7-5j: 'a1', -7-3j: 'ff', -7-1j: 'ed', -7+1j: '39', -7+3j: 'dc', -7+5j: '81', -7+7j: 'bd', -7+9j: '29', -7+11j: 'f8', -7+13j: '7c', -7+15j: '94',
        -5-15j: '9a', -5-13j: '76', -5-11j: '4f', -5-9j: 'ab', -5-7j: '97', -5-5j: 'de', -5-3j: 'c4', -5-1j: '18', -5+1j: 'a4', -5+3j: '88', -5+5j: 'ef', -5+7j: '80', -5+9j: '84', -5+11j: '43', -5+13j: '23', -5+15j: '33',
        -3-15j: 'fd', -3-13j: '35', -3-11j: '5e', -3-9j: '65', -3-7j: '52', -3-5j: '2b', -3-3j: '0e', -3-1j: 'ba', -3+1j: '30', -3+3j: '32', -3+5j: 'd8', -3+7j: '47', -3+9j: '4b', -3+11j: '13', -3+13j: '27', -3+15j: '6a',
        -1-15j: '05', -1-13j: '8e', -1-11j: '17', -1-9j: '2e', -1-7j: '7d', -1-5j: '1e', -1-3j: '51', -1-1j: '21', -1+1j: '60', -1+3j: 'b0', -1+5j: '86', -1+7j: '28', -1+9j: '83', -1+11j: '0a', -1+13j: '6d', -1+15j: 'af',
        1-15j: '26', 1-13j: '1c', 1-11j: 'fb', 1-9j: 'c8', 1-7j: '34', 1-5j: 'c7', 1-3j: 'b8', 1-1j: 'ea', 1+1j: '08', 1+3j: '03', 1+5j: '46', 1+7j: 'd7', 1+9j: 'ad', 1+11j: '0b', 1+13j: 'a3', 1+15j: 'bb',
        3-15j: '2c', 3-13j: '6b', 3-11j: '2f', 3-9j: 'be', 3-7j: '95', 3-5j: '16', 3-3j: '8b', 3-1j: 'df', 3+1j: 'cf', 3+3j: '67', 3+5j: '56', 3+7j: 'ee', 3+9j: '68', 3+11j: '66', 3+13j: 'e9', 3+15j: '78',
        5-15j: '02', 5-13j: '5c', 5-11j: '40', 5-9j: '75', 5-7j: 'da', 5-5j: '37', 5-3j: 'f1', 5-1j: '07', 5+1j: '7b', 5+3j: '01', 5+5j: '85', 5+7j: 'ac', 5+9j: 'a7', 5+11j: 'a0', 5+13j: 'a2', 5+15j: 'b7',
        7-15j: 'd9', 7-13j: 'f2', 7-11j: 'f9', 7-9j: '58', 7-7j: 'ca', 7-5j: '89', 7-3j: 'c9', 7-1j: 'aa', 7+1j: '4c', 7+3j: '57', 7+5j: 'c2', 7+7j: '1b', 7+9j: 'a9', 7+11j: '73', 7+13j: 'e0', 7+15j: '45',
        9-15j: 'cd', 9-13j: '59', 9-11j: 'a8', 9-9j: '4d', 9-7j: 'b9', 9-5j: '48', 9-3j: '41', 9-1j: '49', 9+1j: 'f3', 9+3j: '25', 9+5j: 'eb', 9+7j: 'ae', 9+9j: '96', 9+11j: '90', 9+13j: '9d', 9+15j: '8f',
        11-15j: 'c6', 11-13j: 'a6', 11-11j: 'd0', 11-9j: '62', 11-7j: 'bc', 11-5j: '3e', 11-3j: '6c', 11-1j: '5f', 11+1j: 'b2', 11+3j: 'fc', 11+5j: '0c', 11+7j: '8a', 11+9j: 'ce', 11+11j: 'b4', 11+13j: '9b', 11+15j: '50',
        13-15j: 'e8', 13-13j: 'cb', 13-11j: '24', 13-9j: '9f', 13-7j: '87', 13-5j: 'db', 13-3j: 'c5', 13-1j: 'd5', 13+1j: 'e6', 13+3j: '19', 13+5j: '2a', 13+7j: 'c1', 13+9j: '14', 13+11j: '4e', 13+13j: 'a5', 13+15j: 'd6',
        15-15j: '12', 15-13j: 'fa', 15-11j: '69', 15-9j: 'f4', 15-7j: 'e5', 15-5j: '15', 15-3j: '82', 15-1j: '3a', 15+1j: 'fe', 15+3j: '3c', 15+5j: 'bf', 15+7j: 'b6', 15+9j: '53', 15+11j: '42', 15+13j: '55', 15+15j: '09'}

def shuffle_dict_by_string(dic, s):
    keys = list(dic.keys())
    values = list(dic.values())

    # 문자열을 기반으로 시드값 생성
    seed = int(hashlib.sha256(s.encode()).hexdigest(), 16)
    random.seed(seed)

    # 값을 섞기
    shuffled_values = values[:]
    random.shuffle(shuffled_values)

    # 새로운 딕셔너리 생성
    shuffled_dic = dict(zip(keys, shuffled_values))
    return shuffled_dic

def Encoding(input_str, password):
    code_table = shuffle_dict_by_string(Code, password)
    hex_str = ''
    seed = 0
    for i in input_str:
        if ord(i) < 256:
            hex_str += format(ord(i), '02x')
        else:
            hex_str += format(ord(i), '06x')
        seed += ord(i)
    # print(encoded)
    seed2 = seed%2

    random.seed(seed)
    rand_num = random.randint(15, 84) + random.randint(15, 84)*1j
    limit_real = random.randint(int(rand_num.real)+16, 100)
    limit_imag = random.randint(int(rand_num.imag)+16, 100)
    
    result = ''
    temp = 0
    for i in range(len(hex_str)//2):
        for key, value in code_table.items():
            if value == hex_str[2*i:2*(i+1)]:
                temp += (-1)**seed2 * key + rand_num
                temp = int(temp.real)%limit_real + (int(temp.imag)%limit_imag)*1j
                result += str(temp) + ','
                break
        
        result = result.replace("(","")
        result = result.replace(")","")

    result = result.rstrip(',')
    return seed + (3-seed2)*seed, result

def Decoding(input_seed, encoded_str, password):
    code_table = shuffle_dict_by_string(Code, password)
    seed = int(input_seed)
    if seed%2 == 0: seed = seed // 4
    else: seed = seed // 3
    seed2 = seed%2
    random.seed(seed)
    rand_num = random.randint(15, 84) + random.randint(15, 84)*1j
    limit_real = random.randint(int(rand_num.real)+16, 100)
    limit_imag = random.randint(int(rand_num.imag)+16, 100)

    code_list = [complex(num) for num in encoded_str.split(',')]

    decoded = [(-1)**seed2 * (code_list[0] - rand_num)]
    for i in range(len(code_list)-1):
        decoded.append((-1)**seed2 * (code_list[i+1] - code_list[i] - rand_num))
    
    for index, value in enumerate(decoded):
        if int(value.real) < -15: decoded[index] = value + limit_real
        elif int(value.real) > 15: decoded[index] = value - limit_real
    for index, value in enumerate(decoded):
        if int(value.imag) < -15: decoded[index] = value + limit_imag*1j
        elif int(value.imag) > 15: decoded[index] = value - limit_imag*1j

    ascii_result = ''
    for i in decoded:
        try: ascii_result += code_table[i]
        except: print('Wrong code table'); return
    # print(ascii_result)

    result = ''
    ascii_index = 0
    while (ascii_index < len(ascii_result)//2):
        temp = ascii_result[2*ascii_index:2*ascii_index+2]
        if temp != '00':
            result += chr(int(temp, 16))
            ascii_index += 1
        else:
            result += chr(int(ascii_result[2*ascii_index+2:2*ascii_index+6], 16))
            ascii_index += 3

    return result

# # --- test code ---
# a = input('password: ')
# seed, encoded_string = Encoding('This is test string, 이것은 테스트입니다.', a)
# print(seed)
# print(encoded_string)
# b = input('password: ')
# result = Decoding(seed, encoded_string, b)
# print(result)
