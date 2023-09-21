import secrets
import tkinter as tk
import tkinter.messagebox
from tkinter import *
import threading
import time

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# 明文转成二进制
def text2binary(text):
    iBinary = ""
    for char in text:
        ascii_code = ord(char)
        binary_code = bin(ascii_code)[2:]  # 去掉二进制字符串前面的"0b"前缀
        if len(binary_code) > 8:
            return 0
        binary_code = binary_code.zfill(8)  # 在不足八位的二进制数前面填充零
        iBinary += binary_code
    return iBinary


# 子密钥k[i]的生成
def subkey(origin):
    p_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    p_8 = [6, 3, 7, 4, 8, 5, 10, 9]
    leftShift01 = [2, 3, 4, 5, 1]
    leftShift02 = [3, 4, 5, 1, 2]
    temp = []
    # 按p10轮转对密钥进行处理
    for i in range(10):
        temp.append(int(origin[p_10[i] - 1]))
    k1 = []
    k2 = []
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    # 获得k1
    # 对密钥的左半边进行leftShift1
    for i in range(5):
        temp01.append(temp[leftShift01[i] - 1])
    # 对密钥的右半边进行leftShift1
    for i in range(5):
        temp02.append(temp[leftShift01[i] + 4])
    # 合并得到子密钥k1
    for i in range(8):
        k1.append((temp01 + temp02)[p_8[i] - 1])
    # 计算并获得k2
    for i in range(5):
        temp03.append(temp[leftShift02[i] - 1])
    for i in range(5):
        temp04.append(temp[leftShift02[i] + 4])
    for i in range(8):
        k2.append((temp03 + temp04)[p_8[i] - 1])
    return [k1, k2]


# 初始置换，即IP函数
def permutation(origin):
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    temp = []
    for index in range(8):
        temp.append(int(origin[ip[index] - 1]))
    return temp


# 最终置换，即IP^(-1)函数
def permutation_reverse(origin):
    ip_reverse = [4, 1, 3, 5, 7, 2, 8, 6]
    temp = []
    for index in range(8):
        temp.append(int(origin[ip_reverse[index] - 1]))
    return temp


# 二进制转换
def binary(a):
    if a == 3:
        return [1, 1]
    elif a == 2:
        return [1, 0]
    elif a == 1:
        return [0, 1]
    else:
        return [0, 0]


# 轮函数，输入的值分别为处理后的明文和子密钥
def round_function(originKey, k):
    # 将输入的内容分成L和R，其中origin_split是L
    origin = []
    origin_split = []
    for index in range(4):
        origin_split.append(int(originKey[index]))
    for index in range(4):
        origin.append(int(originKey[index + 4]))
    EPBox = [4, 1, 2, 3, 2, 3, 4, 1]
    SBox01 = [(1, 0, 3, 0), (3, 2, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)]
    SBox02 = [(0, 1, 2, 3), (2, 3, 1, 0), (3, 0, 1, 2), (2, 1, 0, 3)]
    SPBox = [2, 4, 3, 1]
    key_right = []
    # 对R半边进行拓展
    for index in range(8):
        key_right.append(int(origin[EPBox[index] - 1]))
    # 进行轮转置换
    for index in range(8):
        if k[index] == key_right[index]:
            key_right[index] = 0
        else:
            key_right[index] = 1
    # 找到在矩阵中对应位置
    flag01 = key_right[0] * 2 + key_right[3] * 1
    flag02 = key_right[1] * 2 + key_right[2] * 1
    flag03 = key_right[4] * 2 + key_right[7] * 1
    flag04 = key_right[5] * 2 + key_right[6] * 1
    key_right01 = SBox01[flag01][flag02]
    key_right02 = SBox02[flag03][flag04]
    ans = binary(key_right01) + binary(key_right02)
    key_left = []
    # 轮转
    for index in range(4):
        key_left.append(ans[SPBox[index] - 1])
    # 异或
    for index in range(4):
        if key_left[index] == origin_split[index]:
            key_left[index] = 0
        else:
            key_left[index] = 1
    # 左右合并
    return key_left + origin


# 左右互换SW，输入一段8-bit的密文，函数会将其左右4-bit的内容调换
def swapper(origin):
    temp01 = []
    temp02 = []
    for index in range(4):
        temp01.append(origin[index])
    for index in range(4):
        temp02.append(origin[index + 4])
    return temp02 + temp01


# 获取密钥函数
def generate_key(length):
    key = secrets.randbits(length)
    key_bin = bin(key).replace('0b', '').zfill(10)
    return key_bin


# 判断是否为2的次方
def is_power_of_two(n):
    return n != 0 and (n & (n - 1)) == 0


