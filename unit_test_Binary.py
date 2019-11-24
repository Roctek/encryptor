from Binary import *

def testFP():
	print("ForcePos")
	print(forcePos(3) == 3)
	print(forcePos(2) == 2)
	print(forcePos(1) == 1)
	print(forcePos(0) == 0)
	print(forcePos(-1) == 1)
	print(forcePos(-2) == 2)
	print(forcePos(-3) == 5)
	print(forcePos(-4) == 4)
	print(forcePos(-5) == 11)
	print(forcePos(-6) == 10)
	print(forcePos(-7) == 9)
	print(forcePos(-8) == 8)
	print(forcePos(-9) == 23)
	print(forcePos(-20) == 44)
	print(forcePos(-400) == 624)
	
def testFN():
	print("ForceNeg")
	print(forceNeg(-3) == -3)
	print(forceNeg(-2) == -2)
	print(forceNeg(-1) == -1)
	print(forceNeg(0) == 0)
	print(forceNeg(1) == -1)
	print(forceNeg(2) == -2)
	print(forceNeg(3) == -1)
	print(forceNeg(4) == -4)
	print(forceNeg(5) == -3)
	print(forceNeg(6) == -2)
	print(forceNeg(7) == -1)
	print(forceNeg(8) == -8)
	print(forceNeg(20) == -12)
	print(forceNeg(350) == -162)
	
def testBitLen():
	print("BitLen")
	print(bitLen(-9) == 5)
	print(bitLen(-8) == 4)
	print(bitLen(-7) == 4)
	print(bitLen(-6) == 4)
	print(bitLen(-5) == 4)
	print(bitLen(-4) == 3)
	print(bitLen(-3) == 3)
	print(bitLen(-2) == 2)
	print(bitLen(-1) == 1)
	print(bitLen(0) == 1)
	print(bitLen(1) == 1)
	print(bitLen(2) == 2)
	print(bitLen(3) == 2)
	print(bitLen(4) == 3)

def testIntify():
	print("Intify")
	print("BIN")
	print(intify("0b1001",True) == (-7,4))
	print(intify("0b1001",False) == (9,4))
	print(intify("0b01001",True) == (9,5))
	print(intify("0b01001",False) == (9,5))
	print(intify("-0b1001",True) == (7,4))
	print(intify("-0b1001",False) == (-9,5)) #negative number always signed
	print(intify("-0b01001",True) == (-9,5))
	print(intify("-0b01001",False) == (-9,5))
	print(intify("-01001",False,"bin") == (-9,5))
	print("OCT")
	print(intify("0o6",True) == (-2,3))
	print(intify("0o6",False) == (6,3))
	print(intify("0o11",True) == (9,6))
	print(intify("0o11",False) == (9,6))
	print(intify("-0o6",True) == (2,3))
	print(intify("-0o6",False) == (-6,4))
	print(intify("-0o11",True) == (-9,6))
	print(intify("-0o11",False) == (-9,6))
	print(intify("-11",False,"oct") == (-9,6))
	print("HEX")
	print(intify("0xa",True) == (-6,4))
	print(intify("0xa",False) == (10,4))
	print(intify("0x10",True) == (16,8))
	print(intify("0x10",False) == (16,8))
	print(intify("-0xa",True) == (6,4))
	print(intify("-0xa",False) == (-10,5))
	print(intify("-0x10",True) == (-16,8))
	print(intify("-0x10",False) == (-16,8))
	print(intify("-0x10",False,"hex") == (-16,8))
	print("DEC")
	print(intify("111",True) == (111,8))
	print(intify("111",False) == (111,7))
	print(intify("-111",True) == (-111,8))
	print(intify("-111",False) == (-111,None))
	print(intify("-111",False,"dec") == (-111,None))
	print(intify(111,True) == (111,8))
	print(intify(111,False) == (111,7))
	print(intify(-111,True) == (-111,8))
	print(intify(-111,False) == (-111,None))
	print("BYTES")
	print(intify(int.to_bytes(157,1,'big'),True) == (-99,8))
	print(intify(int.to_bytes(157,1,'big'),False) == (157,8))
	print(intify(int.to_bytes(78,1,'big'),True) == (78,8))
	print(intify(int.to_bytes(78,1,'big'),False) == (78,8))
	
	#TODO REWRITE
