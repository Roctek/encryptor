# Encryptor
This is a Python library that includes the following:
1. encrypt.py:              command line password manager
2. Binary.py:               binary manipulation and conversion datatype
3. SymmetricEncryptor.py:   home-brew encryptor class 

## Notices/Disclaimers/Warnings:
- This is a work in progress, so there are likely some bugs left in the code. Please let me know about these and any suggestions you may have so that I can improve the code.
- I have had little to no formal training in encryption. Please DO NOT assume the algorithms I have supplied in SymmetricEncryptor and use in encrypt.py are proven to be reversable and hard to crack
- If you add stages to SymmetricEncryptor, please note that if done incorrectly, you may inadvertently expose the password or other information that may be used to break all stages of encryption (Although I do encourage you to play around with your own encryption stages).

## Encrypt.py Commands and aliases: 

### `help`
- display commands
- aliases: ["help","?"]
            
### `quit` 
- stop running the script
- aliases: ["quit","exit","stop"]
            
### `read <filename>`       
- read password dictionary from a file previously encrypted using the same scheme
- aliases: ["load","read"]

### `write <filename>`
- write the current password dictionary to the specified file using the current encryption scheme
- aliases: ["write","save"]

### `set <label> <password>`
- store the given password in the current password dictionary with the given label

### `get <label>`
- read the currently stored password with the given label
- aliases: ["get","show"]

### `remove <label>`
- remove the currently stored password with the given label
- aliases: ["remove","delete"]
### `labels`      
- print all labels in the dictionary to the screen
- aliases: ["labels","options","keys"]

### `dump`
- print all labels with corresponding passwords to the screen
- aliases: ["dump","passwords"]

### `pass <new password>`
- set the password so that you do not have to specify it for each command
- note: this field gets updated automatically whenever a different password is used
- aliases: ["password","setpass","pass"]

### `file <filename>`
- set the filename so that you do not have to specify it for each command
- note: this field gets updated automatically whenever a different filename is used
- aliases: ["file","setfile","filename"]

### `encrypt <string to encrypt> <password>`     
- print the result of encrypting the specified string with the given password in Hexadecimal representation
- note: the length is also provided as preceeding zero bits may or may not present
- aliases: ["encrypt","enc","encode"]

### `decrypt <hex string> <password> <length(optional)>`
- print the result of decrypting the specified hexadecimal or binary string of specified length with the given password in 'latin-1' encoding
- note: if no length argument is provided, all preceeding zeros are considered significant
- note: Hex string begin with '0x' and binary begin with '0b'. No type designator is considered decimal
- aliases: ["decrypt","dec","decode"]
