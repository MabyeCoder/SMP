  #########################
 # S+.<M>\=P Version 1.1 #
#########################

from sys import *
import sys
import time
import platform

#DataBase
Tokens = []
Symbols = {}

def open_file(File_Name):
	if sys.version_info[0] < 3:
		print("[Python Error]: Must be using Python 3")
		exit()
	else:
		if File_Name.endswith(".smp"):
			print("[Python " + platform.python_version() + "]: " + File_Name + " Successfully Loaded!")
			Data = open(File_Name, "r").read()
			Data += "<EOF>"
			return Data
		else:
			print("[File Error]: Can't Open " + File_Name)
			exit()

def Lex(File_Contents):
	tok = ""
	State = 0
	VariableStarted = 0
	String = ""
	Variable = ""
	Expression = ""
	IsExpression = 0
	n = ""
	File_Contents = list(File_Contents)
	for char in File_Contents:
		tok += char
		if tok == " ":
			if State == 0:
				tok = ""
			else:
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			if Expression != "" and IsExpression == 1:
				Tokens.append("Expression:" + Expression)
				Expression = ""
			elif Expression != "" and IsExpression == 0:
				Tokens.append("Number:" + Expression)
				Expression = ""
			elif Variable != "":
				Tokens.append("Variable:" + Variable)
				Variable = ""
				VariableStarted = 0
			tok = ""
		elif tok == "=" and State == 0:
			if Variable != "":
				Tokens.append("Variable:" + Variable)
				Variable = ""
				VariableStarted = 0
			Tokens.append("Equals")
			tok = ""
		elif tok == "!" and State == 0:
			VariableStarted = 1
			Variable += tok
			tok = ""
		elif VariableStarted == 1:
			if tok == "<" or tok == ">":
				if Variable != "":
					Tokens.append("Variable:" + Variable)
					Variable = ""
					VariableStarted = 0
			Variable += tok
			tok = ""
		elif tok == "Say" or tok == "SAY" or tok == "say":
			Tokens.append("Say")
			tok = ""
		elif tok == "Info" or tok == "INFO" or tok == "info":
			Tokens.append("Info")
			tok = ""
		elif tok == "About" or tok == "ABOUT" or tok == "about":
			Tokens.append("About")
			tok = ""
		elif tok == "Do" or tok == "DO" or tok == "do":
			Tokens.append("Do")
			tok = ""
		elif tok == "Input" or tok == "INPUT" or tok == "input":
			Tokens.append("Input")
			tok = ""
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			Expression += tok
			tok = ""
		elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "%" or tok == "(" or tok == ")" and State == 0:
			IsExpression = 1
			Expression += tok
			tok = ""
		elif tok == "\"" or tok == " \"":
			if State == 0:
				State = 1
			elif State == 1:
				Tokens.append("String:" + String + "\"")
				String = ""
				State = 0
				tok = ""
		elif State == 1:
			String += tok
			tok = ""
	print(Tokens)
	#return ''    
	return Tokens

def evalExpression(Expression):
	return eval(Expression)


def getINPUT(String, VariableName):
	i = input(String[1:-1] + " ")
	Symbols[VariableName] = "String:\"" + i + "\""

def getVARIABLE(VariableName):
	VariableName = VariableName[9:]
	if VariableName in Symbols:
		return Symbols[VariableName]
	else:
		print("[Variable Error]: Undefind Variable")
		exit()


def doPRINT(toPRINT):
	if(toPRINT[0:6] == "String"):
		toPRINT = toPRINT[8:]
		toPRINT = toPRINT[:-1]
	elif(toPRINT[0:6] == "Number"):
		toPRINT = toPRINT[7:]
	elif(toPRINT[0:10] == "Expression"):
		toPRINT = evalExpression(toPRINT[11:])
	print(toPRINT)


def doASSIGN(VariableName, VariableValue):
	Symbols[VariableName[9:]] = VariableValue


def doEVENT(MString, FString, CString, VariableName):
	MString = MString[1:-1]
	FString = FString[1:-1]
	CString = CString[1:-1]
	if VariableName in Symbols:
		if Symbols[VariableName] == "String:\"" + CString + "\"":
			print(MString)
		else:
			print(FString)
			exit()
	else:
		print("[Variable Error]: Undefind Variable")
		exit()

def checkINFO(NString, VString, VariableName):
	NString = NString[1:-1]
	VString = VString[1:-1]
	if VariableName in Symbols:
		print(NString + " " + VariableName)
		print(VString + " " + Symbols[VariableName][7:][1:-1])
	else:
		print("[Variable Error]: Undefind Variable")
		exit()


def Parse(Toks):
	i = 0
	while(i < len(Toks)):
		if Toks[i] + " " + Toks[i+1][0:6] == "Say String" or Toks[i] + " " + Toks[i+1][0:6] == "Say Number" or Toks[i] + " " + Toks[i+1][0:10] == "Say Expression" or Toks[i] + " " + Toks[i+1][0:8] == "Say Variable":
			if Toks[i+1][0:6] == "String" or Toks[i+1][0:6] == "Number":
				doPRINT(Toks[i+1])
				i+=2
			elif Toks[i+1][0:8] == "Variable":
				doPRINT(getVARIABLE(Toks[i+1]))
				i+=2
			elif Toks[i+1][0:10] == "Expression":
				doPRINT(Toks[i+1])
				i+=2
		elif Toks[i][0:8] + " " + Toks[i+1] + " " + Toks[i+2][0:6] == "Variable Equals String" or Toks[i][0:8] + " " + Toks[i+1] + " " + Toks[i+2][0:6] == "Variable Equals Number" or Toks[i][0:8] + " " + Toks[i+1] + " " + Toks[i+2][0:10] == "Variable Equals Expression" or Toks[i][0:8] + " " + Toks[i+1] + " " + Toks[i+2][0:8] == "Variable Equals Variable":
			if Toks[i+2][0:6] == "String":
				doASSIGN(Toks[i],Toks[i+2])
			elif Toks[i+2][0:6] == "Number":
				doASSIGN(Toks[i],Toks[i+2])
			elif Toks[i+2][0:10] == "Expression":
				doASSIGN(Toks[i],"Number:" + str(evalExpression(Toks[i+2][11:])))
			elif Toks[i+2][0:8] == "Variable":
				doASSIGN(Toks[i],getVARIABLE(Toks[i+2]))
			i+=3
		elif Toks[i] + " " + Toks[i+1][0:6] + " " + Toks[i+2][0:8] == "Input String Variable":
			getINPUT(Toks[i+1][7:],Toks[i+2][9:])
			i+=3
		elif Toks[i] + " " + Toks[i+1][0:6] + " " + Toks[i+2][0:6] + " " + Toks[i+3][0:6] + " " + Toks[i+4][0:8] == "Do String String String Variable" or Toks[i] + " " + Toks[i+1] + " " + Toks[i+2][0:6] + " " + Toks[i+3][0:6] + " " + Toks[i+4][0:8] == "Info About String String Variable":
			if Toks[i] == "Do":
				doEVENT(Toks[i+1][7:],Toks[i+2][7:],Toks[i+3][7:],Toks[i+4][9:])
			elif Toks[i] == "Info":
				checkINFO(Toks[i+2][7:],Toks[i+3][7:],Toks[i+4][9:])
			i+=5
	#print(Symbols)



def Run():
	Data = open_file(argv[1])
	Toks = Lex(Data)
	Parse(Toks)

Run()