def testBinify():
	print("Binify")
	print("BIN")
	print(binify("0b1001",True) == "0b1001")
	print(binify("0b1001",False) == "0b1001")
	print(binify("0b01001",True) == "0b01001")
	print(binify("0b01001",False)== "0b01001")
	print(binify("-0b1001",True) == "0b0111")
	print(binify("-0b1001",False) == "0b10111")
	print(binify("-0b01001",True) == "0b10111")
	print(binify("-0b01001",False) == "0b10111")
	print(binify("-01001",False,None,"bin") == "0b10111")
	print("OCT")
	print(binify("0o6",True) == "0b110")
	print(binify("0o6",False) == "0b110")
	print(binify("0o11",True) == "0b001001")
	print(binify("0o11",False) == "0b001001")
	print(binify("-0o6",True) == "0b010")
	print(binify("-0o6",False) == "0b1010")
	print(binify("-0o11",True) == "0b110111")
	print(binify("-0o11",False) == "0b010111")
	print(binify("-11",False,None,"oct") == "0b010111")
	print("HEX")
	print(binify("0xa",True) == "0b1010")
	print(binify("0xa",False) == "0b1010")
	print(binify("0x10",True) == "0b00010000")
	print(binify("0x10",False) == "0b00010000")
	print(binify("-0xa",True) == "0b0110")
	print(binify("-0xa",False) == "0b10110")
	print(binify("-0x10",True) == "0b11110000")
	print(binify("-0x10",False) == "0b00010000")
	print(binify("-0x10",False,None,"hex") == "0b00010000")
	print("DEC")
	print(binify("111",True) == "0b01101111")
	print(binify("111",False) == "0b1101111")
	print(binify("-111",True) == "0b10010001")
	print(binify("-111",False) == "0b10010001")
	print(binify("-111",False,None,"dec") == "0b10010001")
	print(binify(111,True) == "0b01101111")
	print(binify(111,False) == "0b1101111")
	print(binify(-111,True) == "0b10010001")
	print(binify(-111,False) == "0b10010001")
	print("BYTES")
	print(binify(int.to_bytes(157,1,'big'),True) == "0b10011101")
	print(binify(int.to_bytes(157,1,'big'),False) == "0b10011101")
	print(binify(int.to_bytes(78,1,'big'),True) == "0b01001110")
	print(binify(int.to_bytes(78,1,'big'),False) == "0b01001110")
	
	
	
	

def testBinaryInit():
	print("Init")
	print(Binary(20).toBin() == "0b10100")
	print(int(Binary(20)) == 20)
	print(Binary(-5).toBin() == "0b1011")
	print(int(Binary(-5)) == 11)
	print(Binary("0b111").toBin() == "0b111")
	print(int(Binary("0b111")) == 7)
	print(Binary("0x10").toBin() == "0b00010000")
	print(int(Binary("0x10")) == 16)
	print(Binary("0o13").toBin() == "0b001011")
	print(int(Binary("0o13")) == 11)
	print(Binary("test".encode()).toBin() == "0b01110100011001010111001101110100")
	
	print(Binary(20,True).toBin() == "0b010100")
	print(int(Binary(20,True)) == 20)
	print(Binary(-5,True).toBin() == "0b1011")
	print(int(Binary(-5,True)) == -5)
	print(Binary("0b111",True).toBin() == "0b111")
	print(int(Binary("0b111",True)) == -1)
	print(Binary("0xd",True).toBin() == "0b1101")
	print(int(Binary("0xd",True)) == -3)
	print(Binary("0o4",True).toBin() == "0b100")
	print(int(Binary("0o4",True)) == -4)
	print(Binary("test".encode(),True).toBin() == "0b01110100011001010111001101110100")
	
	print(Binary(20,False,16).toBin() == "0b0000000000010100")
	print(int(Binary(20,False,16)) == 20)
	print(Binary(-5,False,16).toBin() == "0b1111111111111011")
	print(int(Binary(-5,False,16)) == 65531)
	print(Binary("0b111",False,16).toBin() == "0b0000000000000111")
	print(int(Binary("0b111",False,16)) == 7)
	print(Binary("0xd",False,16).toBin() == "0b0000000000001101")
	print(int(Binary("0xd",False,16)) == 13)
	print(Binary("0o4",False,16).toBin() == "0b0000000000000100")
	print(int(Binary("0o4",False,16)) == 4)
	print(Binary("test".encode(),False,48).toBin() == "0b000000000000000001110100011001010111001101110100")
	
	print(Binary(20,True,16).toBin() == "0b0000000000010100")
	print(int(Binary(20,True,16)) == 20)
	print(Binary(-5,True,16).toBin() == "0b1111111111111011")
	print(int(Binary(-5,True,16)) == -5)
	print(Binary("0b111",True,16).toBin() == "0b1111111111111111")
	print(int(Binary("0b111",True,16)) == -1)
	print(Binary("0xd",True,16).toBin() == "0b1111111111111101")
	print(int(Binary("0xd",True,16)) == -3)
	print(Binary("0o4",True,16).toBin() == "0b1111111111111100")
	print(int(Binary("0o4",True,16)) == -4)
	print(Binary("test".encode(),True,48).toBin() == "0b000000000000000001110100011001010111001101110100")
	
	print(Binary().toBin() == '0b')
	print(Binary(None,True,10).toBin() == '0b')
	
