# VHDL Graph creator
# Parser

# Our componentLibrary.py file, containing classes declaration
import componentLibrary as vhdl

#####################################################################################
## LEXER
#####################################################################################
#from ply import lex

# Reserved word defenitions { value : key, ... }
reserved = {
	#'architecture' : 'ARCHITECTURE',
	'component'	: 'COMPONENT',
	'entity'	: 'ENTITY',
	#'ENTITY'	: 'ENTITY',
	'end'		: 'END',
	'generate'  : 'GENERATE',
	'is'		: 'IS',
	'of'		: 'OF',
	'downto'	: 'DOWNTO',
	'to'		: 'TO',
	'begin'		: 'BEGIN',
	'for'		: 'FOR',
	'port'		: 'PORT',
	'map'		: 'MAP',
	'in'		: 'IN',
	'out'		: 'OUT',
	'signal'	: 'SIGNAL',
	# Logical operators
	'and'		: 'AND',
	'or'		: 'OR',
	'not'		: 'NOT',
	'nand'		: 'NAND',
	'nor'		: 'NOR',
	'xor'		: 'XOR',
	'xnor'		: 'XNOR',

	}
	
signalTypes = [
	'std_ulogic',
	'std_ulogic_vector',
        'std_logic',
	'std_logic_vector',
	'STD_LOGIC',
	'STD_LOGIC_VECTOR',
	]

# Token defenitions
tokens = [
	'IDENTIFIER',
	'SIGTYPE',
	'NUMBER',
	'SCOLON',
	'COLON',
	'LPAREN',
	'RPAREN',
	'COMMA',
	'CONNECTION_OUT',
	'CONNECTION_IN',
	'LITERAL',
	] + list(reserved.values())

# debug
print ("tokens: " + str(tokens) + "\n")

	
t_ignore = '\t ' #ignore tabs and spaces
t_ignore_COMMENT = '--(.*)' # ignore VHDL comments
t_ignore_ASSIGNMENT = ':=(.*)(\'|\")(.*)(\'|\")' # ignore literal assignments

#Basic misc tokens
t_NUMBER	= r'[0-9]+'
t_SCOLON 	= r';'
t_COLON 	= r':'
t_LPAREN 	= r'\('
t_RPAREN 	= r'\)'
t_COMMA		= r','
#t_LITERAL	= r'((X(\'|\")([a-fA-F0-9]+)(\'|\"))|((\'|\")([0-1]+)((\'|\"))))'

t_CONNECTION_OUT	= r'=>'
t_CONNECTION_IN		= r'<='

def t_LITERAL(t):
	r'((X(\'|\")([a-fA-F0-9]+)(\'|\"))|((\'|\")([0-1]+)((\'|\"))))'
	return t
	
def t_newLine(t):
	r'\n'
	#Set the line number of each token
	t.lexer.lineno += len(t.value)

