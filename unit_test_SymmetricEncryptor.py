from SymmetricEncryptor import *
from Binary import *

def testMagicNum():
	print("Magic Number, Binary result, Input string")
	for string in ["testing","test","toast","bad","bbd","abcdef","abcdeg","abcdefg",
				"aaaaaaaaaa","aaaaaaaaaaa","testlongerstring","does this change anything?",
				"N0wI@mU$ing@l0t0F$ymbOlz"]:
		result = getMagicNumber(Binary(string.encode()))
		print(str(result) + "   " + str(Binary(result,False,8)) + "   " + string)
	print("defferent seeds: ")
	for seed in [1,2,3,4,5,6,64,139,218,365,720,420,76]: #internally mods 256
		result = getMagicNumber(Binary("test".encode()),seed)
		print(str(result) + "   " + str(Binary(result,False,8)) + "   test")


def TestingAlgorithm(seed):
	result = 0b11111111 & seed #mask to right size
	for abyte in "test".encode():
		result = (result ^ 17*(seed+abyte)) & 0b11111111 #mod 256
	return result

def testOneToOne():
	results = []
	bad = []
	good = []
	for value in range(0,256):
		results.append(TestingAlgorithm(value))
	for value in range(0,256):
		if value not in results:
			bad.append(value)
		else:
			good.append(value)
	print("bad: ")
	for item in bad:
		print(str(item) + "   " + str(Binary(item)))
	print("good: ")
	for item in good:
		print(str(item) + "   " + str(Binary(item)))
	print ("total bad: " + str(len(bad)))

def testObfuscate():
	for string in ["testing","test","toast","bad","bbd","abcdef","abcdeg","abcdefg",
		"aaaaaaaaaa","aaaaaaaaaaa","testlongerstring","does this change anything?",
		"N0wI@mU$ing@l0t0F$ymbOlz"]:
		result = obfuscate(Binary(string.encode()))
		print(string + "   " + result.toBytes().decode("Latin-1") + "   " + Binary(string.encode(),False).toHex() + "   " + Binary(result,False).toHex())

def testXor():
	print("XOR")
	encryptor = SymmetricEncryptor('xor')
	#print(encryptor.encrypt("testing".encode(),"password").toBytes().decode("Latin-1"))
	print(encryptor.decrypt(encryptor.encrypt("testing".encode(),"password"),"password").toBytes().decode('latin-1') == "testing")
	print(encryptor.decrypt(encryptor.encrypt("test message that is kinda long".encode(),"stuff"),"stuff").toBytes().decode('latin-1') == "test message that is kinda long")
	print(encryptor.decrypt(encryptor.encrypt("Hi".encode(),"qwertyuiopasdfghjklzxcvbnm"),"qwertyuiopasdfghjklzxcvbnm").toBytes().decode('latin-1') == "Hi")

def testRand():
	print("RAND")
	encryptor = SymmetricEncryptor('rand')
	#print(encryptor.encrypt("testing".encode(),"password").toBytes().decode("Latin-1"))
	print(encryptor.decrypt(encryptor.encrypt("testing".encode(),"password"),"password").toBytes().decode('latin-1') == "testing")
	print(encryptor.decrypt(encryptor.encrypt("test message that is kinda long".encode(),"stuff"),"stuff").toBytes().decode('latin-1') == "test message that is kinda long")
	print(encryptor.decrypt(encryptor.encrypt("Hi".encode(),"qwertyuiopasdfghjklzxcvbnm"),"qwertyuiopasdfghjklzxcvbnm").toBytes().decode('latin-1') == "Hi")

def testStaging():
	print("STAGING")
	#print(Binary("testing".encode()).toHex())
	encryptor = SymmetricEncryptor("rand",'xor')
	enc = encryptor.encrypt("testing".encode(),"password1")
	#print(enc.toHex())
	dec = encryptor.decrypt(enc,"password1")
	#print(dec.toHex())
	print(dec.toBytes().decode('latin-1') == "testing")
	
	encryptor = SymmetricEncryptor('xor','rand','xor')
	enc = encryptor.encrypt("testing".encode(),"password1")
	dec = encryptor.decrypt(enc,"password1")
	print(dec.toBytes().decode('latin-1') == "testing")
	

if __name__ == "__main__":
	#testMagicNum()
	#testOneToOne()
	#testObfuscate()
	testXor()
	testRand()
	testStaging()