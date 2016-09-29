import os
import sys
from configuration import Configuration
'''preCompiler.py: a script which compiles all the modules virusLand.py is dependent on.
Programs needed to be compiled:
TaxFromGBK		(C executable)
TaxXGenomeHits	(C executable)
JPaudaParser	(java .class)
CParser		(C executable)
virusGraphis (.jar executable)
Should be executed before buildIndexes.py; only needs to be ran once when virusLand is installed

Usage: python preCompiler.py
'''
class preCompile:
	def __init__(self):
		self.cwd = os.getcwd()
		self.uncompiled = self.cwd+'/uncompiled'
		self.compileStuff()
	def compileStuff(self):
		cmds=[]
		cmds.append('g++ %s/statsGenerator.cpp -o %s/StatsGenerator'%(self.uncompiled, self.cwd))
		cmds.append('g++ %s/taxFromGBK.cpp -o %s/TaxIndexer'%(self.uncompiled, self.cwd))
		cmds.append('g++ %s/genomeHits.cpp -o %s/KronaPrep'%(self.uncompiled, self.cwd))
		cmds.append('javac -d %s %s/JPauda.java'%(self.cwd, self.uncompiled))
		for i in cmds:
			print(i)
			os.system(i)
	
p = preCompile()
