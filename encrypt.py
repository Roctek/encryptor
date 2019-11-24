from SymmetricEncryptor import SymmetricEncryptor
from Binary import Binary
import pickle
import sys
NL = "\n"
HELPSPACING = int(12)
BORDERSIZE = int(60)
DEBUG = False

class encryptUI:
	def __init__(self):
		self.state = "listen"
		self.modified = False
		self.lastOpened = None
		self.lastPass = None
		self.passwords = {}
		self.encryptor = SymmetricEncryptor()

#************************************************************************************
#	Methods
#************************************************************************************

	def getHelpStr(self):
		return (
		("*" * (BORDERSIZE)) + " Commands " + ("*" * (BORDERSIZE)) + NL +
		helpEntry("quit", "stop running the script") +
		helpEntry("read", "read password dictionary from a file previously encrypted using the same scheme") +
		helpEntry("","read <filename>") +
		helpEntry("write", "write the current password dictionary to the specified file using the current encryption scheme") +
		helpEntry("","write <filename>") +
		helpEntry("set", "store the given password in the current password dictionary with the given label") +
		helpEntry("","set <label> <password>") +
		helpEntry("get","read the currently stored password with the given label") +
		helpEntry("","get <label>") +
		helpEntry("remove","remove the currently stored password with the given label") +
		helpEntry("","remove <label>") +
		helpEntry("labels","print all labels in the dictionary to the screen") +
		helpEntry("dump","print all labels with corresponding passwords to the screen") +
		helpEntry("pass","set the password so that you do not have to specify it for each command") +
		helpEntry("","note: this field gets updated automatically whenever a different password is used") +
		helpEntry("","pass <new password>") +
		helpEntry("file","set the filename so that you do not have to specify it for each command") +
		helpEntry("","note: this field gets updated automatically whenever a different filename is used") +
		helpEntry("","file <filename>") +
		helpEntry("encrypt","print the result of encrypting the specified string with the given password in Hexadecimal representation") +
		helpEntry("","note: the length is also provided as preceeding zero bits may or may not present") +
		helpEntry("","encrypt <string to encrypt> <password>") +
		helpEntry("decrypt", "print the result of decrypting the specified hexadecimal or binary string of specified length with the given password in 'latin-1' encoding") +
		helpEntry("","note: if no length argument is provided, all preceeding zeros are considered significant") +
		helpEntry("","note: Hex string begin with '0x' and binary begin with '0b'. No type designator is considered decimal") +
		helpEntry("","decrypt <hex string> <password> <length(optional)>") +
		("*" * (2*BORDERSIZE + 10)) + NL
		)
		
	def setFilePass(self, password):
		self.lastPass = password
	
	def setFile(self, filename):
		self.lastOpened = filename
		
	def readFile(self, filename=None, password=None):
		if filename is None:
			if self.lastOpened is not None:
				filename = self.lastOpened
			else:
				print("no specified file to read")
				return False
		if password is None:
			if self.lastPass is not None:
				password = self.lastPass
			else:
				print("no specified password for encryption")
				return False
		try:
			fobj = open(filename,'r')
			length, binData = fobj.read().split('0x')
			if not length.isdigit():
				raise TypeError("Expected integer length precursing the data")
			decData = self.encryptor.decrypt(Binary("0x" + binData).resized(int(length),True),password)
			loadObj = pickle.loads(bytes(decData))
			if not isinstance(loadObj, dict):
				raise pickle.PickleError("expected encoded dictionary object")
			for key, val in loadObj.items():
				if not isinstance(key, str):
					raise pickle.PickleError("non-string key detected")
				if not isinstance(val, str):
					raise pickle.PickleError("non-string password detected")
			for key, val in loadObj.items():
				self.passwords[key] = val
			fobj.close()
			self.lastOpened = filename
			self.lastPass = password
			return True
		except pickle.PickleError as error:
			if DEBUG:
				print("error decrypting file: " + str(error))
			else:
				print("Incorrect Password!")
			return False
		except Exception as error:
			print("error loading file: " + str(filename) + ": " + str(error))
			return False
	
	def writeFile(self, filename=None, password=None):
		if len(self.passwords) < 1:
			print("no data to write to file")
			return False
		if filename is None:
			if self.lastOpened is not None:
				filename = self.lastOpened
			else:
				print("no specified file to write to")
				return False
		if password is None:
			if self.lastPass is not None:
				password = self.lastPass
			else:
				print("no specified password for encryption")
				return False
		try:
			fobj = open(filename,'w')
			binData = pickle.dumps(self.passwords)
			encData = self.encryptor.encrypt(binData,password)
		#test decryption
			decData = self.encryptor.decrypt(Binary(encData.toHex()).resized(len(encData),True),password)
			loadObj = pickle.loads(bytes(decData))
			if not isinstance(loadObj, dict):
				raise pickle.PickleError("Decryption Test expected encoded dictionary object")
			for key, val in loadObj.items():
				if not isinstance(key, str):
					raise pickle.PickleError("Decryption Test detected non-string key")
				if not isinstance(val, str):
					raise pickle.PickleError("Decryption Test detected non-string password")
			if loadObj != self.passwords:
				raise Exception("Decryption Test failed to reproduce password data")
			fobj.write(str(len(encData)))
			fobj.write(encData.toHex())
			fobj.close()
			self.modified = False
			self.lastOpened = filename
			self.lastPass = password
			return True
		except Exception as error:
			print("error writing to file: " + str(filename) + ": " + str(error))
			return False
	
	def setPass(self, key, password):
		try:
			self.passwords[key] = password
			self.modified = True
		except Exception as error:
			print("Error updating the password dictionary: " + str(error))
	
	def removePass(self, key):
		try:
			del self.passwords[key]
			self.modified = True
		except Exception as error:
			print("Error removing password from dictionary: " + str(error))			

	def getPass(self, key=None):
		if key is None:
			self.showLabels()
		elif key in self.passwords:
			print(self.passwords[key])
		else:
			print("no password for: " + str(key))
			
	def showPasswords(self):
		print("*** Password List ***")
		for key, value in self.passwords.items():
			print(key + " : " + value)
		print("*********************")
			
	def showLabels(self):
		print("*** Label List ***")
		for key in self.passwords.keys():
			print(key)
		print("******************")
	
	def encryptStr(self, string, password):
		encrypted = self.encryptor.encrypt(string.encode(),password)
		print(encrypted.toHex())
		print("length: " + str(len(encrypted)))
		return True
		
	def decryptBin(self, string, password, length=None):
		if length is not None:
			length = int(length)
		print(self.encryptor.decrypt(Binary(string,False,length),password).toBytes().decode('latin-1'))
		return True
	
	def call(self, funct, *args, **kwargs):
		try:
			funct(*args, **kwargs)
			return True
		except TypeError as error:
			print(error)
			return False
			
	def quit(self):
		if self.modified:
			self.state = "modified"
		else:
			self.state = "complete"
			
	def prompt(self,string=">"):
		try:
			cmdList = str(input(string)).split()
		except KeyboardInterrupt:
			return None
		if len(cmdList) < 1:
			return []
		else:
			#parse quotes
			newcmdList = []
			quote = ''
			for cmd in cmdList:
				if cmd.startswith('"') and quote == '':
					if cmd.endswith('"') and len(cmd) > 1 and not cmd.replace("\\\\","").endswith('\\\"'):
						newcmdList.append(cmd[1:-1])
					else:
						quote = '"'
						newcmdList.append(cmd[1:])
				elif cmd.startswith("'") and quote == '':
					if cmd.endswith("'") and len(cmd) > 1 and not cmd.replace("\\\\","").endswith("\\\'"):
						newcmdList.append(cmd[1:-1])
					else:
						quote = "'"
						newcmdList.append(cmd[1:])
				elif cmd.endswith('"') and (not cmd.replace("\\\\","").endswith('\\\"')) and quote == '"':
					newcmdList[-1] += " " + cmd[:-1]
					quote = ''
				elif cmd.endswith("'") and (not cmd.replace("\\\\","").endswith("\\\'")) and quote == "'":
					newcmdList[-1] += " " + cmd[:-1]
					quote = ''
				elif quote != '':
					newcmdList[-1] += " " + cmd
				else:
					newcmdList.append(cmd)
			if quote != '':
				raise Exception("No closing quote found for: " + quote)
			return newcmdList
		
		
