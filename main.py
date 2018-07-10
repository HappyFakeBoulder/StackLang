# IMPORTANT NOTE:
# This program reads code from code.txt.
# Before running, edit code.txt to hold the
# program you want to run.

import pdb
# allows code errors
class CodeError(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
# some helpful little functions
def compressBin(string):
	while string[0] == "0":
		string = string[1:]
	return string
def divideStr(string, sectLen):
	return [string[start:start+sectLen] for start in range(0, len(string), sectLen)]
def divideToChars(string):
	return divideStr(string[len(string) % 8:], 8)
def divToAscii(string):
	retVal = ""
	for x in string:
		if x not in "01":
			raise ValueError("Non-binary input to divToAscii")
	print("Modulo of string is " + str(len(string) % 8))
	for x in divideToChars(string):
		retVal += chr(int(compressBin(x), 2))
	return retVal
# the main interpreter class
class StackLangInterpreter():
	# setting up variables
	def __init__(self):
		self.dataStack = []
	# interpretation function
	def interpret(self, code):
		print(code)
		# checks for correct argument type
		if type(code) != str:
			raise TypeError("Expected str in interpret()")
		# a basic parsing
		self.parsedCode = code.lower().split(";")
		for x in range(0, len(self.parsedCode)):
			self.parsedCode[x] = self.parsedCode[x].strip()
		# interpret!
		for x in self.parsedCode:
			# push instruction
			if x.startswith("push"):
				# checks for number to push
				self.genPurpVar = False
				for y in x:
					if y in "1234567890":
						self.genPurpVar = True
						break
				if self.genPurpVar == False:
					raise CodeError("Line " + str(self.parsedCode.index(x) + 1) + ": No number in push instruction")
				# gets the number
				for z in range(0, len(x[x.find(y):])):
					if x[z + x.find(y)] not in "1234567890":
						break
				print(z)
				self.genPurpVar = x[x.find(y):z + 6]
				print(self.genPurpVar)
				self.dataStack.append(bin(int(self.genPurpVar))[2:])
			# pop instruction
			if x.startswith("pop"):
				try:
					del self.dataStack[len(self.dataStack) - 1]
				except IndexError:
					raise CodeError("Line " + str(self.parsedCode.index(x) + 1) + ": Attempt to pop with an empty stack")
			# concat instruction
			if x.startswith("concat"):
				# check stack size
				if len(self.dataStack) < 2:
					raise CodeError("Line " + str(self.parsedCode.index(x) + 1) + ": Not enough items on stack to concatenate")
				# get concatenation
				self.genPurpVar = self.dataStack[len(self.dataStack) - 2]
				self.genPurpVar += self.dataStack[len(self.dataStack) - 1]
				# pop 2 times
				del self.dataStack[len(self.dataStack) - 1]
				del self.dataStack[len(self.dataStack) - 1]
				# leave result on stack
				self.dataStack.append(self.genPurpVar)
			# copy instruction
			if x.startswith("copy"):
				self.dataStack.append(self.dataStack[len(self.dataStack) - 1])
			# swap instruction
			if x.startswith("swap"):
				self.genPurpVar = self.dataStack[len(self.dataStack) - 1]
				del self.dataStack[len(self.dataStack) - 1]
				self.dataStack.insert(len(self.dataStack) - 1, self.genPurpVar)
			# exec instruction
			if x.startswith("exec"):
				print(self.dataStack)
				print(divToAscii(self.dataStack[len(self.dataStack) - 1]))
				self.interpret(divToAscii(self.dataStack[len(self.dataStack) - 1]))
# programming interface
interpreter = StackLangInterpreter()
codeFile = open("code.txt", "r")
userCode = codeFile.read()
codeFile.close()
interpreter.interpret(userCode)
print(interpreter.dataStack)
