import random
import math

class WyyEncryption(object):
    def __init__(self):
        pass


    def createSecretKey(self,size) :
        keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        key = ""
        for i in range(0,size):
            pos = random.random(0,1) * len(keys)
            pos = math.floor(pos)
            key = key +keys[pos]
        return key


    def aesEncrypt(self,word, secKey) :
        pass
                #  key = CryptoJS.enc.Utf8.parse(secKey)  #十六位十六进制数作为密钥
        #  iv = CryptoJS.enc.Utf8.parse(aes_mv)  #十六位十六进制数作为密钥偏移量
        #  srcs = CryptoJS.enc.Utf8.parse(word)
        #  encrypted = CryptoJS.AES.encrypt(srcs, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 })
        #  res = encrypted.toString()
        # print(res)
        # return res