# Match an identifier, or a reserved word
def t_IDENTIFIER(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'


	# print("identifier: " + str(t.value))
        
	for sigType in signalTypes:
		if t.value == sigType:
			t.type = 'SIGTYPE'
			return t


	#if t.value == ENTITY
	#	t.type = 'ENTITY'
        #	return t

        #debug
	if t.value in reserved:
		t.type = reserved[ t.value ]
		#print ("reserved matched. Value: "+ str(t.value) + "Type: " + str(t.type))

		return t
	
	t.type = reserved.get(t.value, 'IDENTIFIER')
	return t

# Skip over any undefined tokens, we don't need them
def t_error(t):
	t.lexer.skip(1)
	
#Build the lexer
import ply.lex as lex

lex.lex()

#####################################################################################
## PARSER
#####################################################################################

# file : statementList
def p_file(p):
	'file : entity statementList'
	items = [p[1]]
	for item in p[2]:
		items.append(item)
	# Push items up the tree
	p[0] = items
	
# statementList : statement statementList
#				| statement
def p_statementList(p):
	'''statementList : statement statementList
					 | statement'''
	statements = [p[1]]
	# Add the other statements to the list, if any
	if len(p) == 3:
		for statement in p[2]:
			statements.append(statement)
	# Push the statements up the tree
	p[0] = statements
	
# statement : component
#			| signal
#			| signalDeclaration
#			| signalAssign ;
#			| portmap
#			| error
def p_statement(p):
	'''statement : component
				 | signal
				 | signalDeclaration
				 | signalAssign SCOLON
				 | portMap'''
	p[0] = p[1]
	
# statementerror
def p_statementerror(p):
	'statement : error'
	pass
		
# component : COMPONENT IDENTIFIER portDef END COMPONENT ;
def p_component(p):
	'component : COMPONENT IDENTIFIER portDef END COMPONENT SCOLON'
	#locals
	ident = p[2]
	inSignals = []
	outSignals = []
	#Organize the signals
	for signal in p[3]:
		if signal.type == 'in':
			inSignals.append(signal)
		elif signal.type == 'out':
			outSignals.append(signal)
                # TBD: add support for inout signals
		else:
			raise Exception("Invalid signal type.")
			
	#Create the component
	p[0] = vhdl.component(ident, inSignals, outSignals)

# TBD: add here support for component instantiated as work.<comp_name>,
#      so that we can add it p[0] = vhdl.component(ident, inSignals, outSignals)
#      Fake the directions of IO when work.<comp_name>
        
# entity : ENTITY IDENTIFIER IS portDef END IDENTIFIER ;
def p_entity(p):
	'''entity : ENTITY IDENTIFIER IS portDef END IDENTIFIER SCOLON
			  | ENTITY IDENTIFIER IS END IDENTIFIER SCOLON'''		
	ident = p[2]
	inSignals = []
	outSignals = []

	# Entity does not contain a portDef
	if len(p) == 7:
		p[0] = vhdl.component(ident)
		return
		
	# Organize the signals
	# NOTE: inout ports not supported at the moment
	for signal in p[4]:
		if signal.type == 'in':
			inSignals.append(signal)
		elif signal.type == 'out':
			outSignals.append(signal)
		else:
			raise Exception("Invalid signal type.")
			
	#Create the entity
	#Note: an entity is identical to a component, however, its signals has global context
	p[0] = vhdl.component(ident, inSignals, outSignals)
	
# portDef : PORT ( signalDeclarationList );
def p_portDef(p):
	'portDef : PORT LPAREN signalDeclarationList RPAREN SCOLON'
	p[0] = p[3]

# TBD: QUESTION: who uses this signalassign?
#      Try to stimulate the exception to understand...
# NOTE: connected to the "connection" wrong rule...
#
# signalAssign : signal connection lE
def p_signalAssign2(p):
	'signalAssign : signal connection lE'
	
	if p[2] == 'out':
		#p[0] = vhdl.signalAssignment(p[1], ("\""+p[3]+"\""), 'forward')
		p[0] = vhdl.signalAssignment(p[1], p[3], 'forward')
	elif p[2] == 'in':
		#p[0] = vhdl.signalAssignment(p[1], ("\""+p[3]+"\""), 'back')
		p[0] = vhdl.signalAssignment(p[1], p[3], 'back')
	else:
		raise Exception("Expected connection in or out. Got: " + p[2])

# portMap : IDENTIFIER : IDENTIFIER port map ( signalAssignList );		
def p_portMap(p):
	'portMap : IDENTIFIER COLON IDENTIFIER PORT MAP LPAREN signalAssignList RPAREN SCOLON'
	p[0] = vhdl.portMap(p[1],p[3],p[7])

# signal : IDENTIFIER LPAREN range RPAREN
#		 | IDENTIFIER
def p_signal(p):
	'''signal : IDENTIFIER LPAREN range RPAREN
			  | IDENTIFIER'''
	p[0] = p[1]
	if len(p) > 2:
		p[0] = p[0] + '[' + p[3] + ']'
	
# signalAssignList : signalAssign COMMA signalAssignList
# 				   | signalAssign
def p_signalAssignList(p):
	'''signalAssignList : signalAssign COMMA signalAssignList
						| signalAssign'''
	signalAssignments = [p[1]]
	# Add the other signal assignments, if any
	if len(p) == 4:
		for sigAssign in p[3]:
			signalAssignments.append(sigAssign)
	# Push the signals up the tree
	p[0] = signalAssignments

# signalDeclarationList : identifierList COLON signalDirection signalType SCOLON signalDeclarationList
#							 | identifierList COLON signalDirection signalType
def p_signalDeclarationList(p):
	'''signalDeclarationList : identifierList COLON signalDirection signalType SCOLON signalDeclarationList
							 | identifierList COLON signalDirection signalType'''
	signals = []
	for ident in p[1]:
		signals.append(vhdl.signal(ident,p[3]))
	# If there are any, combine with the other signals
	if len(p) == 7:
		for sig in p[6]:
			signals.append(sig)
	
	# Push the signals up the tree
	p[0] = signals
	
# signalDirection : in
#				  | out
def p_signalDirection(p):
	'''signalDirection : IN
						| OUT'''
	p[0] = p[1]
		
# identifierList : IDENTIFIER , identifierList
#				 | IDENTIFIER
def p_identifierList(p):
	'''identifierList : IDENTIFIER COMMA identifierList
					  | IDENTIFIER'''
	
	identifiers = [p[1]]
	if len(p) == 4:
		# Add the other identifiers
		for ident in p[3]:
			identifiers.append(ident)
	# Push the identifiers up the tree
	p[0] = identifiers

# signalDeclaration : SIGNAL identifierList : signalType ;
#		 			| SIGNAL identifierList : signalDirection signalType ;
def p_signalDeclaration(p):
	'''signalDeclaration : SIGNAL identifierList COLON signalType SCOLON
						 | SIGNAL identifierList COLON signalDirection signalType SCOLON
						 '''
	signals = []
	# Create all of the signals
	for ident in p[2]:
		signals.append(vhdl.signal(ident, 'signal'))
	# Push the signals up the tree
	p[0] = signals
	
	
# connection : =>
#			 | <=
# TDB: DANGER: THIS RULE IS COMPLETELY WRONG!
#      The => or <= differs depending on where they are used.
#      They do not necessarily mean INPUT or OUTPUT connections!
#      MUST be improved with correct grammar!
def p_connection(p):
	'''connection : CONNECTION_OUT
				  | CONNECTION_IN'''
	if p[1] == '<=':
		p[0] = 'in'
	elif p[1] == '=>':
		p[0] = 'out'
	else:
		raise Exception("Expected <= or =>  received " + p[1])
	
# signalType : SIGTYPE
#			 : SIGTYPE range
def p_signalType(p):
	'''signalType : SIGTYPE
				  | SIGTYPE LPAREN range RPAREN'''
	p[0] = p[1]
	
# lE : NOT lE
#	 | lE lOp LE
#	 | ( lE )
#	 | signal
def p_lE(p):
	'''lE : NOT lE
		| lE lOp lE
		| LPAREN lE RPAREN
		| signal
		| LITERAL'''
	# signal
	if len(p) == 2:
		p[0] = p[1]
	# NOT lE
	elif len(p) == 3:
		p[0] = "not " + p[2]
	# lE lOp lE or LPAREN lE RPAREN
	elif len(p) == 4:
		# LPAREN lE RPAREN
		if p[0] == '(':
			p[0] = "( " + p[2] + " )"
		# lE lOp lE
		else:
			p[0] = p[1] + " " + p[2] + " " + p[3]
	else:
		raise Exception("Invalid argument length to rule lE")

# lOp : AND
#			| OR
#			| XOR
#			| NOR
#			| XNOR
#			| NAND        
def p_lOp(p):
	'''lOp : AND
			| OR
			| XOR
			| NOR
			| XNOR
			| NAND'''
	p[0] = p[1]
	
# range : NUMBER DOWNTO NUMBER
#		| NUMBER TO NUMBER
def p_range(p):
	'''range : NUMBER DOWNTO NUMBER
			| NUMBER TO NUMBER
			| NUMBER'''
	p[0] = p[1]
	if len(p) > 3:
		p[0] = p[0] + '-' + p[3]
		
# Error rule, skips all invalid tokens
def p_error(p):
	#Record the line number the error is on
	errLineNo = p.lineno
	tok = yacc.token() # get the next token
	while tok != None:
		if tok.lineno != errLineNo:
			yacc.errok()
			return tok
		else:                        
			tok = yacc.token()
	
# Build the parser
import ply.yacc as yacc
yacc.yacc()
	
#####################################################################################
## Function definitions
#####################################################################################

import sys	

## flatten function
#
def flatten(x):
    if isinstance(x, list):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

## generateDotFile function
#
# TBD: NOTE: the following function seems to be outdated if compared with the one
# defined in componentLibrary. Maybe we can remove the following function.
#
# This deprecated function can and should be moved to another file
def generateDotFile(componentTemplates, signalDefinitions, signalAssignments, portMaps, outputName='temp.dot'):
		
	# Create a dictionary of the defined components
	components = dict()
	for component in componentTemplates:
		components[component.identifier] = component
	
	# Create the output file
	file = open(outputName,'w')
	
	# Write the header
	file.write("digraph " + componentTemplates[0].identifier + " {\n")
	
	# Draw the signals
	file.write("\n//Signals\n")
	for signal in signalDefinitions:
		file.write( "\"" + signal.identifier + "\"" + " [shape=circle,color=black,label=" + signal.identifier + "];\n")
		
	# Draw all of the port maps
	file.write("\n//Port maps\n")
	for pm in portMaps:

		file.write(pm.identifier + " [shape=record,nodesep=20,label=\"")
		file.write("{"+pm.identifier+"|{")
		# Get the list of input signals for the component that the port map is using
		inSignals = components[pm.componentName].inSignals
		
		# Draw the input signals
		if(len(inSignals) > 1):
			file.write("{<"+inSignals[0].identifier+"> " + inSignals[0].identifier + "|")
			for i in range(1, len(inSignals)-1):
				file.write("{<"+inSignals[i].identifier+"> " + inSignals[i].identifier + "}|")
			file.write("<"+inSignals[len(inSignals)-1].identifier+"> " + inSignals[len(inSignals)-1].identifier+"}")
		elif(len(inSignals) == 1):
			file.write("<"+inSignals[0].identifier+"> " + inSignals[0].identifier)
		
		# Draw the component name
		file.write("|"+pm.componentName+"|")
		
		# Get the list of output signals for the component that the port map is using
		outSignals = components[pm.componentName].outSignals
		
		# Draw the output signals
		if(len(outSignals) > 1):
			file.write("{<"+outSignals[0].identifier+"> " + outSignals[0].identifier + "|")

			for i in range(1, len(outSignals)-1):
				file.write("{<"+outSignals[i].identifier+"> " + outSignals[i].identifier + "}|")
			file.write("<"+outSignals[len(outSignals)-1].identifier+"> " + outSignals[len(outSignals)-1].identifier+"}")
		elif(len(outSignals) == 1):
			file.write("<"+outSignals[0].identifier+"> " + outSignals[0].identifier)
		
		# End the current port map
		file.write("}}\"];\n")
	
	# Draw the signal assignemnts defined by the port map
	file.write("\n//Port map transitions\n")
	for pm in portMaps:
		for sig in pm.signalAssignments:
			file.write("\""+pm.identifier+"\":"+sig.left+" -> "+sig.right+" [dir="+sig.direction+"]"+"\n")
	
	# Link all of the signals together
	file.write("\n//Signal assignments\n")
	for sigAssign in signalAssignments:
		file.write( "\"" + sigAssign.left + "\"" + " -> " + sigAssign.right + " [dir="+sigAssign.direction+"]\n")
		
	file.write("}\n")

#####################################################################################
## Main starts here
#####################################################################################

## Steps: 

## 1] Choose input source (prompt or batch from command line argument)

## 2] Parse each file provided as input source, and store in parsedData

## 3] Loop through parsedData and create the data structure which will be used to
##    generate .dot file (very IMPORTANT!)

## 4] call generateDotCode or generateDotFile to create .dot files from data strucure
##    previously initialized

#####################################################################################

parsedData = []
fileNames = []

## Step 1

if len(sys.argv) > 1:
	print ("Reading files specified by command line parameters...")
	for i in range(1, len(sys.argv)):
		fileNames.append(sys.argv[i])
else:
	print ("Enter the name of the file to parse.")
	t = raw_input('>')
	fileNames.append(t)

## Step 2
        
for file in fileNames:
	print ("File: " + str(file))
	fileContents = ''
	print ("\tOpening file...")
	f = open(file, 'r')
	print ("\tReading file...")
	for line in f:
		fileContents = fileContents + line
	print ("\tParsing file...")
        # debug
	print ("fileContents: " + str(fileContents) + "\n")
	result = yacc.parse(fileContents,debug=1)
        # debug
	print ("yacc.parse: " + str(result) + "\n")

	result = flatten(result)
        # debug
	print ("flattened result: " + str(result) + "\n")

        
	if result == [None]:
		print ("Error parsing VHDL file. " + str(file) + "\n")
	else:
		print ("Ok: " + str(file) + "\n")
		parsedData.append([file,result])
		
# parsedData is of the form [ [ fileName, parseResult ], ... ]

	print ("parsedData: " + str(parsedData) + "\n")

       
for results in parsedData:
	fileName = results[0]
	
	outputName = fileName.strip(".vhd") + ".dot"
	logFileName = fileName.strip(".vhd") + ".log"
	r = results[1]

    
	rootEntity = r[0]
	componentTemplates = []
	signalDefinitions = []
	signalAssignments = []
	portMaps = []

        ## Step 3

	# Fill the data structures
	for statement in r:
		# Components
		if isinstance(statement, vhdl.component):
			componentTemplates.append(statement)
		# Signal definitions
		elif isinstance(statement, vhdl.signal):
			signalDefinitions.append(statement)
		# Signal assignments
		elif isinstance(statement, vhdl.signalAssignment):
			signalAssignments.append(statement)
		# Port maps
		elif isinstance(statement, vhdl.portMap):
			portMaps.append(statement)

        ## Step 4
			
	renderer = vhdl.dotRenderer()

        ## NOTE: the following generateDotCode function comes from componentLibrary (most updated) 
	renderer.generateDotCode(rootEntity, componentTemplates, signalDefinitions, signalAssignments, portMaps, outputName)
	
	## NOTE: the following generateDotFile function was defined ealier in this file (older) 
	#generateDotFile(componentTemplates, signalDefinitions, signalAssignments, portMaps, outputName)

#####################################################################################
## logfile generation starts here
#####################################################################################
        
	logFile = open(logFileName, 'w')

	print ("Writing parse data of " + fileName + " to log file " + logFileName + " ...")

	# Write data to logfile
	for statement in r:
		if isinstance(statement, vhdl.component):
			logFile.write("\n")
			logFile.write("Ident: " + statement.identifier + '\n')
			inSignals = statement.inSignals
			logFile.write("Inputs: ")
			for signal in inSignals:
				logFile.write(signal.identifier + " ")
			logFile.write('\n')
			outSignals = statement.outSignals
			logFile.write("Outputs: ")
			for signal in outSignals:
				logFile.write(signal.identifier + " ")
			logFile.write('\n')
		elif isinstance(statement, vhdl.signal):
			logFile.write('\n')
			logFile.write("Ident: " + statement.identifier + '\n')
		elif isinstance(statement, vhdl.signalAssignment):
			logFile.write('\n')
			logFile.write(statement.left + " -> " + statement.right + '\n')
		elif isinstance(statement, vhdl.portMap):
			logFile.write('\n')
			logFile.write("Ident: " + statement.identifier + '\n')
			logFile.write("Component: " + statement.componentName + '\n')
			logFile.write("Assignments: ")
			for sigAssign in statement.signalAssignments:
				logFile.write("[ " + sigAssign.left + " => " + sigAssign.right + " ]")
			logFile.write('\n')
	