def testBytes():
	print("Bytes")
	print(Binary("test".encode()).toBytes() == b'test')
	print(bytes(Binary(5,True)) == b'\x05')  
	print(bytes(Binary(-5,True)) == b'\x0b')
	print(bytes(Binary(5,True,20)) == b'\x00\x00\x05')
	print(bytes(Binary(-5,True,20)) == b'\x0f\xff\xfb')
	print(bytes(Binary(0)) == b'\x00')
	
	#I shoved bool in here too
	print(bool(Binary(5,True)))
	print(bool(Binary(-5,True)))
	print(not bool(Binary(0)))
	
	try:
		bytes(Binary())
		print(False)
	except Exception:
		print(True)
	
def testHex():
	print("Hex")
	print(Binary(5,True).toHex() == '0x5')  
	print(Binary(-5,True).toHex() == '0xb')
	print(Binary(5,True,20).toHex() == '0x00005')
	print(Binary(-5,True,20).toHex() == '0xffffb')
	print(Binary(0).toHex() == '0x0')
	
	try:
		Binary().toHex()
		print(False)
	except Exception:
		print(True)
	
def testCompare():
	print("Compare")
	print(Binary(5) == 5)
	print(Binary(-4,True) == -4)
	print(Binary(-4) != -4)
	print(Binary(-15,True,10) == Binary(-15,True,10))
	print(Binary(-15,True,10) != Binary(-15,False,10))
	print(Binary(-15,True,20) != Binary(-15,True,10))
	print(Binary(-15,False,20) != Binary(-15,False,10))
	print(Binary("0b1001",False) != Binary("0b1001",True))
	print(Binary(10) < Binary(20))
	print(Binary(10,True) < Binary(20,True))
	print(Binary(-5) > Binary(3)) #unsigned
	print(Binary(-10,True) > Binary(-20,True))
	print(Binary(5) <= 6)
	print(Binary(5) <= 5)
	print(Binary(5) >= 5)
	print(Binary(5) >= 4)
	print(not Binary(5) == 4)
	print(not Binary(-4) == -4)
	print(not Binary("0b1001",True) != Binary("0b1001",True))
	print(not Binary(10) > Binary(20))
	print(not Binary(10,True) > Binary(20,True))
	print(not Binary(-5) < Binary(3)) #unsigned
	print(not Binary(-10,True) < Binary(-20,True))
	print(not Binary(5) >= 6)
	print(not Binary(5) != 5)
	print(not Binary(5) <= 4)
	
	#with self.shifted() sign only affects integer representation after shift
	#with shift operator (>>) sign maintained (arithmetic shift)
