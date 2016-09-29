'''Virusland main controller file'''
#Author: Zach Romer

import os
import sys
import glob
from configuration import Configuration
from velvet import VelvetPackage
from emboss import EmbossPack
from pauda import PaudaPack
from lamb import Lambs
from parsers import JPaudaParser
from parsers import CParser
from kronaGen import Krona_generator
from visualizer import Virus_visualizer

'''
Usage:
python virusLand.py runName seq1 seq2 pathToConfig.vl
virusLand.py = virusLand source file
seq1 = first sequence
seq2 = second sequence
pathToConfig.vl = file path to config.vl file (if located in /src only need to give file name, config.vl)
'''
class VirusLand:
	#Take run name, 2 sequences and config.vl file / location as arguments
	def __init__(self, argv):
		print('running')
		self.config=Configuration()
		self.config.runSetup(argv)
		self.config.folderSetup()
		self.run()

	def run(self):
		print('Welcome to VirusLand')
		
		v=VelvetPackage(self.config)
		fileName = v.callVelvet()
		

		e=EmbossPack(self.config)
		orfFile=e.ORF_find(self.config.assemblies, self.config.orfs)
		print('filename: ', orfFile)
		
		#orfFile = '/home/lsb456/virusLand2/runs/run4/ORFs/v1S1Xv1S2_ORF.fa'
		p=PaudaPack(self.config, orfFile)
		paudaFile = p.runPauda(orfFile)
		l=Lambs(self.config, orfFile)
		lambFile = l.ORF_find()
		parsedLambs = l.lambda_parser(lambFile)
		print('parsedlambda: ', parsedLambs)
		
		#parsedLambs = '/home/lsb456/virusLand2/run3/lambda/v1S1Xv1S2_ORF_chopped.m8'
	
		#paudaFile = '/home/lsb456/virusLand2/run3/pauda/v1S1Xv1S2_ORF_pauda.blastx'
		jParser= JPaudaParser(self.config, paudaFile)
		paudaParsed = jParser.parse(paudaFile)
		
		#parsedLambs = '/home/lsb456/virusLand2/runs/run4/lambda/v1S1Xv1S2_ORF_chopped.m8'
		#paudaParsed = '/home/lsb456/virusLand2/runs/run4/pauda/v1S1Xv1S2_ORF_pauda.parsed'
		print(self.config.faalist)
		cParser = CParser(self.config)
		cParser.parse('PAUDA', paudaParsed)
		cParser.parse('LAMBDA', parsedLambs)

		k = Krona_generator(self.config)
		
		v=Virus_visualizer(self.config)
		p=v.runVisuals()
		



argv = sys.argv
argc = len(argv)

vl=VirusLand(argv)