class Welcome(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('600x400+900+450')  # 设置窗口大小
        self.commandStr = ttk.StringVar()
        self.createPage()

    def encryption_command(self):
        self.page.destroy()
        Encryption(self.root)

    def decryption_command(self):
        self.page.destroy()
        Decryption(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)
        sWelcome = tk.Label(self.page, text='S-DES密码系统', height=3, width=200,
                            bg='white',
                            font=('黑体', 16))
        sWelcome.pack(padx=40, pady=40)
        combobox = ttk.Combobox(self.page, textvariable=self.commandStr)  # 获取用户输入的信息
        combobox['value'] = ('加密', '解密', '获取密钥', 'Crack')  # 组合框显示的选项
        combobox.current(0)
        combobox.pack(padx=5, pady=10)
        combobox.place(x=220, y=150)  # 组合框的位置和大小

        getStr = ['加密', '解密', '获取密钥', 'Crack']

        def get_command():
            for index in range(len(getStr)):
                if self.commandStr.get() == getStr[index]:
                    temp = index
                    break
                else:
                    temp = 5
            if temp == 0:
                self.page.destroy()
                Encryption(self.root)
            elif temp == 1:
                self.page.destroy()
                Decryption(self.root)
            elif temp == 2:  # 获取密钥
                self.page.destroy()
                Welcome(self.root)
                key = str(generate_key(10))
                tk.messagebox.showinfo('Key Generated', '密钥请妥善保管:' + key)
            elif temp == 3:
                self.page.destroy()
                Crack(self.root)
            else:
                tk.messagebox.showerror('错误', '不提供该类型服务')

        func = tk.Label(self.page, text='操作类型', width=9, height=2, font=('黑体', 10), bg='white')
        func.place(x=100, y=145)

        # “查询”按钮的设计
        iGet1 = ttk.Button(self.page, text='    操作    ', bootstyle=(INFO, OUTLINE), command=get_command)
        iGet1.pack(padx=5, ipady=10)
        iGet1.place(x=250, y=240)  # 设计按钮的样式，大小和位置


class Encryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('600x450+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        var = IntVar()
        var.set(1)  # 默认输入为二进制,用于判断哪个按钮被选中
        btn_ascii = tk.Radiobutton(self.page, text='ASCII', variable=var, value=0)
        btn_bin = tk.Radiobutton(self.page, text='Binary', variable=var, value=1)
        btn_ascii.grid(row=1, column=0, sticky=ttk.W, padx=10, pady=10)
        btn_ascii.place(x=100, y=80)
        btn_bin.grid(row=1, column=1, sticky=ttk.W, padx=10, pady=10)
        btn_bin.place(x=200, y=80)

        def selectbtn():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        # 明文，主密钥输入
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        plainText_input.place(x=200, y=110)

        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        masterKey_input.place(x=200, y=150)

        sWelcome = tk.Label(self.page, text='加密界面', height=3, width=200,
                            bg='white',
                            font=('Arial', 14))
        sWelcome.pack()

        # 提示词的设计和放置
        func1 = tk.Label(self.page, text='明文', width=9, height=2, font=('黑体', 10), bg='white')
        func1.place(x=80, y=105)
        func2 = tk.Label(self.page, text='主密钥', width=9, height=2, font=('黑体', 10), bg='white')
        func2.place(x=80, y=145)

        # 密文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.pack(padx=10, pady=150)
        plainText_output.insert('insert', '加密结果：')

        def encryption_ans():
            # 这里设置检查，防止用户不合理输入
            key = self.masterKey.get()
            flag = selectbtn()
            if len(key) != 10:
                tk.messagebox.showerror('Invalid Key', '密钥长度错误，请重新输入')
                return -1
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            if flag == 0:
                text = self.plainText.get()
                # ASCII版本
                text = text2binary(text)
            else:
                text = self.plainText.get()

            if len(text) != 8:
                tk.messagebox.showerror('Invalid PlainText', '明文错误，请重新输入')
                return -1
            for i in range(len(text)):
                if int(text[i]) != 1 and int(text[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '明文错误，请重新输入')
                    return -1
            k1 = subkey(key)[0]
            k2 = subkey(key)[1]
            ip = permutation(text)
            fk1 = round_function(ip, k1)
            sw = swapper(fk1)
            fk2 = round_function(sw, k2)
            ip_reverse = permutation_reverse(fk2)
            plainText_output.delete(0.0, tk.END)
            plainText_output.insert('insert', '加密结果：')
            plainText_output.insert('insert', ip_reverse)

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle=(INFO, OUTLINE), command=self.iBack, width=10)
        quit_button.pack(padx=5, ipady=10)
        quit_button.place(x=230, y=330)

        # “加密”按钮的设计
        iGet = ttk.Button(self.page, text='    加密    ', bootstyle=(INFO, OUTLINE), command=encryption_ans)
        iGet.pack(padx=5, ipady=10)
        iGet.place(x=460, y=130)  # 设计按钮的样式，大小和位置


class Decryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('600x450+900+450')  # 设置窗口大小
        self.cipherText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        # 明文，主密钥输入
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        cipherText_input.place(x=200, y=110)

        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        masterKey_input.place(x=200, y=150)

        sWelcome = tk.Label(self.page, text='解密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 14))
        sWelcome.pack()

        # 提示词的设计和放置
        func1 = tk.Label(self.page, text='密文', width=9, height=2, font=('黑体', 10), bg='white')
        func1.place(x=80, y=105)
        func2 = tk.Label(self.page, text='主密钥', width=9, height=2, font=('黑体', 10), bg='white')
        func2.place(x=80, y=145)

        # 密文输出
        cipherText_output = ttk.Text(self.page, height=5, width=30)
        cipherText_output.pack(padx=10, pady=150)
        cipherText_output.insert('insert', '解密结果：')

        # 解密实现函数
        def Decryption_ans():
            key = self.masterKey.get()
            cipherText = self.cipherText.get()
            if len(key) != 10:
                tk.messagebox.showerror('Invalid Key', '密钥格式错误')
                return -1
            if len(cipherText) != 8:
                tk.messagebox.showerror('Invalid CipherText', '密文格式错误')
                return -1
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            for i in range(len(cipherText)):
                if int(cipherText[i]) != 1 and int(cipherText[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥错误，请重新输入')
                    return -1
            k1 = subkey(key)[0]
            k2 = subkey(key)[1]
            ip = permutation(cipherText)
            fk2 = round_function(ip, k2)
            sw = swapper(fk2)
            fk1 = round_function(sw, k1)
            ip_reverse = permutation_reverse(fk1)
            cipherText_output.delete(0.0, tk.END)
            cipherText_output.insert('insert', '解密结果：')
            cipherText_output.insert('insert', ip_reverse)

        # “解密”按钮的设计
        iGet = ttk.Button(self.page, text='    解密    ', bootstyle=(INFO, OUTLINE), command=Decryption_ans)
        iGet.pack(padx=5, ipady=10)
        iGet.place(x=460, y=130)  # 设计按钮的样式，大小和位置

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle=(INFO, OUTLINE), command=self.iBack, width=10)
        quit_button.pack(padx=5, ipady=10)
        quit_button.place(x=230, y=330)


class Crack(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('600x530+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.cipherText = ttk.StringVar()
        self.createPage()
        self.ans = []

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        # 明文，密文输入
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        plainText_input.place(x=200, y=110)

        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.grid(row=15, column=1, sticky=ttk.W, padx=10, pady=10)
        cipherText_input.place(x=200, y=150)

        sWelcome = tk.Label(self.page, text='破解界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 14))
        sWelcome.pack()

        # 提示词的设计和放置
        func1 = tk.Label(self.page, text='明文', width=9, height=2, font=('黑体', 10), bg='white')
        func1.place(x=80, y=105)
        func2 = tk.Label(self.page, text='密文', width=9, height=2, font=('黑体', 10), bg='white')
        func2.place(x=80, y=145)

        #
        key_output = ttk.Text(self.page, height=9, width=30)
        key_output.pack(padx=10, pady=150)
        key_output.insert('insert', '破解结果：')

        def encryption_ans_check(text, key):
            k1 = subkey(key)[0]
            k2 = subkey(key)[1]
            ip = permutation(text)
            fk1 = round_function(ip, k1)
            sw = swapper(fk1)
            fk2 = round_function(sw, k2)
            ip_reverse = permutation_reverse(fk2)
            return ip_reverse

        # 破解实现函数
        def worker(num, Tid, iText, iCipher, ans):
            print(f"Thread {Tid} is starting...")
            if not is_power_of_two(num):
                return -1

            temp = int(1024 / num)
            flag = 0
            for index in range(Tid * temp, (Tid + 1) * temp):
                temp_key = str(bin(index)[2:].zfill(10))
                temp_ans = encryption_ans_check(iText, temp_key)
                solved_ans = ''.join(str(i) for i in temp_ans)
                if solved_ans == iCipher:
                    ans.append(temp_key)
                    print("Key Found: " + temp_key)
                    flag = 1
            if flag == 0:
                print("Key not found!\n")
                return -1

        # 创建16个线程进行密码破解
        def crack_func():
            threads = []
            start = time.time()
            for i in range(16):
                # Format the thread ID with leading zeros
                thread_id = i
                t = threading.Thread(target=worker,
                                     args=(16, thread_id, self.plainText.get(), self.cipherText.get(), self.ans))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            end = time.time()
            running_time = str(end - start)
            print("运行时间为：" + running_time + "s")
            key_output.delete(0.0, tk.END)
            key_output.insert('insert', '破解结果：\n')
            for i in range(len(self.ans)):
                key_output.insert('insert', self.ans[i] + "\n")
            key_output.insert('insert', "运行时间: " + running_time + "s" + "\n")

        # “解密”按钮的设计
        iGet = ttk.Button(self.page, text='    解密    ', bootstyle=(INFO, OUTLINE), command=crack_func)
        iGet.pack(padx=5, ipady=10)
        iGet.place(x=460, y=130)  # 设计按钮的样式，大小和位置

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle=(INFO, OUTLINE), command=self.iBack, width=10)
        quit_button.pack(padx=5, ipady=10)
        quit_button.place(x=230, y=430)


win = ttk.Window()
win.geometry('600x400+900+450')
win.title('S-DES')  # 窗口名称
win.resizable(False, False)  # 禁止用户自行调节窗口大小
Welcome(win)
win.mainloop()