def testShift():
	print("Shift")
	print(Binary("0b1100").shifted(1,"left","barrel").toBin() == "0b1001")
	print(int(Binary("0b1100",False).shifted(1,"left","barrel")) == 9)
	print(int(Binary("0b1100",True).shifted(1,"left","barrel")) == -7)
	print(Binary("0b1100").shifted(1,"left").toBin() == "0b11000")
	print(Binary("0b1100").shifted(1,"right","barrel").toBin() == "0b0110")
	print(Binary("0b1100").shifted(1,"right").toBin() == "0b0110")
	print(Binary("0b1100").shifted(1,"right","arithmetic").toBin() == "0b1110")

	print(Binary("0b1100").shifted(3,"left","barrel").toBin() == "0b0110")
	print(Binary("0b1100").shifted(3,"left").toBin() == "0b1100000")
	print(Binary("0b1100").shifted(3,"right","barrel").toBin() == "0b1001")
	print(Binary("0b1100").shifted(3,"right").toBin() == "0b0001")
	print(Binary("0b1100").shifted(3,"right","arithmetic").toBin() == "0b1111")

	print(Binary("0b1100").shifted(50,"left","barrel").toBin() == "0b0011")
	print(Binary("0b1100").shifted(50,"left").toBin() == "0b110000000000000000000000000000000000000000000000000000")
	print(Binary("0b1100").shifted(50,"right","barrel").toBin() == "0b0011")
	print(Binary("0b1100").shifted(50,"right").toBin() == "0b0000")
	print(Binary("0b1100").shifted(50,"right","arithmetic").toBin() == "0b1111")

	print((Binary("0b1010")<<5).toBin() == "0b101000000")
	print((Binary("0b10101110")>>3).toBin() == "0b00010101")
	print((Binary("0b10101110",True)>>3).toBin() == "0b11110101")
	
	try:
		Binary() << 2
		print(False)
	except Exception:
		print(True)
		
	try:
		Binary() >> 2
		print(False)
	except Exception:
		print(True)
	
def testBitwise():
	print("Bitwise")
	#not
	print((~Binary("0b10011001")).toBin() == "0b01100110")
	print((~Binary("0b01100110")).toBin() == "0b10011001")
	print((~Binary("0b10011001",True)).toBin()  == "0b01100110")
	print((~Binary("0b01100110",True)).toBin()  == "0b10011001")
	print(~Binary(0) == "1")
	print(int(~Binary(0)) == 1)
	print(int(~Binary(0,True)) == -1)

	print((Binary("0b0000000011111111") & Binary("0b1001001110010011")).toBin() == "0b0000000010010011") #and
	print((Binary("0b0000000011111111") | Binary("0b1001001110010011")).toBin() == "0b1001001111111111") #or
	print((Binary("0b0000000011111111") ^ Binary("0b1001001110010011")).toBin() == "0b1001001101101100") #xor
	
	print((Binary("0b110000",True) & Binary("0b1001001110010011")).toBin() == "0b1001001110010000") #and
	print((Binary("0b1001001110010011") & Binary("0b110000",True)).toBin() == "0b1001001110010000") #and
	print((Binary("0b110000",True) | Binary("0b1001001110010011")).toBin() == "0b1111111111110011") #or
	print((Binary("0b1001001110010011") | Binary("0b110000",True)).toBin() == "0b1111111111110011") #or
	print((Binary("0b110000",True) ^ Binary("0b1001001110010011")).toBin() == "0b0110110001100011") #xor
	print((Binary("0b1001001110010011") ^ Binary("0b110000",True)).toBin() == "0b0110110001100011") #xor
	
	print(int(Binary(-1,True) & 12) == -4) #sign retained
	print(int(Binary(-1) & 12) == 0)
	print(int(Binary(12) & -1) == 12)
	print((Binary(12,True) & -1) == '0b01100')
	print((Binary(12,True) | -1) == '0b11111')
	print(int(Binary(12,True) & -1) == 12)
	print(int(Binary(12,True) | -1) == -1)
	
#TODO: add to init
def testInitWithBin():
	print("Initializing with binary")
	print(Binary(Binary(10),False,6).toBin() == "0b001010")
	print(int(Binary(Binary(10),False,6)) == 10)
	print(Binary(Binary(-10,True),True,6).toBin() == "0b110110")
	print(int(Binary(Binary(-10,True),True,6)) == -10)
	
	try:
		Binary(Binary(10),False,2)
		print(False)
	except Exception:
		print(True)
		
	print(Binary(Binary(10,True),False).toBin() == "0b01010") #sign bit maintained with length
	print(Binary(Binary(-10), True) == "0b10110")
	print(Binary(Binary(-10), True) == -10)
	print(Binary(Binary(0,True),False,10).toBin() == "0b0000000000")
	print(Binary(Binary(-12),True,10).toBin() == "0b1111110100")
	
	print(Binary(Binary(),True).toBin() == '0b')
	
