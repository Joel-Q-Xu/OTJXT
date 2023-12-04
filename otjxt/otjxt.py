
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import IV,VI
import time
import sys, os, math, random
from subprocess import call, Popen, PIPE
import numpy as np
import csv
from Crypto.Cipher import AES
import base64
import pickle
from Crypto.Random import get_random_bytes
from dataclasses import dataclass
import hashlib


@dataclass
class T:
    y:int
    e:bytes



random_bytes = get_random_bytes(16)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# def hashp(text):
#     group_name = 'MNT159'
#     group = PairingGroup(group_name)
#
#     hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
#     print(hashed.hexdigest())
#     time1=time.time()
#     a=hash(text)
#     time2=time.time()
#     time3=time.time()
#     b=group.hash(text)
#     time4=time.time()
#
#     print(time2-time1)
#     print(time4-time3)
#
#
#
#     # return group.hash(text)
#     return hashed.hexdigest()
def aes_encrypt(key, text):
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    text = pad(text)
    ciphertext = cipher.encrypt(text.encode('utf8'))
    return ciphertext

def aes_decrypt(key, text):
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    plaintext = cipher.decrypt(text)
    unpad = lambda s: s[0:-s[-1]]
    return unpad(plaintext).decode('utf8')

group_name = 'MNT159'
group = PairingGroup(group_name)



def EMM_setup(attrw1,attrw2,intable):

    MM= {}
    K_e = "77d933b37ebf4e3410724a8ba8e9cdf7"
    K_w = "f56ba18a927f6b4851106e85835ed891"
    K_z = "77d972b37ebf4e3410724a8ba8e9cdf7"
    msk = "88d972b37ebf4e3410724a8ba8e9cdf7"


    p=208617601094290618684641029477488665211553761021




    attrw=[attrw1,attrw2]
    l=len(attrw)
    for i in range(2):
        for j in range(len(intable[i])):

            z=group.hash(K_z+intable[i][j].keyword)
            c = 1
            for m in range(len(attrw[i])):
                stag =  hashlib.sha256((msk+str(i + 1) + intable[i][j].keyword + attrw[i][m]).encode('utf-8')).hexdigest()
                MM[stag] = []
            for k in range(len(intable[i][j].id_list)):
                z_c = group.hash(K_z+intable[i][j].keyword + str(c))
                for m in range(len(attrw[i])):
                    xw = group.hash(K_w + attrw[i][m])+group.hash(K_w + intable[i][j].id_list[k][2 * m + 2])
                    y = (xw - z_c) * z
                    k_ew =hashlib.sha256((K_e+ intable[i][j].keyword + attrw[i][m]).encode('utf-8')).hexdigest()
                    k_ew = str(k_ew)
                    k_ew = k_ew[0:16]
                    e = aes_encrypt(k_ew, intable[i][j].id_list[k][0])

                    stag = hashlib.sha256((msk+str(i + 1) + intable[i][j].keyword + attrw[i][m]).encode('utf-8')).hexdigest()
                    MM[stag].append(T(y, e))
                c = c + 1
    return K_z,K_w,K_e,msk,p,MM

def ClientGenmtk(i,j,w1,w2,msk,attr1,attr2):
    mtk1=hashlib.sha256((msk+str(i)+w1 +attr1).encode('utf-8')).hexdigest()
    mtk2=hashlib.sha256((msk+ str(j) + w2 + attr2).encode('utf-8')).hexdigest()
    return mtk1,mtk2

def ClientGenab(p):
    alpha = group.random(ZR)
    beta=group.random(ZR)
    # alpha=get_random_bytes(8)
    # beta=get_random_bytes(8)
    # alpha = int.from_bytes(alpha, byteorder='big') % p
    # beta= int.from_bytes(beta, byteorder='big') % p
    # print(alpha)
    # print(beta)
    return alpha,beta
def inverse(n, mod):
    return pow(n, mod-2, mod)

def ClientGenxtk(alpha,beta,K_z,w1,w2,p):
    a=group.hash(K_z+w2)
    # a=int(a,16)%p
    # a=int.from_bytes(a, byteorder='big')%p
    b =group.hash(K_z+w1)
    # b=int(b,16)%p
    # b = int.from_bytes(b, byteorder='big')%p
    xtk1=alpha*a+inverse(b, p)
    xtk2 = alpha * b + inverse(a, p)

    return xtk1,xtk2

def ClientGenXattr(attr,K_w,p):
    xattr=group.hash(K_w+attr)
    # xattr=int(xattr,16)%p
    #xattr=int.from_bytes(xattr,byteorder='big')%p
    return xattr

def ClientGenjtk(c,beta,K_z,xtk,w,xattr,p):
    jtk = [i for i in range(c)]
    a=group.hash(K_z+w)
    # a=int(a,16)%p
    #a=int.from_bytes(a,byteorder='big')%p
    for i in range(c):
        b = group.hash(K_z+w+str(i+1))
        # b=int(b,16)%p
        #b = int.from_bytes(b, byteorder='big') % p
        jtk[i]=int(beta+a*xtk*(b-xattr))
    return jtk

def SearchStag(mtk,MM):

    return MM[mtk]

def ServerGenxtag(t, xtk,jtk,p):
    xtag=[i for i in range(len(t))]
    # time1=time.time()
    for i in range(len(t)):
        xtag[i]=t[i].y*xtk+jtk[i]
    # time2=time.time()
    # print(time2-time1)
    return xtag
