
#assumes big-endian representation
#Treat it as an integer. Everything is a copy. Nothing set beyond instantiation. (low cost considering it is 2 int and a bool) 

#TODO: Error using Binary("0xFF",True,8)   0xFF may be interpreted as integer. maybe not <=

class Binary(object):
	#default sign is unsigned (signed = false)
	def __init__(self, value=None, signed = None, length = None):
		#initialize fields
		if isinstance(value, Binary):
			#handle sign
			if isinstance(signed, bool):
				self.isSigned = signed
			else:
				self.isSigned = value.isSigned
			self.data, dataLen = intify(value.toBin(),self.isSigned)
		else: #not a Binary
			#handle sign
			if isinstance(signed, bool):
				self.isSigned = signed
			elif signed is None:
				self.isSigned = False
			else:
				raise Exception('expected bool or None as "signed" argument')
			#compute value
			self.data, dataLen = intify(value, self.isSigned) #includes leading sign bits in length
			
		#compute length
		if self.data is None:
			minLen = 0
		else:
			minLen = bitLen(self.data,self.isSigned)
		if isinstance(length, int):
			if length < minLen:
				raise Exception("length argument not big enough to represent the integer value " + str(self.data))
			else:
				self.length = length
		elif length is None:
			self.length = dataLen
		else:
			raise Exception("Length argument must be an integer or Nonetype")
			
		if dataLen is None: #negative unsigned is converted to positive 1 filled to length
			if self.length is None:
				self.length = minLen
			self.isSigned = True
			self.data = self.toUint()
			self.isSigned = False

	#recreate the binary value by treating it as signed
	#If you want to find the current signed status, use the attribute self.isSigned
	def signed(self):
		return Binary(self, True)
	
	#recreate the binary value by treating it as unsigned
	def unsigned(self):
		return Binary(self, False)

#size

	def __len__(self):
		return self.length
	
	#return the smallest representable length to maintain same integer value
	def minLen(self):
		if self.data is None:
			return 0
		return bitLen(self.data, self.isSigned)
	
	#create a new binary of the same value but different length
	#any added bits will equal the sign bit if the binary is signed
	#error thrown if length not big enough to support the same value
	#if force is true, length error is ignored and value is truncated to lower order bits
	#	0b1001001 resized to 3 bits using force = 0b001
	def resized(self, length, force=False):
		if force is True and length < self.minLen():
			if not isinstance(length, int):
				raise TypeError("Expected integer argument")
			if length < 0:
				raise Exception("Expected length argument 0 or greater")
			elif length == 0:
				return Binary(None,self.isSigned)
			else:
				return Binary("0b" + self.toBin()[self.length-length+2:],self.isSigned)
		else:
			if length == 0:
				return Binary(None,self.isSigned)
			else:
				return Binary(self, self.isSigned, length)
		
	def minimize(self):
		if self.data is None:
			return Binary(None,self.isSigned)
		else:
			return Binary(self, self.isSigned, self.minLen())
		
# conversion
	def __repr__(self):
		return str(self)
		
	def __str__(self):
		return self.toBin()
		
	def __int__(self):
		if self.data is None:
			raise Exception("Binary cannot convert Nonetype value to integer")
		return self.data
	
	def __bytes__(self):
		return self.toBytes()
		
	def __bool__(self):
		return bool(self.data)
		
	def toBin(self):
		if self.data is None:
			return "0b"
		else:
			return binify(self.data, self.isSigned, self.length)
		
	def toBytes(self):
		if self.data is None:
			raise Exception("Binary cannot convert Nonetype value to bytes")
		remainder = self.length%8
		numBytes = int((self.length-remainder)/8) + int(bool(remainder))
		return int.to_bytes(self.toUint(),numBytes,'big') #must convert to unsigned
		
	def toHex(self):
		if self.data is None:
			raise Exception("Binary cannot convert Nonetype value to hexadecimal")
		remainder = self.length%8
		byteVal = self.toBytes()
		result = "0x"
		for abyte in byteVal:
			result = result + "0"*(abyte < 0x10) + hex(abyte)[2:]
		if remainder < 5 and remainder > 0: #remove extra digit if necessary
			result = "0x" + result[3:]
		return result
		
	#returns an unsigned integer represented by the data (even if signed)
	def toUint(self):
		if self.data is None:
			raise Exception("Binary cannot convert Nonetype value to unsigned integer")
		if self.isSigned and self.data < 0:
			return self.unsigned().data
		else:
			return self.data
		