def testIndexing():
	print("Indexing")
	print(Binary("0b1010111")[0] == "0b1")
	print(Binary("0b1010111")[1:3] == "0b01")
	print(Binary("0b1010111")[3:] == Binary("0b0111"))
	print(Binary("0b1010111")[:] == Binary("0b1010111"))
	
	print(list(iter(Binary("0b1010111"))) == ["1","0","1","0","1","1","1"])
	print(list(reversed(Binary("0b1010111"))) == ["1","1","1","0","1","0","1"])
	print("0b1010" in Binary("0b1010111"))
	print("0b1010" not in Binary(0))
	print(Binary("0b1111") in Binary("0x8f"))

	print(list(iter(Binary()))[0].data is None)
	print(list(reversed(Binary()))[0].data is None)
	print(Binary() not in Binary(4))
	print(Binary() not in Binary())
	print("4" not in Binary())
	print(list(iter(Binary()))[0].data is None)
	
def testUnsigned():
	print("To Unsigned Int")
	print(Binary("0b1111",True).toUint() == 15)
	print(Binary("0b1111").toUint() == 15)
	print(Binary(64).toUint() == 64)
	print(Binary(-64,True).toUint() == 64)
	print(Binary(-64).toUint() == 64)
	print(Binary(-7,True).toUint() == 9)
	
def testSignChange(): #underlying code tested in testInitWithBin
	print("Sign Change")
	print(int(Binary(18).signed()) == -14)
	print(int(Binary(-18).signed()) == -18)
	print(int(Binary(18,True).unsigned()) == 18)
	print(int(Binary(-18,True).unsigned()) == 46)
	print(Binary('0b1001').signed().toBin() == '0b1001')
	print(Binary('0b1001',True).unsigned().toBin() == '0b1001')
	
	print(Binary(None,False).signed().isSigned)
	print(Binary(None,True).unsigned().isSigned == False)

def testResize():  #underlying code tested in testInitWithBin
	print("Resize")
	print(Binary('0b1001').resized(5).toBin() == '0b01001')
	print(Binary('0b1001',True).resized(5).toBin() == '0b11001')
	
	try:
		Binary('0b1001').resized(3)
		print(False)
	except Exception:
		print(True)
		
	print(Binary('0b1001').resized(3,True) == "0b001")
		
		
def testPut():
	print("Put")
	print(Binary('0b1001').putBefore('0b0110').toBin() == '0b10010110')
	print(Binary('0b1001').putAfter('0b0110').toBin() == '0b01101001')
	print((Binary('0b1110',True) // Binary('0b0000')).toBin() == '0b11100000')
	print(Binary().putAfter('0b0110').toBin() == '0b0110')
	print(Binary().putBefore('0b0110').toBin() == '0b0110')
	

def testEmpty():
	print("Empty")
	for function in ['__add__', '__and__','__eq__', '__ge__', '__gt__', '__le__', '__lt__','__mul__', '__ne__', '__or__','__sub__','__xor__']:
		try:
			getattr(Binary(),function)(Binary(4))
			print(False)
		except Exception:
			print(True)
		try:
			getattr(Binary(4),function)(Binary())
			print(False)
		except Exception:
			print(True)
	
	for function in ['__invert__','__neg__','__pos__']:
		try:
			getattr(Binary(),function)()
			print(False)
		except Exception:
			print(True)
			
def testInsertRemove():
	print(Binary('0b10000001').inserted('0b11',4) == Binary('0b1000110001'))
	print(Binary('0b10000001').inserted('0b11',0) == Binary('0b1110000001'))
	print(Binary('0b10000001').inserted('0b11',8) == Binary('0b1000000111'))
	
	print(Binary('0b10101010').removed(0) == Binary('0b0101010'))
	print(Binary('0b10101010').removed(4) == Binary('0b1010010'))
	print(Binary('0b10101010').removed(7) == Binary('0b1010101'))
	
if __name__ == "__main__":
#independent functions
	testFP()
	testFN()
	testBitLen()
	testIntify()
	testBinify()
#Binary methods
	testBinaryInit()
	testBytes()
	testHex()
	testCompare()
	testShift()
	testInitWithBin()
	testBitwise()
	testIndexing()
	testUnsigned()
	testSignChange()
	testResize()
	testPut()
	testEmpty()
	testInsertRemove()





