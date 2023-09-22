import secrets
import tkinter as tk
import tkinter.messagebox
import threading
import time
import ttkbootstrap as ttk

from ttkbootstrap import Style
from tkinter import *


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


# 子密钥的生成
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


# 初始置换函数
def permutation(origin):
    p_box = [2, 6, 3, 1, 4, 8, 5, 7]
    p_result = []
    for index in range(8):
        p_result.append(int(origin[p_box[index] - 1]))
    return p_result


# 最终置换函数
def permutation_reverse(origin):
    p_box = [4, 1, 3, 5, 7, 2, 8, 6]
    p_reverse_result = []
    for index in range(8):
        p_reverse_result.append(int(origin[p_box[index] - 1]))
    return p_reverse_result


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
    right = []
    left = []
    for index in range(4):
        right.append(origin[index])
    for index in range(4):
        left.append(origin[index + 4])
    return left + right


# 获取密钥函数
def generate_key(length):
    key = secrets.randbits(length)
    # 转为二进制，左零补全为10-bit
    key_bin = bin(key).replace('0b', '').zfill(10)
    return key_bin


# 判断是否为2的次方
def is_power_of_two(n):
    return n != 0 and (n & (n - 1)) == 0


# 首页界面
class Welcome(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
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
        self.page.pack(fill='both', pady=10, expand=True)
        sWelcome = tk.Label(self.page, text='S-DES密码系统', height=3, width=200,
                            bg='white',
                            font=('黑体', 26))
        sWelcome.pack(pady=10)

        combobox = ttk.Combobox(self.page, bootstyle='info', textvariable=self.commandStr)  # 获取用户输入的信息
        combobox['value'] = ('加密', '解密', '获取密钥', 'Crack')  # 组合框显示的选项
        combobox.current(0)
        combobox.pack(padx=5, pady=10)
        combobox.place(relx=0.45, rely=0.45)  # 组合框的位置和大小

        getStr = ['加密', '解密', '获取密钥', 'Crack']

        # 选择不同功能切换至不同界面
        def get_command():
            for index in range(len(getStr)):
                if self.commandStr.get() == getStr[index]:
                    flag = index
                    break
                else:
                    flag = 5
            if flag == 0:
                self.page.destroy()
                Encryption(self.root)
            elif flag == 1:
                self.page.destroy()
                Decryption(self.root)
            elif flag == 2:  # 获取密钥
                self.page.destroy()
                Welcome(self.root)
                key = str(generate_key(10))
                tk.messagebox.showinfo('Key Generated', '密钥请妥善保管:' + key)
            elif flag == 3:
                self.page.destroy()
                Crack(self.root)
            else:
                tk.messagebox.showerror('错误', '不提供该类型服务')

        op_label = tk.Label(self.page, text='选择操作类型', width=14, height=2, font=('黑体', 13), bg='white')
        op_label.place(relx=0.2, rely=0.44)

        # "确定"按钮
        confirm_button = ttk.Button(self.page, text='确定', bootstyle='primary.TButton', command=get_command, width=7)
        confirm_button.pack(padx=5, ipady=10)
        confirm_button.place(relx=0.42, rely=0.75)


# 加密界面
class Encryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        def encryption_ans():
            # 这里设置检查，防止用户不合理输入
            key = self.masterKey.get()
            flag = select_button()
            if len(key) != 10:
                tk.messagebox.showerror('Invalid Key', '密钥长度错误，请重新输入')
                return -1
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            if flag == 0:
                # ASCII版本
                text = self.plainText.get()
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：\n')
                for letter in text:
                    binary_text = text2binary(letter)
                    k1 = subkey(key)[0]
                    k2 = subkey(key)[1]
                    ip = permutation(binary_text)
                    fk1 = round_function(ip, k1)
                    sw = swapper(fk1)
                    fk2 = round_function(sw, k2)
                    ip_reverse = permutation_reverse(fk2)
                    ip_str = ''.join(str(i) for i in ip_reverse)
                    out = chr(int(ip_str, 2))
                    plainText_output.insert('insert', out)
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
                ip_str = ''.join(str(i) for i in ip_reverse)
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：')
                plainText_output.insert('insert', ip_str)

        # GUI界面
        sWelcome = tk.Label(self.page, text='加密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='ASCII', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='Binary', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 明文，主密钥输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.31)

        # 密钥输入显示为*号进行保密
        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 标签显示输入类别
        plaintext_label = tk.Label(self.page, text='明文', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '加密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "加密"按钮
        encrypt_button = ttk.Button(self.page, text='加密', bootstyle='success.TButton', command=encryption_ans,
                                    width=7)
        encrypt_button.place(relx=0.52, rely=0.8)


class Decryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.cipherText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        # 解密实现函数
        def decryption_ans():
            flag = select_button()
            key = self.masterKey.get()
            cipherText = self.cipherText.get()
            if len(key) != 10:
                tk.messagebox.showerror('Invalid Key', '密钥格式错误')
                return -1
            if flag == 1:
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
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '解密结果：')
                plainText_output.insert('insert', ip_reverse)
            else:
                binary_cipherText = text2binary(cipherText)
                if len(binary_cipherText) % 8 != 0:
                    tk.messagebox.showerror('Invalid CipherText', '密文格式错误')
                    return -1
                for i in range(len(key)):
                    if int(key[i]) != 1 and int(key[i]) != 0:
                        tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                        return -1
                temp_text = [binary_cipherText[i:i + 8] for i in range(0, len(binary_cipherText), 8)]
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '解密结果：\n')
                for index in temp_text:
                    k1 = subkey(key)[0]
                    k2 = subkey(key)[1]
                    ip = permutation(index)
                    fk2 = round_function(ip, k2)
                    sw = swapper(fk2)
                    fk1 = round_function(sw, k1)
                    ip_reverse = permutation_reverse(fk1)
                    ip_str = ''.join(str(i) for i in ip_reverse)
                    out = chr(int(ip_str, 2))
                    plainText_output.insert('insert', out)

        # GUI界面
        sWelcome = tk.Label(self.page, text='解密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='ASCII', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='Binary', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, text='密文', width=9, height=3, font=('黑体', 13), bg='white')
        ciphertext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文，密钥输入栏
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.31)

        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 明文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '解密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "解密"按钮
        decrypt_button = ttk.Button(self.page, text='解密', bootstyle='success.TButton', command=decryption_ans,
                                    width=7)
        decrypt_button.place(relx=0.52, rely=0.8)  # 设计按钮的样式，大小和位置


class Crack(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
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

            scale = int(1024 / num)
            flag = 0
            for index in range(Tid * scale, (Tid + 1) * scale):
                temp_key = str(bin(index)[2:].zfill(10))
                temp_ans = encryption_ans_check(iText, temp_key)
                solved_ans = ''.join(str(i) for i in temp_ans)
                if solved_ans == iCipher:
                    ans.append(temp_key)
                    print("Key Found: " + temp_key)
                    flag = 1
            if flag == 0:
                print(f"Key not found in thread {Tid}\n")
                return -1

        # 创建16个线程进行密码破解
        def crack_func():
            threads = []
            start = time.time()
            for i in range(16):
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

        # GUI界面
        sWelcome = tk.Label(self.page, text='破解界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, text='明文', width=9, height=3, font=('黑体', 13), bg='white')
        ciphertext_label.place(relx=0.28, rely=0.18)
        plaintext_label = tk.Label(self.page, text='密文', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.26)

        # 明文，密文输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.21)
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.29)

        # 输出可能的密钥
        key_output = ttk.Text(self.page, height=9, width=30)
        key_output.place(relx=0.32, rely=0.42)
        key_output.insert('insert', '破解结果：')

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "破解"按钮
        crack_button = ttk.Button(self.page, text='破解', bootstyle='success.TButton', command=crack_func, width=7)
        crack_button.place(relx=0.52, rely=0.8)


win = ttk.Window()
style = Style(theme='yeti')
win.geometry('820x660+900+450')
win.title('S-DES')
Welcome(win)
win.mainloop()