# comparison operators
# treats argument values as signed or unsigned according to the Binary's signed field
# Binaries are compared using the internal integer value they represent
		
	def __lt__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data < val.data
		return self.data < intify(val)[0]
		
	def __gt__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data > val.data
		return self.data > intify(val)[0]
			
	def __le__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data <= val.data
		return self.data <= intify(val)[0]
			
	def __ge__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data >= val.data
		return self.data >= intify(val)[0]
			
#exact comparrison operators(accounts for length and sign of binary provided)
#try converting both to signed or unsigned if sign is to be ignored
#	Binary(-1,True,8) == Binary(255,False,8) is False
#	Binary(-1,True,8) == Binary(255).signed() is True
#	Binary(-1,True,8).unsigned() == Binary(255) is True
#	both = 0b 1111 1111
#try converting both to the same length if it is to be ignored (I recommend using length max(length1,length2))
#	Binary(-1) == Binary(255) is False
#	= 0b1         = 0b 1111 1111
#	Binary(-1,False,8) == Binary(255,False,8) is True

	def __eq__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data == val.data and self.length == val.length
		return self.data == intify(val,self.isSigned)[0]
			
	def __ne__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to compare")
		if isinstance(val, Binary):
			if val.data is None:
				raise Exception("Binary argument has no value to compare")
			return self.data != val.data or self.length != val.length
		return self.data != intify(val,self.isSigned)[0]

# bitwise:
# retain signed status

	def __lshift__(self, amount):
		return self.shifted(amount, "left")
	
	#handled aritmetically if object is signed
	def __rshift__(self, amount):
		if self.isSigned:
			return self.shifted(amount, "right", "arithmetic")
		else:
			return self.shifted(amount, "right")
		
	# direction = ["left","right"] special = ["barrel" or "curcular","arithmetic",None]
	def shifted(self, shiftAmnt = 1, direction = "left", special = None):
		if self.data is None:
			raise Exception("Binary has no value to shift")
		tempBin = self.toBin()[2:]
		if direction == "right":
			if special in ["barrel","circular"]:
				shiftAmnt = shiftAmnt%len(tempBin)
				keptBits = tempBin[:len(tempBin)-shiftAmnt] #copy first part of string
				result = tempBin[len(tempBin)-shiftAmnt:] + keptBits #add second part to front
			else:
				if shiftAmnt > len(tempBin): #ensure more bits aren't added
					shiftAmnt = len(tempBin)
				keptBits = tempBin[:len(tempBin)-shiftAmnt] #copy first part of string
				if special == "arithmetic":
					result = (tempBin[0] * shiftAmnt) + keptBits  #copy sign from first bit. repeat "shiftamnt" times
				else:
					result = ("0" * shiftAmnt) + keptBits #repeats 0 "shiftamnt" times
		elif direction == "left":
			if special in ["barrel", "circular"]:
				shiftAmnt = shiftAmnt%len(tempBin)
				keptBits = tempBin[shiftAmnt:]			#copy last part of string
				result = keptBits + tempBin[:shiftAmnt]	#add first part of string to end
			else:
				result = tempBin + "0" * shiftAmnt
		else:
			raise Exception('Expected "left" or "right" as direction argument')
		return Binary("0b" + result,self.isSigned)

#logical operators
#arguments other than Binary are treaded as unsigned
#result signed if argument binary signed
	def __invert__(self): #this one is weird because it has to avoid bit length increase
		if self.data is None:
			raise Exception("Binary has no value to operate on")	
		retVal = Binary(~self.signed().data,True,self.length)
		if self.isSigned:
			return retVal
		return retVal.unsigned()
		
	def __and__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		if isinstance(val, Binary):
			newSigned = self.isSigned or val.isSigned
		else:
			val = Binary(val,intify(val)[0]<0) #negative argument -> signed binary
			newSigned = self.isSigned
		newLen = max(self.length, val.length)
		return Binary(binify(self.resized(newLen).toUint() & val.resized(newLen).toUint(),False,newLen),self.isSigned)
	
	def __or__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")    
		if isinstance(val, Binary):
			newSigned = self.isSigned or val.isSigned
		else:
			val = Binary(val,intify(val)[0]<0)
			newSigned = self.isSigned
		newLen = max(self.length, val.length)
		return Binary(binify(self.resized(newLen).toUint() | val.resized(newLen).toUint(),False,newLen),self.isSigned)
	
	def __xor__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")	
		if isinstance(val, Binary):
			newSigned = self.isSigned or val.isSigned
		else:
			val = Binary(val,intify(val)[0]<0)
			newSigned = self.isSigned
		newLen = max(self.length, val.length)
		return Binary(binify(self.resized(newLen).toUint() ^ val.resized(newLen).toUint(),False,newLen),self.isSigned)

