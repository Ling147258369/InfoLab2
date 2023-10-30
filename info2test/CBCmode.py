from main import  *
my=AES()
def list_to_binary(my_list):
    binary_string = ""
    for item in my_list:
        binary = hex(item)
        binary_string += binary[2:]
    return binary_string
def xor_bytes1(a, b):

     return    a^b
key = 0b1010101010101010  # 16字节的密钥
iv = 0b1010101010101010  # 16字节的初始化向量
plaintext ='10101010101010101010101010101010'  # 明文消息

    # 分割明文消息为多个分组
plaintext_blocks = [plaintext[i:i+15] for i in range(0, len(plaintext), 16)]

    # 加密每个分组，并将加密结果链接在一起
previous_block = iv
ciphertext = ''
for block in plaintext_blocks:
        # XOR前一分组的密文和当前分组的明文
        block=int(block,2)
        plaintext_block = xor_bytes1(block, previous_block)
        # 加密
        encrypted_block = my.encrypt(key, plaintext_block)
        encrypted_block=list_to_binary(encrypted_block)
        ciphertext += encrypted_block
        encrypted_block=int(encrypted_block,16)
        # 更新前一分组的密文
        previous_block =int("{0:b}".format(encrypted_block))

    # 输出加密后的结果
print("加密后的消息：", ciphertext)
    # 解密加密后的消息
decrypted_message = ''
previous_block = iv
for i in range(0, len(ciphertext),2):

        encrypted_block = ciphertext[i:i+2]

        encrypted_block=int(encrypted_block,16)
        #print(encrypted_block)
        decrypted_block = my.decrypt(key, encrypted_block)
        #print(decrypted_block)
        decrypted_block=list_to_binary(decrypted_block)
        #print(decrypted_block)
        decrypted_block=int(decrypted_block,16)
        #print(decrypted_block)
        decrypted_block=int(bin(decrypted_block)[2:])

        # XOR前一分组的密文和当前分组的解密结果
        plaintext_block = xor_bytes1(decrypted_block, previous_block)
        plaintext_block=str(bin(plaintext_block))


        decrypted_message=''

        decrypted_message += plaintext_block
        # 更新前一分组的密文
        previous_block = encrypted_block

       # 输出解密后的结果
print("解密后的消息：", decrypted_message)
