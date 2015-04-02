#Data structures for the VHDL parser

import random

class dotRenderer:
	
	def __init__(self):
		self.built = True
		
	def generatePortMapDotCode(self, componentDict, portMaps):
		code = []
		
		for pm in portMaps:
			# Get the input and output signals
			inSignals = componentDict[pm.componentName].inSignals
			outSignals = componentDict[pm.componentName].outSignals
			
			code.append(pm.identifier + " [shape=record,label=\"{" + pm.identifier+"|{")
			# Draw the input signals
			if len(inSignals) == 0:
				code.append("{}")
			elif len(inSignals) == 1:
				code.append("{<"+inSignals[0].identifier+"> " + inSignals[0].identifier + "}")
			elif len(inSignals) == 2:
				lastIndex = len(inSignals)-1
				# Write the first signal
				code.append("{<"+inSignals[0].identifier+"> " + inSignals[0].identifier + " | ")
				# Write the last signal
				code.append("<"+inSignals[lastIndex].identifier+"> " + inSignals[lastIndex].identifier + "}")
			elif len(inSignals) > 2:
				lastIndex = len(inSignals)-1
				# Write the first signal
				code.append("{<"+inSignals[0].identifier+"> " + inSignals[0].identifier + " | ")
				# Write the middle signal(s) if any
				for i in range(0, lastIndex-1):
					code.append("<"+inSignals[i+1].identifier+"> " + inSignals[i+1].identifier + " | ")
				# Write the last signal
				code.append("<"+inSignals[lastIndex].identifier+"> " + inSignals[lastIndex].identifier + "}")
				
			# Draw the component name
			code.append(" | " + pm.componentName + " | ")
			
			# Draw the output signals
			if len(outSignals) == 0:
				code.append("{}")
			elif len(outSignals) == 1:
				code.append("{<"+outSignals[0].identifier+"> " + outSignals[0].identifier + "}")
			elif len(outSignals) == 2:
				lastIndex = len(outSignals)-1
				# Write the first signal
				code.append("{<"+outSignals[0].identifier+"> " + outSignals[0].identifier + " | ")
				# Write the last signal
				code.append("<"+outSignals[lastIndex].identifier+"> " + outSignals[lastIndex].identifier + "}")
			elif len(outSignals) > 2:
				lastIndex = len(outSignals)-1
				# Write the first signal
				code.append("{<"+outSignals[0].identifier+"> " + outSignals[0].identifier + " | ")
				# Write the middle signal(s) if any
				for i in range(0, lastIndex):
					code.append("<"+outSignals[i+1].identifier+"> " + outSignals[i+1].identifier + " | ")
				# Write the last signal
				code.append("<"+outSignals[lastIndex].identifier+"> " + outSignals[lastIndex].identifier + "}")
			
			# End the port map
			code.append("}}\" ];\n")
			
		codeStr = ''
		for i in code:
			codeStr = codeStr + i
			
		return codeStr
		
		
	def generateDotCode(self, rootEntity, componentTemplates, signalDefinitions, signalAssignments, portMaps, outputName):
		# Build data structures necessary for linking
		
		# Build a dictionary containg each signal, and its context
		globalSignals = dict()
		globalSignals[rootEntity.identifier] = []
		globalSignals['signals'] = []
		# Root entity signals
		for inSig in rootEntity.inSignals:
			globalSignals[rootEntity.identifier].append(inSig.identifier)
		for outSig in rootEntity.outSignals:
			globalSignals[rootEntity.identifier].append(outSig.identifier)
		# Global signals
		for sig in signalDefinitions:
			globalSignals['signals'].append(sig.identifier)
		
		# Build a dictionary of components
		components = dict()
		for component in componentTemplates:
			components[component.identifier] = component
		
		# Open the filestream
		file = open(outputName,'w')
		# Write the header
		file.write("//Generated with VHDL-Dot\n\n")
		
		# Write the root graph
		file.write("digraph vhdlGraph {\n\n")
		
		file.write("nodesep=1;\n")
		file.write("ranksep=4;\n")
		
		file.write("//Root Entity\n")
		
		# Write the rootEntity input signals into a record
		rootInSignals = rootEntity.inSignals
		if len(rootInSignals) == 0:
			file.write(rootEntity.identifier + "Inputs" + " [ shape=record, label=\"" + rootEntity.identifier + " Inputs" + "\"];")
		elif len(rootInSignals) == 1:
			file.write(rootEntity.identifier + "Inputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Inputs |" + " <" + rootInSignals[0].identifier + "> " + rootInSignals[0].identifier +"}\" ];\n")
		elif len(rootInSignals) == 2:
			lastIndex = len(rootInSignals)-1
			# Write the first input signal
			file.write(rootEntity.identifier + "Inputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Inputs |" + " <" + rootInSignals[0].identifier + "> " + rootInSignals[0].identifier + " | ")
			# Write the final input signal
			file.write(" <" + rootInSignals[lastIndex].identifier + "> " + rootInSignals[lastIndex].identifier + "}\" ];\n")
		elif len(rootInSignals) > 2:
			lastIndex = len(rootInSignals)-1
			# Write the first input signal
			file.write(rootEntity.identifier + "Inputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Inputs |" + " <" + rootInSignals[0].identifier + "> " + rootInSignals[0].identifier + " | ")
			# Write the middle input signals, if any
			for i in range(0,(lastIndex-1)):
				file.write(" <" + rootInSignals[i+1].identifier + "> " + rootInSignals[i+1].identifier + " | ")
			# Write the final input signal
			file.write(" <" + rootInSignals[lastIndex].identifier + "> " + rootInSignals[lastIndex].identifier + "}\" ];\n")
		
		# Write the subgraph definition
		file.write("subgraph cluster0 {\n")
		file.write("label=\""+rootEntity.identifier+"\"\n")
		
		# Create all of the signals
		for s in signalDefinitions:
			file.write(s.identifier + "[shape=octagon,label=\""+s.identifier+"\" ];\n")
		
		for s in rootEntity.inSignals:
			file.write(s.identifier + "[shape=rectangle, label=\""+s.identifier+"\" ];\n")
			
		for s in rootEntity.outSignals:
			file.write(s.identifier + "[shape=rectangle, label=\""+s.identifier+"\" ];\n")
		
		# Write the global signals to a single line horizontal record
		#if len(signalDefinitions) == 0:
		#	file.write("signals" + " [ shape=record, label=\"{Signals}\" ];")
		#elif len(signalDefinitions) == 1:
		#	file.write("signals" + " [ shape=record, label=\"{Signals | { <" + signalDefinitions[0].identifier + "> " + signalDefinitions[0].identifier + " }}\" ];\n")
		#elif len(signalDefinitions) > 1:
		#	lastIndex = len(signalDefinitions)-1
		#	# Write the first signal definition
		#	file.write("signals" + " [ shape=record, label=\"{Signals | { <" + signalDefinitions[0].identifier + "> " + signalDefinitions[0].identifier + " | ")
		#	# Write the middle signal definition(s)
		#	for i in range(1,lastIndex):
		#		file.write("<" + signalDefinitions[i].identifier + "> " + signalDefinitions[i].identifier + " | ")
		#	# Write the last signal definition
		#	file.write("<" + signalDefinitions[lastIndex].identifier + "> " + signalDefinitions[lastIndex].identifier + " }}\" ];\n")
		
		colors = [ 'red', 'green', 'blue', 'purple', 'orange', 'black', 'darkgray', 'darkorange', 'firebrick', 'darkolivegreen' ]
		
		# Write all of the port maps
		file.write(self.generatePortMapDotCode(components, portMaps))
		# Write all of the signal assignments defined by port maps
		for pm in portMaps:
			for sig in pm.signalAssignments:
				success = False
				temp = sig.right
				temp = temp.replace("\"","\\\"")
				for key in globalSignals.keys():
					if globalSignals[key].count(sig.right) >= 1:
						success = True
						file.write("\""+pm.identifier+"\":"+sig.left+" -> " +"\""+temp+"\" [dir="+sig.direction+",color=\""+random.choice(colors)+"\"]\n")
						#file.write("\""+pm.identifier+"\":"+sig.left+" -> " + "\""+key+"\":\""+sig.right+"\" [dir="+sig.direction+"]\n")
						break
				if not success:
					#file.write("\""+pm.identifier+"\":"+sig.left+" -> " + "\""+sig.right+"\":n [dir="+sig.direction+"]\n")
					file.write("\""+pm.identifier+"\":"+sig.left+" -> " +"\""+temp+"\" [dir="+sig.direction+",color=\""+random.choice(colors)+"\"]\n")

				#if globalSignals['signals'].count(sig.right) >=1:
				#	file.write("\""+pm.identifier+"\":"+sig.left+" -> " + "\"signals\":\""+sig.right + "\" [dir="+sig.direction+"]\n")
		
		# Write all of the signal assignments
		for sig in signalAssignments:
			temp = sig.right
			temp = temp.replace("\"","\\\"")
			file.write(sig.left+" -> " +"\""+temp+"\" [dir="+sig.direction+"]\n")

		# Close the subgraph
		file.write("}\n")
		
		# Write the rootEntity output signals into a record
		rootOutSignals = rootEntity.outSignals
		if len(rootOutSignals) == 0:
			file.write(rootEntity.identifier + "Outputs" + " [ shape=record, label=\"" + rootEntity.identifier + " Outputs" + "\"];")
		elif len(rootOutSignals) == 1:
			file.write(rootEntity.identifier + "Outputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Outputs |" + " <" + rootOutSignals[0].identifier + "> " + rootOutSignals[0].identifier +"}\" ];\n")
		elif len(rootOutSignals) == 2:
			lastIndex = len(rootOutSignals)-1
			# Write the first input signal
			file.write(rootEntity.identifier + "Outputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Outputs |" + " <" + rootOutSignals[0].identifier + "> " + rootOutSignals[0].identifier + " | ")
			# Write the final input signal
			file.write(" <" + rootOutSignals[lastIndex].identifier + "> " + rootOutSignals[lastIndex].identifier + "}\" ];\n")
		elif len(rootOutSignals) > 2:
			lastIndex = len(rootOutSignals)-1
			# Write the first input signal
			file.write(rootEntity.identifier + "Outputs" + " [ shape=record, label=\"{" + rootEntity.identifier + " Outputs |" + " <" + rootOutSignals[0].identifier + "> " + rootOutSignals[0].identifier + " | ")
			# Write the middle input signals, if any
			for i in range(0,(lastIndex-1)):
				file.write(" <" + rootOutSignals[i+1].identifier + "> " + rootOutSignals[i+1].identifier + " | ")
			# Write the final input signal
			file.write(" <" + rootOutSignals[lastIndex].identifier + "> " + rootOutSignals[lastIndex].identifier + "}\" ];\n")
		
		# Close the root digraph
		file.write("}\n")
		# Write to the file
		file.close()
		
		
class component:
	
	def __init__(self, arg_identifier='', arg_inSignals=[], arg_outSignals=[]):
		self.identifier = arg_identifier
		self.inSignals = arg_inSignals
		self.outSignals = arg_outSignals
		
class signal:

	def __init__(self, arg_identifier='', arg_type='', arg_leftLinks=[], arg_rightLinks=[]):
		self.identifier = arg_identifier
		self.type = arg_type
		self.leftLinks = arg_leftLinks
		self.rightLinsk = arg_rightLinks
		
class signalAssignment:

	def __init__(self, arg_LHS='', arg_RHS='', arg_Dir='forward'):
		self.left = arg_LHS
		self.right = arg_RHS
		self.direction = arg_Dir
		
class portMap:
	
	def __init__(self, arg_identifier='', arg_componentName='', arg_signalAssignments=[]):
		self.identifier = arg_identifier
		self.componentName = arg_componentName
		self.signalAssignments = arg_signalAssignments
		