#arithmetic operators 
#arguments other than Binary are treaded as signed
	def __add__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		if isinstance(val, Binary):
			tempVal = val
		else:
			tempVal = Binary(val,True,self.length)
		tempLen = max(len(self),len(tempVal))
		return tempVal.set(self.data + tempVal.data, self.isSigned or tempVal.isSigned, tempLen)
	
	def __sub__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		if isinstance(val, Binary):
			tempVal = val
		else:
			tempVal = Binary(val,True,self.length)
		tempLen = max(len(self),len(tempVal))
		return tempVal.set(self.data - tempVal.data, self.isSigned or tempVal.isSigned, tempLen)
		
	def __mul__(self, val):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		if isinstance(val, Binary):
			tempVal = val
		else:
			tempVal = Binary(val,True,self.length)
		tempLen = max(len(self),len(tempVal))
		return tempVal.set(self.data * tempVal.data, self.isSigned or tempVal.isSigned, tempLen)
		
	#TODO what to do if unsigned
	def __neg__(self):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		return Binary(-self.data,self.isSigned,self.length)    
		
	#essentially returns a copy
	def __pos__(self):
		if self.data is None:
			raise Exception("Binary has no value to operate on")
		return Binary(+self.data,self.isSigned,self.length)
	
# indexing / list operations

	#put the binary representation of the object in the lower bits and self in the higher order bits
	def putBefore(self, object):
		object = Binary(object)
		return Binary(self.toBin() + object.toBin()[2:],self.isSigned or object.isSigned)
		
	#what to do if signed and begins with 1
	def putAfter(self, object):
		object = Binary(object)
		return Binary(object.toBin() + self.toBin()[2:],self.isSigned or object.isSigned)
		
	def inserted(self, object, index):
		object = Binary(object)
		return self[:index] // object // self[index:]
		
	def removed(self, index):
		return self[:index] // self[index+1:]
		
	# use // to concatenate Binaries with high order on the left and low order on the right
	def __floordiv__(self,object):
		return self.putBefore(object)

	#returns Binary(1) or Binary(0)
	def __getitem__(self, index):
		if self.data is None:
			return Binary(None,self.isSigned)
		return Binary("0b" + (self.toBin()[2:][index]))
	
	def __iter__(self):
		if self.data is None:
			return iter([Binary(None,self.isSigned)])
		return map(Binary,self.toBin()[2:])
		
	def __reversed__(self):
		if self.data is None:
			return reversed([Binary(None,self.isSigned)])
		return map(Binary,reversed(self.toBin()[2:]))
	
	def __contains__(self, val):
		if self.data is None:
			return False
		if not isinstance(val, Binary):
			val = Binary(val)
		if val.data is None:
			return False
		return val.toBin()[2:] in self.toBin()[2:]
		



#typeString is (bin,int,hex,oct) or None
#tries to infer type by preceeding base designator (0b,0o,0x)
#"-" negates a value.
#returns intValue, binLength (same as provided except in cases below)
#1) negating signed negative powers of 2 increases the number of bits required above the given length
#    0b 1000 0000 (signed) = -128
#   -0b 1000 0000 (signed) = 128 = 0b 0 1000 0000 (signed)
#2) binLength = None if the value is negative and unsigned
def strToInt(string, signed = False, typeString = None):
	if string.startswith("-"):
		string = string[1:]
		negate = True
	else:
		negate = False
	#binary
	if string.startswith("0b") or typeString == "bin":
		if string.startswith("0b"):
			if typeString is not None and typeString != "bin":
				raise Exception('Unexpected type argument for string with "0b" heading: ' + str(typeString))
			string = string[2:]
			if string == '':
				return None, 0
		result = int(string,2)
		lenResult = len(string)
		if signed and string.startswith("1"):
			result = forceNeg(result)
	#octal
	elif string.startswith("0o") or typeString == "oct":
		if string.startswith("0o"):
			if typeString is not None and typeString != "oct":
				raise Exception('Unexpected type argument for string with "0o" heading: ' + str(typeString))
			string = string[2:]
			if string == '':
				return None, 0
		result = int(string,8)
		lenResult = len(string) * 3
		if signed and any(string.startswith(test) for test in "4567"):
			result = forceNeg(result)
	#hexadecimal
	elif string.startswith("0x") or typeString == "hex":
		if string.startswith("0x"):
			if typeString is not None and typeString != "hex":
				raise Exception('Unexpected type argument for string with "0x" heading: ' + str(typeString))
			string = string[2:]
			if string == '':
				return None, 0
		result = int(string,16)
		lenResult = len(string) * 4
		if signed and any(string.startswith(test) for test in "89abcdef"):
			result = forceNeg(result)
	#decimal
	elif typeString is None or typeString == "dec": 
		result = int(string)
		if negate:
			result = -result
		if not signed and result < 0:
			return result, None
		return result, bitLen(result,signed)
	else:
		raise Exception("Invalid typeString argument: " + str(typeString))	
		
	if negate:
		result = -result
	lenResult = max(bitLen(result,signed),lenResult) # minimum bitlength returned if bit length supplied is not enough
	return result, lenResult