#
# def ServerSearch(xtag1,xtag2,t1,t2):
#     e1 = []
#     e2 = []
#     for i in range(len(xtag1)):
#         flag = False
#         for j in range(len(xtag2)):
#             if (xtag1[i]==xtag2[j]):
#                 flag = True
#         if (flag):
#             e1.append(t1[i].e)
#
#     for i in range(len(xtag2)):
#         flag = False
#         for j in range(len(xtag1)):
#             if (xtag2[i]==xtag1[j]):
#                 flag = True
#         if (flag):
#             e2.append(t2[i].e)
#
#     return e1, e2


def hash_join(xtag1, xtag2,t1,t2):
    hash_table = {}
    result = []
    if(len(xtag1)<len(xtag2)):
        # 将第一个数据集的每个元素哈希到哈希表
        for i in range(len(xtag1)):

            hash_table[xtag1[i]] = t1[i].e
            # 遍历第二个数据集的每个元素，查找匹配的连接
        for j in range(len(xtag2)):
            match = hash_table.get(xtag2[j])
            if match:
                result.append((match, t2[j].e))
    else:
        # 将第一个数据集的每个元素哈希到哈希表
        for i in range(len(xtag2)):
            hash_table[xtag2[i]] = t2[i].e
            # 遍历第二个数据集的每个元素，查找匹配的连接
        for j in range(len(xtag1)):
            match = hash_table.get(xtag1[j])
            if match:
                result.append((t1[j].e,match))

    return result
def ClientGetind2(result, w1, w2, K_e,attr1,attr2):

        ind1 = []
        ind2 = []
        k_ew1 = hashlib.sha256((K_e+w1 + attr1).encode('utf-8')).hexdigest()
        #k_ew1 = bytearray(aes_encrypt(K_e, w1 + attr1))
        k_ew1 = str(k_ew1)
        k_ew1= k_ew1[0:16]
        for i in range(len(result)):
            ind1.append(aes_decrypt(k_ew1, result[i][0]))

        k_ew2 =hashlib.sha256((K_e+ w2 + attr2).encode('utf-8')).hexdigest()
        k_ew2 = str(k_ew2)
        k_ew2 = k_ew2[0:16]
        for i in range(len(result)):
            ind2.append(aes_decrypt(k_ew2, result[i][1]))

        return ind1, ind2

if __name__ == "__main__":
    time_start=time.time()
    time1_start = time.time()
    # table = []
    #
    # attrw = ['tid','abc']
    # table_a_file = "./testa.tbl"
    # table1 = IV.read_table(attrw, table_a_file)
    # table_b_file = "./testb.tbl"
    # table2 = IV.read_table(attrw, table_b_file)
    #
    # table = [table1, table2]
    # intable_a_file = "./intesta.tbl"
    # intable1 = VI.read_intable(attrw,intable_a_file)
    # intable_b_file = "./intestb.tbl"
    # intable2 = VI.read_intable(attrw,intable_b_file)
    # intable = [intable1, intable2]
    #
    # w1 = "data=012011"
    # w2 = "mname=apple"
    # ww='tid'

    # #
    attrw = ["custkey"]

    intable_a_file = "indata/0.01/incustomer.tbl"
    intable1 = VI.read_intable(attrw, intable_a_file)
    intable_b_file = "indata/0.01/inorders.tbl"
    intable2 = VI.read_intable(attrw, intable_b_file)
    intable = [intable1, intable2]

    w1 = "selectivity=12.5"
    w2 = "selectivity=12.5"
    ww = "custkey"
    print('aaaaaaaaaaaaa')
    time1_end=time.time()
    print(time1_end-time1_start)
    time2_start=time.time()

    K_z,K_w,K_e,msk,p,MM=EMM_setup(attrw,attrw,intable)
    print(len(MM))
    time2_end=time.time()
    print(time2_end-time2_start)

    mtk1, mtk2 = ClientGenmtk(1, 2, w1, w2, msk, ww, ww)
    alpha, beta = ClientGenab(p)
    xtk1, xtk2 = ClientGenxtk(alpha, beta, K_z, w1, w2, p)
    xattr1 = ClientGenXattr(ww, K_w, p)
    xattr2 = ClientGenXattr(ww, K_w, p)
    t1 = SearchStag(mtk1, MM)
    t2 = SearchStag(mtk2, MM)
    c1 = len(t1)
    c2 = len(t2)
    print("cccccccccccc")
    print(c1, c2)
    jtk1 = ClientGenjtk(c1, beta, K_z, xtk1, w1, xattr1, p)
    jtk2 = ClientGenjtk(c2, beta, K_z, xtk2, w2, xattr2, p)
    xtag1 = ServerGenxtag(t1, xtk1, jtk1, p)
    xtag2 = ServerGenxtag(t2, xtk2, jtk2, p)
    #e1, e2 = ServerSearch(xtag1, xtag2, t1, t2)
    result=hash_join(xtag1, xtag2,t1,t2)
    print("aaaaaaaaaaaa")

    ind1, ind2 = ClientGetind2(result, w1, w2, K_e, ww, ww)
    print(ind1, ind2)
    print(len(ind2))
    time_end=time.time()
    print("all time:"+str(time_end-time_start))


