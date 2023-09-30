

# 测试结果



## 第1关：基本测试

- 根据S-DES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是8bit的数据和10bit的密钥，输出是8bit的密文

### 主界面

- 可以选择不同的功能，包括**加密，解密，获取密钥，破解功能**

   ![main_interface](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/main%20interface.png)

### 加密操作

- 密钥采用隐式显示，测试使用密钥均为***1111100000***

-  二进制风格

    ![encryption_binary](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/encryption_binary.png)

- ASCII风格

   ![encryption_ascii](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/encryption_ascii.png)

### 解密操作

- 密钥采用隐式显示，测试使用密钥均为***1111100000***

- 二进制风格

   ![decryption_binary](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/decryption_binary.png)

- ASCII风格

   ![decryption_ascii](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/decryption_ascii.png)

### 获取密钥操作

- 使用python的secrets模块获取随机密钥，提供的函数可以获取长度不同的密钥，S-DES获取10-bit密钥

```python
def generate_key(length):
    key = secrets.randbits(length)
    # 转为二进制，左零补全为10-bit
    key_bin = bin(key).replace('0b', '').zfill(10)
    return key_bin
```

 ![generate_key](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/generate_key.png)

### 破解操作

- 采用**多线程**进行破解，对密钥空间进行划分分别破解，比对获取的密文和截取的密文输出破解成功的密钥，同时会输出破解所花费的时间

```python
def crack_func():
    threads = []
    start = time.time()
    for i in range(16):
        thread_id = i
        t = threading.Thread(target=worker,
                             args=(16, thread_id, self.plainText.get(), self.cipherText.get(), self.ans,
                                   select_button()))
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
```

- 破解过程是将截取的明文通过划分的密钥进行加密，比对获取的密文是否正确

```python
# 破解实现函数
def worker(num, Tid, iText, iCipher, ans, selection):
    print(f"Thread {Tid} is starting...")
    # 为了简便线程数量需要为2的n次方
    if not is_power_of_two(num):
        return -1

    scale = int(1024 / num)
    flag = 0
    for index in range(Tid * scale, (Tid + 1) * scale):
        temp_key = str(bin(index)[2:].zfill(10))
        temp_ans = encryption_ans_check(iText, temp_key, selection)
        solved_ans = ''.join(str(i) for i in temp_ans)
        if solved_ans == iCipher:
            ans.append(temp_key)
            print("Key Found: " + temp_key)
            flag = 1
    if flag == 0:
        print(f"Key not found in thread {Tid}\n")
        return -1
```

- 破解测试

  - 二进制风格

     ![crack](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/crack.gif)

  - ASCII风格

     ![crack_ascii](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/crack_ascii.gif)



## 第2关：交叉测试

- 考虑到是**算法标准**，所有人在编写程序的时候需要使用相同算法流程和转换单元(P-Box、S-Box等)，以保证算法和程序在异构的系统或平台上都可以正常运行
- 设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P

### A组测试：



## 第3关：扩展功能

- 考虑到向实用性扩展，加密算法的数据输入可以是ACSII编码字符串(分组为1 Byte)，对应地输出也可以是ACII字符串(很可能是乱码)

### 功能实现

- GUI界面提供了ASCII或二进制编码的按钮，选择可以切换加密模式，ASCII模式下输出密文为ASCII对应的字符串
- 通过对按钮的选择切换模式，对于ASCII编码格式，对于每个字符转为二进制单独处理，最后整合获取的结果显示在相应的位置

```python
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
```

### 测试结果

  ![switch](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/switch.gif)

 ![switch_decrypt](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/switch_decrypt.gif)



## 第4关：暴力破解

- 假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，你也可以考虑使用多线程的方式提升破解的效率。请设定时间戳，用视频或动图展示你在多长时间内完成了暴力破解

### 测试结果

 ![crack_test](https://github.com/RaymundoTheWolf/S-DES/blob/main/test%20results%20gifs/crack_test.gif)



## 第5关：封闭测试

- 根据第4关的结果，进一步分析，对于你随机选择的一个明密文对，是不是有不止一个密钥Key？进一步扩展，对应明文空间任意给定的明文分组P~n~，是否会出现选择不同的密钥K~i~ ≠ K~j~加密得到相同密文C~n~的情况？

|   明文   | 密文     | 加密使用的密钥 |   破解的密钥   | 破解时间 |
| :------: | -------- | :------------: | :------------: | :------: |
|  101010  | 10011011 |   1111100000   | **1111100000** |  0.042s  |
|          |          |                |   1011100000   |          |
| 10011100 | 11100000 |   1001010110   |   0010111011   |  0.042s  |
|          |          |                |   0110111011   |          |
|          |          |                | **1001010110** |          |
|          |          |                |   1010101101   |          |
|          |          |                |   1101010110   |          |
|          |          |                |   1110101101   |          |
|  s-des   | ¨        |   0100110101   |   0000110101   |  0.204s  |
|          |          |                | **0100110101** |          |



## Summary

- S-DES的密钥空间只有10-bit，共1024种情况，这样的密码系统显然安全性不足
- S-DES中的置换盒，替换盒，轮函数和移位都展现了密码学的精华，即扩散和混淆，通过这一系列的变化能够很好地抹去明文和密文的统计特征，密文和密钥的统计关系
- 非线性代替变换提供了很好的加密效果