#quick big-endian translation
#returns value, length (multiple of 8)
# 1111 0000 signed   = -16,8
# 1111 0000 unsigned = 240,8
# 0000 1111 signed   = 15,8
# 0000 1111 unsigned = 15,8
def bytesToInt(byteData, signed=False):
	intVal = int.from_bytes(byteData, "big")
	if signed and byteData[0] > 128: #negative (has leading 1)
		return forceNeg(intVal), 8 * len(byteData)
	else: #positive
		return intVal, 8 * len(byteData)

#returns string of 1's and 0's with preceeding base designator "0b"
def binify(object, signed=False, length = None, stringType=None):
	val, intLen = intify(object, signed, stringType)
	result = bin(forcePos(val))[2:]
	if intLen is None:
		intLen = bitLen(val)
	if isinstance(length, int):
		intLen = max(intLen,length)
	amount = intLen - len(result) #result should always be 0 or more
	if signed and val < 0: 
		return "0b" + (amount * "1") + result
	else:
		return "0b" + (amount * "0") + result

#returns intValue, bitLength (same as provided except in cases below)
#1) negating signed negative powers of 2 increases the number of bits required above the given length
#    0b 1000 0000 (signed) = -128
#   -0b 1000 0000 (signed) = 128 = 0b 0 1000 0000 (signed)
#2) bitLength = None if the value is negative and unsigned
#+int signed:    9=01001 returns  9,5
#-int signed:   -7=1001  returns -7,4
#+int unsigned:  9=1001  returns  9,4
#-int unsigned: -7=1001  returns -7,None
def intify(object, signed=False, stringType=None):
	if isinstance(object, bytes):
		return bytesToInt(object, signed)
	elif isinstance(object, str):
		return strToInt(object, signed, stringType)
	elif isinstance(object, int):
		if not signed and object < 0:
			return object, None
		return object, bitLen(object, signed)
	elif object is None:
		return None,0
	else:
		raise TypeError("Expected bytes, int, or str type argument")
		
#returns the value of an integer if its smallest binary representation (starts with 1) was to be treated as negative ex: 5 = 101 = -3
#exact binary value and length maintained
def forceNeg(intVal):
	if intVal > 0:
		return intVal - (1<<int.bit_length(intVal))
	else:
		return intVal

#returns the value of an integer if its smallest binary representation (starts with 1) was to be treated as positive ex: -7 = 1001 = 9
#exact binary value and length maintained
def forcePos(intVal):
	if intVal < 0:
		return (1<<bitLen(intVal)) + intVal #adds a negative intVal
	else:
		return intVal
		
#returns minimum bit lenght required to represent the value
#int.bit_length but supports negative numbers and signed mode (positives have a leading 0, all negatives despite sign have leading 1)
#use int.bit_length for values known to be positive to reduce computation time
def bitLen(intVal, signed = False):
	tempVal = int.bit_length(intVal) #catches non-integers
	if intVal < 0 and 1<<tempVal-1 != -intVal: #if not a power of 2. (corrects for int.bit_length being one off for sign bit on all except powers of two)
		tempVal += 1
	elif intVal > 0 and signed: #add a sign bit to positive numbers if signed
		tempVal += 1
	elif intVal == 0: #bit_length doesn't work for 0
		return 1
	return tempVal
		
		