import binascii
import tkinter as tk
from tkinter import *
class AES:
    # 列混合矩阵
    MIX_C = [[0x1,0x4],[0x4,0x1]]
    I_MIXC = [[0x9,0x2], [0x2,0x9]]
    RCon = [0b10000000, 0b110000]

    S_BOX = [[0x9, 0x4, 0xA, 0xB],
             [0xD, 0x1, 0x8, 0x5],
             [0x6, 0x2, 0x0, 0x3],
             [0xC, 0xE, 0xF, 0x7]]

    I_SBOX = [[0xA, 0x5, 0x9, 0xB],
             [0x1, 0x7, 0x8, 0xF],
             [0x6, 0x0, 0x2, 0x3],
             [0xC, 0x4, 0xD, 0xE]]

    def subBytes(self, Matrix, state):  # 根据传入的Matrix确定实现字节代替(或逆字节代替)

        return [Matrix[i][j] for i, j in [((t & 0B1100)>>2, t & 0B11) for t in state]]

    def mixColumns(self, matrix, state):
        ls = []
        temp = 0x0
        for round in range(2):
            for row in range(2):  # 矩阵MIX_C的一行乘以state的每一列
                for col in range(2):
                    temp ^= self.mul_all(matrix[round][col], state[col * 2 + row])
                ls.append(temp)
                temp = 0x0
        return ls

    def shiftRows(self, s):  # 加密时的行移位
        return [s[0], s[1],
                s[3], s[2]]

    def inShiftRows(self, s):  # 逆行移位，解密时的行移位
        return [s[0], s[1],
                s[3], s[2]]
   #轮密钥加
    def addRoundKey(self, state, kw):
        ls = [0] * 4
        # for row in range(2):
        #     for col in range(2):
        #         ls[col * 2 + row] = state[col * 2 + row] ^ kw[row * 2+ col]
        for i in range(4):
            ls[i]=state[i]^kw[i]
        return ls
   #有限域乘法递归处理
    def mul_2(self, p1, p2):  # 递归处理有限域乘法(处理乘数p1的数据形如：0x1,0x2,0x4,0x8,0x10,0x20,0x40,0x80)
        if p1 == 1:  # p1为乘数,p2为被乘数
            return p2
        else:
            return (self.mul_2(p1 >> 1, (p2 << 1 & 0xf) ^ (
                0x3 if p2 & 0x8 else 0x0)))  # result=(p2<<1&0xff)^(0x1b if p2&0x80 else 0x00)中间结果项
#有限域乘法
    def mul_all(self, p1, p2):  # 有限域(G(2^4))上的乘法
        result = 0x0
        pp = p1
        temp = 0x1
        for i in range(4):
            if p1 == 0:  # 当乘数等于0的时候就跳出循环
                break
            if pp & temp:
                result ^= self.mul_2(temp, p2)
            temp <<= 1
            p1 >>= 1
        return result

    # 密钥扩展

    def keyExpansion(self,key):
        kw = [key >> 8 & 0xff, key & 0xff]+[0]*4

        # 将包含 6 个字的数组存储到数组 kw 的前 6 个位置上，其余位置置为 0
        # 依次计算出剩余的 4 个轮密钥
        for i in range(2, 6):
            temp = kw[i - 1]

            if i % 2 == 0:

                temp = self.subWord(self.rotWord(temp)) ^ self.RCon[i // 2 - 1]
            kw[i] = kw[i - 2] ^ temp

        # 将得到的轮密钥存储到 6 个字为一组的元组列表中，并返回该列表
        return [(kw[2 * i]>>4, kw[2*i] & 0xf,
                 kw[2 * i+1] >> 4, kw[2 * i+1] & 0xf)
                for i in
                range(3)]

    def rotWord(self, word):
        return ((word & 0xf) << 4) + (word >> 4)

    def subWord(self, word):
        result = 0x0
        for i in range(2):
            temp = word & 0xf0
            word <<= 4
            temp >>= 4
            result = (result << 4) + self.S_BOX[temp >> 2][temp & 0B11]
        return result
        # 加密

    def encrypt(self, text, key):
        kw = self.keyExpansion(key)

        state = self.slipt(text)

        state = self.addRoundKey(state, kw[0])

        state = self.subBytes(self.S_BOX, state)

        state = self.shiftRows(state)

        state = self.mixColumns(self.MIX_C, state)

        state = self.addRoundKey(state, kw[1])

        state = self.subBytes(self.S_BOX, state)

        state = self.shiftRows(state)

        state = self.addRoundKey(state, kw[2])
        return state

    def decrypt(self, text, key):
        kw = self.keyExpansion(key)
        state = self.slipt(text)
        state = self.addRoundKey(state, kw[2])
        state = self.inShiftRows(state)
        state = self.subBytes(self.I_SBOX, state)
        state = self.addRoundKey(state, kw[1])
        state = self.mixColumns(self.I_MIXC, state)
        state = self.inShiftRows(state)
        state = self.subBytes(self.I_SBOX, state)
        state = self.addRoundKey(state, kw[0])
        return state

    # 将输入的16字节进行划分
    def slipt(self, text):
        ls = [0] * 4
        for i in [1, 0]:
            for j in [1, 0]:
                ls[2* i + j] = text & 0b1111
                text >>= 4

        return ls
my = AES()
def str_to_hex(string):
    binary_data = string.encode()
    hex_string = binascii.hexlify(binary_data).decode()
    return hex_string
def click1():
    entry_content1 = e1.get()
    entry_content3 = e3.get()
    e4.delete("1.0", tk.END)
    entry_content1 = int(entry_content1, 2)
    entry_content3 = int(entry_content3, 2)
    s = my.encrypt(entry_content1,entry_content3)
    for num in s:
         e4.insert(INSERT, format((num), '04b'))
def click2():

    entry_content2 = e2.get()
    entry_content3 = e3.get()
    e4.delete("1.0", tk.END)
    entry_content2 = int(entry_content2, 2)
    entry_content3 = int(entry_content3, 2)
    s = my.decrypt(entry_content2, entry_content3)

    for num in s:
        e4.insert(INSERT, format((num), '04b'))


if __name__=="__main__":
 root = tk.Tk()
 root.title('My Window')
 root.minsize(300, 300)
 root.maxsize(500, 500)
 lab1=Label(root,text="  请输入16位明文：").grid(row=0)
 lab2=Label(root,text="  请输入16位暗文：").grid(row=1)
 lab3=Label(root,text="  请输入16位密钥：").grid(row=2)
 lab4=Label(root,text="  得到相应的文本：").grid(row=4)
 e1=Entry(root,width=25)
 e2=Entry(root,width=25)
 e3 = Entry(root, width=25)
 e4=tk.Text(root,width=25,height=1)

 e1.grid(row=0,column=1)
 e2.grid(row=1,column=1)
 e3.grid(row=2,column=1)
 e4.grid(row=4,column=1)

 button1=tk.Button(root,text="加密",command=click1)
 button1.grid(row=3,column=0)
 button2 = tk.Button(root, text="解密", command=click2)
 button2.grid(row=3,column=1)

 root.mainloop()
