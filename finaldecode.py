import math
A=[]
dictionary = []
# 解压缩huffman文件
def decode_huffman(input_string,  char_store, freq_store,outputfile_path):
    # f = open(outputfile_path, 'wb')
    encode = ''
    decode = b''
    for index in range(len(input_string)):
        encode = encode + input_string[index]
        for item in range(len(char_store)):
            if encode == freq_store[item]:
                # decode = decode + item[0]
                decode+=char_store[item]
                encode = ''
    return decode
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

def decompress(outputfile_path,compressed,l1,l2):
    f = open(outputfile_path, 'wb')
    for i in range(0, len(compressed) // (l1 + l2)):
        dictionary.append([int(compressed[(l1 + l2) * i:(l1 + l2) * i + l1], 2),
                           int(compressed[(l1 + l2) * i + l1:(l1 + l2) * i + l1 + l2], 2)])
    for k in dictionary:
        t = k
        tmp = b''
        while t[0] != 0:
            # print(t[0],t[1])
            tmp = A[t[1]] + tmp
            t = dictionary[t[0] - 1]
        tmp = A[t[1]] + tmp
        # output = output + tmp
        f.write(tmp)
        # print(output)
    f.close()
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
def LZ78decode(secondfile,outputfile_path):
    dictionary = []
    # data = open("D:\\code\\编码理论\\test\\output.qaq", 'rb')
    # f=open("D:\\code\\编码理论\\output\\test.txt",'w',encoding='latin1')
    text = ""
    # line = data.read()
    text = secondfile.decode('latin1')

    list = text.split("sjjend")

    left = int(list[0])
    firsttext = list[1]

    mytext = decode(firsttext, left)
    # print(mytext)
    compressed = mytext
    l1 = int(list[2])
    l2 = int(list[3])
    tmp = secondfile[len(secondfile) - len(list[4]):len(secondfile)]
    for k in tmp:
        A.append(int.to_bytes(k, 1, byteorder='big'))
    decompress(outputfile_path,compressed,l1,l2)
def huffman_decode(inputfile_path):
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
    secondfile = decode_huffman(mytext, myname, mycode,outputfile_path)
    LZ78decode(secondfile, outputfile_path)
if __name__=='__main__':
    inputfile_path = "D:\\code\\test\\cat.qaq"
    huffman_decode(inputfile_path)
