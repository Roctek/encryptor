from Binary import Binary
from random import Random

class SymmetricEncryptor:
	def __init__(self, *args):
		self.setStages(*args)
		self.rng = Random()
			
	def setStages(self, *args):
		self.stages = []
		for arg in args:
			if isinstance(arg, list):
				templist = arg
			elif isinstance(arg, str):
				templist = [arg]
			else:
				templist = []
			for item in templist:
				if not isinstance(item, str):
					raise Exception("expected string argument")
				if not hasattr(self,"encStage" + item.capitalize()) or not callable(getattr(self,"encStage" + item.capitalize())):
					raise Exception("Expected member function: encStage" + item.capitalize())
				if not hasattr(self,"decStage" + item.capitalize()) or not callable(getattr(self,"decStage" + item.capitalize())):
					raise Exception("Expected member function: decStage" + item.capitalize())
				else:
					self.stages.append(item)
		
	#takes a Binary object or convertable type
	def encrypt(self, data, password):
		#convert to Binary
		tempData = Binary(data)
		if isinstance(password,str):
			password = password.encode()
		tempPass = Binary(password)
		#run encryption scheme
		for functName in self.stages:
			tempData = getattr(self,"encStage" + functName.capitalize())(tempData, tempPass)
		return tempData
	
	#returns a Binary object
	def decrypt(self, binData, password):
		if isinstance(password,str):
			password = password.encode()
		tempPass = Binary(password)
		tempData = Binary(binData)
		#run decryption scheme
		for functName in reversed(self.stages):
			tempData = getattr(self,"decStage" + functName.capitalize())(tempData, tempPass)
		return tempData

	#maintains data length
	def encStageXor(self, binData, binPass):
		seed = getMagicNumber(binPass,getMagicNumber(Binary("xor".encode())))
		sizedPass = sizePass(binPass,len(binData))
		#obfuscate password
		sizedPass = obfuscate(sizedPass,seed)
		#actually do xor
		return binData ^ sizedPass
			
	#maintains data length
	def decStageXor(self, binData, binPass):
		return self.encStageXor(binData, binPass) #reciprocal
		
	#introduces random bits into the binary at positions determined by the password.
	#Do not use this as the first or last stage of encryption. It may be easily cracked if multiple results of encryptions using the same arguments are available
	def encStageRand(self, binData, binPass):
		seed = getMagicNumber(binPass,getMagicNumber(Binary("Rand".encode())))
		newLen = int(len(binData)*1.5)+(seed>>4)
		sizedPass = sizePass(binPass,newLen)
		sizedPass = obfuscate(sizedPass,seed)
		#go ahead and generate all possible random bits to avoid repeated calls
		randBin = Binary(self.rng.getrandbits(newLen),False,newLen)
		offset = 0
		for index, abit in enumerate(sizedPass):
			if len(binData) == newLen:
				return binData
			elif index >= len(binData):
				return binData // randBin[index:]
			elif abit:
				binData = binData.inserted(randBin[index],index+offset)
				offset += 1
		return binData
	
	#removes random bits instroduced into the binary
	def decStageRand(self, binData, binPass):
		seed = getMagicNumber(binPass,getMagicNumber(Binary("Rand".encode())))
		newLen = int((len(binData)-(seed>>4))/1.5)
		if newLen <= 0:
			raise Exception("Incorrect data length")
		sizedPass = sizePass(binPass,len(binData))
		sizedPass = obfuscate(sizedPass,seed)
		offset = 0
		for index, abit in enumerate(sizedPass):
			if len(binData) == newLen:
				return binData
			elif index+offset >= newLen:
				return binData[:index+offset]
			elif abit:
				binData = binData.removed(index)
				offset -= 1
		return binData[:newLen]

		
#produces an integer 0-255 based on a function of the input binary 
#essentially a very small hash
def getMagicNumber(binData,seed=0b1010101): #0 to 255
	result = 0b11111111 & seed #mask to right size
	for abyte in binData.toBytes():
	#run a simple map to make similar inputs differ a bit more
		result = (result ^ 17*(seed+abyte)) & 0b11111111 #mod 256
	return result	

#produces a different value of the same length as the input binary based on a function
#This is a one-way encryption. Do not use this to encrypt something that needs to be decrypted
def obfuscate(binPass,seed=0b1010101):
	seed = getMagicNumber(binPass,seed) #seed the seed so that nobody knows the actual seed used without the full password.
	result = Binary()
	for abyte in binPass.toBytes():
		tempRes = getMagicNumber(Binary(abyte),seed)
		seed = seed + tempRes # helps with repeated values
		result = result // Binary(tempRes,False,8) #reverses byte order
	return result.resized(len(binPass),True)


def sizePass(binPass,bitLen):
	if len(binPass)< bitLen:
		return extendPass(binPass,bitLen)
	else:
		return truncatePass(binPass,bitLen)

#extends the password by zero-filling
#Note: obfuscate afterwards to hopefully reduce the amount of zeros
def extendPass(binPass,bitLen):
	return binPass.resized(bitLen)

#reduce the size of the password by truncating	
#Note: truncating the password will produce collisions, so make sure to use the full password in obfuscation, etc.
def truncatePass(binPass,bitLen):
	if len(binPass)< bitLen:
		raise Exception("Cannot truncate password that is smaller than the given bit length argument")
	return binPass.resized(bitLen,True)


