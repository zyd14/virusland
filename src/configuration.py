'''Configuration file.  This file parses the config.vl resources file 
which is to be filled in by the user with the appropriate parameters for
velvet, as well as the directories of the reference FAA and GBK files

config.vl file format:

[VELVET-FORMAT] <-fa, -fasta, -raw, -fasta.gz -fastq.gz -raw.gz -sam -bam -fmtAuto>
[VELVET-KMER] <kmer size*>
[VELVET-READTYPE] <-shortPaired, -shortPaired2, -short, -short2, -long, -longPaired, -reference> 
[FAA-DIR] <directory folder containing reference proteins as .faa files>
[GBK-DIR] <directory folder containing reference viral genomes as .gbk files>
[PAUDA-LOCATION] <directory location of PAUDA software>
[STOP]


'''
import os
import sys
import glob

class Configuration:

	def __init__(self):
		'''Takes the config.vl file path as argument'''
		#self.title=argv[1]
		#self.runName=argv[1]
		self.dir=os.path.dirname(os.path.realpath(__file__))
		self.cwd=os.getcwd()	#current working directory - should be /src folder
		self.vlhome=os.path.abspath(os.path.join(self.cwd,os.pardir))
		self.realpath=os.path.realpath(__file__)
		print('Dir: %s cwd: %s realpath: %s'%(self.dir,self.cwd,self.realpath))
		print('vlhome %s'%(self.vlhome))
		#self.runFolder=self.vlhome+'/'+self.runName 	#folder for each run
		self.velvetformat=None							#format of velvet input sequences (.fa, .fasta, etc)
		self.velvetkmer=None							#kmer size for input sequences
		self.velvetreadtype=None						#sequence readtype (short, long, shortPaired, longPaired)
		self.faadir=None						#
		self.gbkdir=None
		#self.seq1=argv[2]
		#self.seq2=argv[3]
		#print('Seq1: ', self.seq1)
		#print('Seq2: ', self.seq2)
		#make basefile name which can be used to make file names for each module
		#self.basename=self.seq1+'X'+self.seq2
		self.indexFolder = self.vlhome+'/indexes'
		self.faa = self.indexFolder+'/faa/'			#folder containing allFAAs.faa and faaList.txt
		#self.faaindex = self.faa+'allFAAs.faa'	
		self.faalist = self.faa+'faaList.txt'	#compiled list of faa file locations
		self.faaAll = self.faa + 'allFAAs.faa'	#concatenated faa files
		self.gbk = self.indexFolder+'/gbk/'			#folder for gbkList.txt
		self.gbkList = self.gbk+'gbkList.txt' 	#compiled list of gbk file locations
		self.taxindex = self.indexFolder+'/taxIndex/' 		#taxFromGBK genomeTax file outputs here
		self.taxIndexFile = self.taxindex+'taxFromGBK.txt'
		self.paudaindex= self.indexFolder+'/paudaindex/'
		self.lambindex= self.indexFolder+'/lambdaindex/'
		print('faa', self.faa, 'gbk', self.gbk)
		self.runs = self.vlhome+'/runs'
		#Locations for generated analysis files for each run
		'''self.assemblies = self.runFolder+'/assembled'
		self.lamb = self.runFolder+'/lambda/'
		self.orfs = self.runFolder+'/ORFs/'
		self.pauda = self.runFolder+'/pauda/'
		self.stats = self.runFolder+'/stats/'
		self.kronaFiles = self.runFolder+'/kronaFiles/'
		self.paudaloc = None'''
		
		#print('Opening ', fpath)
		#self.setup(fpath)
		#self.folderSetup()


	def indexSetup(self, fpath):
		fd = open(fpath, 'r')
		for line in fd:
			if line.startswith("[FAA-DIR]"):
				option = line.split("[FAA-DIR]")[1].strip()
				if option != "":
					self.faadir = option
				else:
					print ("[Error] Cannot find directory for FAA files")
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()
			if line.startswith("[GBK-DIR]"):
				option = line.split("[GBK-DIR]")[1].strip()
				if option != "":
					self.gbkdir = option
				else:
					print ("[Error] Cannot find directory for GBK files!")
					print('Please check to make sure you have filled out the config.vl file')
					sys.exit()
			if line.startswith("[PAUDA-LOCATION]"):
				option = line.split("[PAUDA-LOCATION]")[1].strip()
				if option != "":
					self.paudaloc = option
				else:
					print ("[Error] Cannot find directory for FAA files")
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()

	def runSetup(self,argv):
		#sets up variables for each run - gets called each time virusLand runs
		#set up try/except so it handles error if not valid file path for fpath
		fpath=argv[4]
		self.title=argv[1]
		self.runName=argv[1]
		self.seq1=argv[2]
		self.seq2=argv[3]
		print('Seq1: ', self.seq1)
		print('Seq2: ', self.seq2)
		self.runFolder=self.runs+'/'+self.runName 	#folder for each run

		self.assemblies = self.runFolder+'/assembled'
		self.lamb = self.runFolder+'/lambda/'
		self.orfs = self.runFolder+'/ORFs/'
		self.pauda = self.runFolder+'/pauda/'
		self.stats = self.runFolder+'/stats/'
		self.kronaFiles = self.runFolder+'/kronaFiles/'
		self.paudaloc = None

		fd = open(fpath,'r')
		for line in fd:
			if line.startswith ("[VELVET-FORMAT]"):
				option = line.split("[VELVET-FORMAT]")[1].strip()
				if option != "":
					self.velvetformat = option
				else:
					print("[Error] Cannot find velvet format info!")
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()
			if line.startswith ("[VELVET-KMER]"):
				option = line.split("[VELVET-KMER]")[1].strip()
				if option != "":
					try:
						self.velvetkmer = int(option)
					except:
						pass
				else:
					print('[Error] Cannot find velvet kmer info!')
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()
			if line.startswith("[VELVET-READTYPE]"):
				option = line.split("[VELVET-READTYPE]")[1].strip()
				if option != "":
					self.velvetreadtype = option
				else:
					print("[Error] Cannot find readtype for velvet!")
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()
			if line.startswith("[PAUDA-LOCATION]"):
				option = line.split("[PAUDA-LOCATION]")[1].strip()
				if option != "":
					self.paudaloc = option
				else:
					print ("[Error] Cannot find directory for FAA files")
					print("Please check to make sure you have filled out the config.vl file")
					sys.exit()
		self.info()
		fd.close()

	#Sets up 
	def folderSetup(self):
		print('Runfolder', self.runFolder)
		print('Going to create %s'%self.runFolder)
		'''if os.path.isdir(self.runFolder):
			print(self.runFolder + ' already created.  To avoid overwriting data, please either re-run virusLand with a new run name or delete the ' + self.runFolder + ' folder')
			print('Program will now quit')
			quit()'''
		folders = [self.runFolder, self.assemblies, self.lamb, self.orfs, self.pauda, self.stats, self.kronaFiles]
		for f in folders:
			if os.path.isdir(f):
				print('folder already exists with that name!')
			else:
				os.makedirs(f)
				print('Folder %s created'%f)

 	def info (self):
 		print ("[TITLE] " + str(self.title))
 		print ("[READ 1] " + str(self.seq1))
 		print ("[READ 2] " + str(self.seq2))
 		print ("[VELVET-FORMAT] " + str(self.velvetformat))
 		print ("[VELVET-KMER] " + str(self.velvetkmer))
 		print ("[VELVET-READTYPE] " + str(self.velvetreadtype))
 		print ("[VELVET-OUTPUT] " + str(self.assemblies))
 		print ("[ORFS] " + str(self.orfs))
 		print ("[LAMBDA] " + str(self.lamb))
 		print ("[PAUDA] " + str(self.pauda))
 		print ("[FAA-DIR] " + str(self.faadir))
 		print ("[GBK-DIR] " + str(self.gbkdir))

