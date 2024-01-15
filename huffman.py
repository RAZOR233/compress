import argparse
class Node:
    # 定义一个结构体，表示树的节点
    def __init__(self, name, weight, left=None, right=None, father=None):
        self.name = name
        self.weight = weight
        self.left = left
        self.right = right
        self.father = father

    # 判断是否是左孩子
    def is_left(self):
        return self.father.left == self
myname=[]
mycodes=[]
def get_parser():
    parser = argparse.ArgumentParser(description='请使用正确的文件输入格式')
    parser.add_argument('-type', type=str, help='输入使用功能，压缩（0），或者解压缩（1）')
    parser.add_argument('-inputfile_path', type=str, help='输入待压缩文件路径(请勿输入中文路径）')
    parser.add_argument('-outputfile_path', type=str, help='输入待解压文件路径(请勿输入中文路径）')
    args = parser.parse_args()
    return args
def create_node(words, weights):
    # 将各单词与其权值装载为 node 树节点，返回树节点列表
    node_list = []
    for i in range(len(words)):
        node_list.append(Node(words[i], weights[i]))
    return node_list


def create_huffman_tree(node_list):
    # 将树节点列表进行升序排序。每次取出权值最小的两个节点合并
    node_list.sort(key=lambda node: node.weight)
    left = node_list.pop(0)
    right = node_list.pop(0)
    new_node = Node(left.name+right.name, left.weight+right.weight, left, right, None)
    # 将合并后的节点再次装入节点列表中
    node_list.append(new_node)
    # 判断节点列表是否只剩下一个元素（即根节点），若不是，则递归执行此函数
    return node_list[0] if len(node_list) == 1 else create_huffman_tree(node_list)


def get_huffman_code(root, code=''):
    # 根据数的根节点，递归判断每个节点是不是叶子节点，若是则输出此节点对应的huffman编码
    if root.left is None:
        #print(root.name, code)
        myname.append(root.name)
        mycodes.append(code)
    else:
        get_huffman_code(root.left, code+"0")
        get_huffman_code(root.right, code+"1")

# 获取字符出现的频数
def count_frequency(input_string):
    # 用于存放字符
    char_store = []
    # 用于存放频数
    freq_store = []

    # 解析字符串
    for index in range(len(input_string)):
        if char_store.count(input_string[index]) > 0:
            temp = int(freq_store[char_store.index(input_string[index])])
            temp = temp + 1
            freq_store[char_store.index(input_string[index])] = temp
        else:
            char_store.append(input_string[index])
            freq_store.append(1)
    # 返回字符列表和频数列表
    return char_store, freq_store

def get_char_frequency(char_store=[], freq_store=[]):
    # 用于存放char_frequency
    char_frequency = []
    for item in zip(char_store, freq_store):
        temp = (item[0], item[1])
        char_frequency.append(temp)
    return char_frequency


def code(file):
    i=0
    outtext = ""
    outtext = outtext + (str(len(file) % 8) + "sjjend")
    while i + 8 <= len(file):
        n = 0
        tmp = file[i:i + 8]
        n = int(tmp, 2)
        outtext = outtext + chr(n)
        i += 8
    tmp = file[i:len(file)]
    while len(tmp) != 8:
        tmp = tmp + "0"
    outtext = outtext + chr(int(tmp, 2))
    return outtext
def bytes_read(input_file):
    with open(input_file, 'rb') as f:
        f.seek(0, 2)  # 读取文件的总长度，seek(0,2)移到文件末尾，tell()指出当前位置，并且用seek(0)重新回到起点
        size = f.tell()
        f.seek(0)
        bytes_list = [0] * size  # 创建一个长度为size的列表，存放读入的字节

        i = 0
        while i < size:
            bytes_list[i] = f.read(1)  # 每次读取一个符号
            i += 1
    return bytes_list

def huffman_code(inputfile_path,outputfile_path):
    print("文件正在压缩，请稍等...")
    input_file = inputfile_path
    file = ""
    bytes_list = bytes_read(input_file)

    char_store, freq_store = count_frequency(bytes_list)
    node_list = create_node(char_store, freq_store)
    root = create_huffman_tree(node_list)
    get_huffman_code(root)
    ff = open(outputfile_path, 'wb')
    for k in bytes_list:
        file = file + mycodes[myname.index(k)]
    output = code(file)
    output = output + 'sjjend'

    for k in myname:
        output = output + (chr(int.from_bytes(k, byteorder='big')))
    output = output + 'sjjend'
    for k in mycodes:
        output = output + (k + " ")
    output = output + 'sjjend'
    output = output + inputfile_path
    ff.write(output.encode('latin1'))
    ff.close()
    print("文件压缩完成！！！")
# 解压缩huffman文件
def decode_huffman(input_string,  char_store, freq_store,outputfile_path):
    f = open(outputfile_path, 'wb')
    encode = ''
    # decode = ''
    for index in range(len(input_string)):
        encode = encode + input_string[index]
        for item in range(len(char_store)):
            if encode == freq_store[item]:
                # decode = decode + item[0]
                f.write(char_store[item])
                encode = ''
    # return decode
def decode(firsttext,left):
    mytext = ""
    count = 0
    for i in firsttext:
        if count + 1 == len(firsttext):
            tmp = str(bin(ord(i)).replace('0b', ''))
            while len(tmp) != 8:
                tmp = "0" + tmp
            t = tmp[0:left]
            mytext = mytext + t
            break
        tmp = str(bin(ord(i)).replace('0b', ''))
        while len(tmp) != 8:
            tmp = "0" + tmp
        # print(ord(i),tmp)
        mytext = mytext + tmp
        count += 1
    return mytext
def huffman_decode(inputfile_path):
    print("文件正在解压，请稍等...")
    data = open(inputfile_path, 'rb')
    text = ""
    line = data.read()
    myname = []
    text = line.decode('latin1')
    list = text.split("sjjend")
    left = int(list[0])
    firsttext = list[1]
    mytext = decode(firsttext, left)
    # myname=list[2].split("//")
    mycode = list[3].split(" ")
    outputfile_path=list[4]
    tmp = line[len(list[0]) + 6 + len(list[1]) + 6:len(line) - len(list[3])-len(list[4]) - 12]
    for k in tmp:
        myname.append(int.to_bytes(k, 1, byteorder='big'))
    out = decode_huffman(mytext, myname, mycode,outputfile_path)
    print("文件解压完成！")
if __name__=='__main__':
    args=get_parser()
    type=args.type
    inputfile_path= args.inputfile_path
    outputfile_path= args.outputfile_path
    # --inputfile_path D:\\code\\编码理论\\test\\test.txt"
    # --outputfile_path D:\\code\\编码理论\\test\\test.qaq"
    # inputfile_path="D:\\code\\test\\cat.png"
    # outputfile_path="D:\\code\\test\\cat.qaq"
    if type=='0':
        if inputfile_path==None:
            print("No inputfile path!!!")
        elif inputfile_path==None:
            print("No outputfile path!!!")
        else:
            huffman_code(inputfile_path,outputfile_path)
    elif type=='1':
        if inputfile_path==None:
            print("No inputfile path!!!")
        else:
            huffman_decode(inputfile_path)
    else:
        print("Wrong type input!!")