#************************************************************************************
#	State Handlers
#************************************************************************************

	def runListen(self):
		cmdList = self.prompt()
		if cmdList is None:
			self.quit()
			return
		elif len(cmdList) == 0:
			return
		cmd = cmdList[0]
		args = tuple(cmdList[1:])
		if cmd in ["quit","exit","stop"]:
			self.quit()
		elif cmd in ["load","read"]:
			self.call(self.readFile,*args)
		elif cmd in ["write","save"]:
			self.call(self.writeFile,*args)
		elif cmd in ["set"]:
			self.call(self.setPass,*args)
		elif cmd in ["get","show"]:
			self.call(self.getPass,*args)
		elif cmd in ["remove","delete"]:
			self.call(self.removePass,*args)
		elif cmd in ["encrypt","enc","encode"]:
			self.call(self.encryptStr,*args)
		elif cmd in ["decrypt","dec","decode"]:
			self.call(self.decryptBin,*args)
		elif cmd in ["dump","passwords"]:
			self.showPasswords()
		elif cmd in ["labels","options","keys"]:
			self.showLabels()
		elif cmd in ["password","setpass","pass"]:
			self.call(self.setFilePass,*args)
		elif cmd in ["file","setfile","filename"]:
			self.call(self.setFile,*args)
		elif cmd in ["help","?"]:
			print(self.getHelpStr())
		else:
			print("unrecognized command")
	
	def runModified(self):
		try:
			if self.lastOpened is None or self.lastPass is None:
				cmd = str(input("All unsaved changes will be lost. Quit? y/n: ")).lower()
				if cmd in ["yes","y"]:
					self.state = "complete"
				else:
					self.state = "listen"
			else:
				cmd = str(input("Save changes to " + self.lastOpened + " before exiting? y/n/cancel: ")).lower()
				if cmd in ["yes","y"]:
					if self.writeFile(self.lastOpened, self.lastPass):
						self.state = "complete"
					else:
						self.state = "listen"
				elif cmd in ["no","n"]:
					self.state = "complete"
				else:
					self.state = "listen"
		except KeyboardInterrupt:
			self.state = "complete"

#************************************************************************************
#	main method
#************************************************************************************
	def run(self):
		print("type \"quit\" to exit.")
		while self.state != "complete" and self.state != "error":
			stateHandleStr = "run" + str(self.state).capitalize()
			if not hasattr(self,stateHandleStr) or not callable(getattr(self, stateHandleStr)):
				raise Exception("Program error: state has no handler: " + stateHandleStr)
			getattr(self, stateHandleStr)()


#************************************************************************************
#	End encryptUI
#************************************************************************************

def helpEntry(command,description):
	return command + " " * (HELPSPACING - len(command)) + description + NL

def main():
	enc = encryptUI()
	enc.encryptor = SymmetricEncryptor("xor","rand","xor")
	enc.run()

if __name__ == "__main__":
	main()

