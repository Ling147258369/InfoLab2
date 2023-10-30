from main import  *
my=AES()
# 实现双重加密解密
def double_encrypt(text, key1, key2):

    plain_text1 = my.encrypt(text, key1)
    print(plain_text1)
    plain_text1=list_to_binary(plain_text1)
    print(plain_text1)
    plain_text1=int(plain_text1,16)
    print(plain_text1)
    plain_text2 = my.encrypt(plain_text1, key2)
    print(plain_text2)
    plain_text2=list_to_binary(plain_text2)
    plain_text2 = int(plain_text2, 16)
    return plain_text2
def double_decrypt(cipher_text, key1, key2):
    plain_text1 = my.decrypt(cipher_text, key2)
    plain_text1=list_to_binary(plain_text1)
    plain_text1=int(plain_text1,16)

    plain_text2 = my.decrypt(plain_text1, key1)
    plain_text2=list_to_binary(plain_text2)
    plain_text2 = int(plain_text2, 16)
    return plain_text2
# 实现三重加密解密
def triple_encrypt(text, key1, key2,key3):

    plain_text1 = my.encrypt(text, key3)
    plain_text1=list_to_binary(plain_text1)
    plain_text1=int(plain_text1,16)
    plain_text2 = my.encrypt(plain_text1, key2)
    plain_text2=list_to_binary(plain_text2)
    plain_text2 = int(plain_text2, 16)
    plain_text3=my.encrypt(plain_text2,key1)
    plain_text3=list_to_binary(plain_text3)
    plain_text3 = int(plain_text3, 16)
    return plain_text3

def triple_decrypt(cipher_text, key1, key2,key3):

    plain_text1 = my.decrypt(cipher_text, key1)
    plain_text1=list_to_binary(plain_text1)
    plain_text1=int(plain_text1,16)
    plain_text2 = my.decrypt(plain_text1, key2)
    plain_text2=list_to_binary(plain_text2)
    plain_text2 = int(plain_text2, 16)
    plain_text3=my.decrypt(plain_text2,key3)
    plain_text3=list_to_binary(plain_text3)
    plain_text3 = int(plain_text3, 16)
    return plain_text3

def list_to_binary(my_list):
    binary_string = ""
    for item in my_list:
        binary = hex(item)
        binary_string += binary[2:]
    return binary_string
text = 0xabcd
key1 =  0b1000000000000001
key2 =  0b1010011100111011
key3 = 0b1000111010111011
print("密钥1：", bin(key1))
print("密钥2：",bin( key2))
print("密钥3：",bin( key3))
print("-----------------")
print("测试双重加密解密:")
cipher_text = double_encrypt(text, key1, key2)
mingwen=double_decrypt(cipher_text, key1, key2)
print("初始明文：",hex(text))
print("加密后得到的密文：", hex(cipher_text))
print("初始的密文：", hex(cipher_text))
print("解密后得到的明文：",hex(mingwen))
print("-----------------")
print("测试三重加密解密:")
cipher_text1 = triple_encrypt(text, key1, key2,key3)
mingwen1=triple_decrypt(cipher_text1, key1, key2,key3)
print("初始明文：",hex(text))
print("加密后得到的密文：",hex(cipher_text1))
print("初始密文：", hex(cipher_text1))
print("解密后得到的明文：", hex(mingwen1))


