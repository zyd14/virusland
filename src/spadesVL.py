#virusland.py
#Author: Zachary Romer, romerzs14@gmail.com
#Date 09/28/2016

import glob
import subprocess
import os
import argsparse
import sys
'''
TODO:
-Write argparser
-check_config method? to check that folders assigned actually exist? maybe create if not?
-main
-call graphics module
-cFileParse3.cpp call or rewrite
'''


class OutCalls:

	def __init__(self, config, runName = None):
		argv         = sys.argv
		fpath        = argv[4]
		self.title   = argv[1]
		self.runName = argv[1]
		self.seq1    = argv[2]
		self.seq2    = argv[3]
		self.runName = runName

		self.vlhome = os.path.abspath(os.path.join(os.getcwd(),os.pardir)) #Go up one directory from src folder code should be executing from

		self.indexFolder  = self.vlhome+'/indexes'
		self.paudaindex   = self.indexFolder+'/paudaindex/'
		self.lambindex    = self.indexFolder+'/lambdaindex/'
		self.taxindex     = self.indexFolder+'/taxIndex/' 		#taxFromGBK genomeTax file outputs here
		self.gbk          = self.indexFolder+'/gbk/'			#folder for gbkList.txt
		self.faa          = self.indexFolder+'/faa/'			#folder containing allFAAs.faa and faaList.txt
		self.faalist      = self.faa+'faaList.txt'	#compiled list of faa file locations
		self.faaAll       = self.faa + 'allFAAs.faa'	#concatenated faa files
		self.taxIndexFile = self.taxindex+'taxFromGBK.txt'
		self.gbkList      = self.gbk+'gbkList.txt' 	#compiled list of gbk file locations
		

		self.runs       = self.vlhome+'/runs'
		self.runFolder  = self.runs+'/'+self.runName 	#folder for each run

		self.assemblies = self.runFolder+'/assemblies'
		self.lambda_out = self.runFolder+'/lambda/'
		self.orfs       = self.runFolder+'/ORFs/'
		self.pauda_out  = self.runFolder+'/pauda/'
		self.stats      = self.runFolder+'/stats/'
		self.kronaFiles = self.runFolder+'/kronaFiles/'
		self.paudaloc   = None

	def getArgs(self):
		#need to use argsparse module to get command-line options
		return self

	def callSpades(self, seq1, seq2, outPath, k=None, meta=False):
		#Should check to make sure spades.py exists here, exit program right waway otherwise with explanation
		spadesPath = os.getcwd()+'/spades/spades.py'

		if not k:
			k = '21,33,55,77,99,127'

		if meta:
			assemblerOption = '--meta'
		else:
			assemblerOption = '--only-assembler'

		os.system('{spadesPath!s} -k {k!s} {assemblerOption!s} -1 {seq1!s} -2 {seq2!s} -o {outPath!s}'.format(**locals()))

	def callVelvet(self, fmt, outDir, seq1, seq2, readtype, kmer):

		read1 = os.path.basename(seq1).split('.')[0]
		read2 = os.path.basename(seq2).split('.')[0]

		outName   = '{read1!s}X{read2!s}.fa'.format(**locals)
		velvetOut = '{outDir!s}/{read1!s}X{read2!s}'.format(**locals)

		print "Assembling reads with velvet"
		print 'Velvet hashing {!r}'.format(outName)
		subprocess.call(['velveth', velvetOut, kmer, fmt, readtype, seq1, seq2])
		
		print 'Velvet graphing {!r}'.format(outName)
		os.system('velvetg {!s} -exp_cov auto'.format(velvetOut))

		contigFile = velvetOut + '/contigs.fa'
		moveFiles(contigFile, out, keepOld = False)

	def callEmboss(self, assembly_folder, out_dir):

		files = glob.glob(assembly_folder+'/*')

		print 'Executing Emboss ORF prediction'

		for input_file in files:
			outname = out_dir + os.path.basename(input_file).split('.')[0] + '_ORF.fa'
			args    = 'getorf -sequence {!s} -outseq {!s} -minsize 117 -find 3'.formats(input_file, outname)
            print(args)
            subprocess.call(args, shell=True)

    def callPauda(self, orf_folder, file_name, pauda_dir, pauda_out, pauda_index, pauda_loc):
    
    	print 'Executing Pauda read mapper'
    	
    	blastX_out = pauda_out + os.path.basename(file_name).split('.')[0] + '_pauda.blastx'
    	args       = [pauda_loc + '/pauda-run', '--slow', inFile, blastX_out, pauda_index]

    	print args
		subprocess.call(args)

	def callLambda(self, faa_all, lambda_out, input_orfs, parseOutput = True):

		files = glob.glob(input_orfs+'/*')
		for input_file in files:
			file_name = os.path.basename(input_file).split('.')[0]
			out_path  = lambda_out + file_name + '.m8'
			args = 'sudo lambda -q {!s} -d {!s} -o {!s}'.format(input_file, faa_all, out_path)
			print 'Outputing Lambda mapping to {!r}'.format(out_path)
			print args
			subprocess.call(args, shell=True)
			subprocess.call(['sudo', 'chmod', '666', out_path])
			if parseOutput:
				parseLambda(out_path)

	def parseLambda(self, file_in):

		#Add try/except block later to catch filepath errors and allow for re-input
		file_in = checkFilePath(file_in, 'LAMDBA OUTPUT PARSING ERROR: NO FILE AT PATH {!S}'.format(file_in))

		parsed_name = file_in.split('.')[0]+'_parsed.m8'
		f = open(file_in, 'r')
		o = open(parsed_name, 'w')
		while True:
			line = f.readline()
			if line == "":
				f.close()
				o.close()
				break
			output = re.split(r'\t+', line)
			o.write(output[0]+"\t"+output[1]+"\t"+output[10]+"\n")

	def jPaudaParser(self, file_in, file_out):
		#Add try/except block later to catch filepath errors and allow for re-input
		file_in = checkFilePath(file_in, 'PAUDA OUTPUT PARSING ERROR: NO FILE AT PATH {S}'.format(file_in))
		fin     = open(file_in, 'r')
		fout    = open(file_out, 'w')
		print ''
		line = fin.readline()
		if re.search('^Query=', line):
			currQuery = line[6:]
		if re.search('^Expect = ', line):
			currExp = line[9:]
		if re.search('^\>', line):
			currHit = line[1:]
		lineOut = currQuery + "\t" + currHit + "\t" + currExp + "\n"
		fout.write(lineOut)

	def checkFilePath(self, file_in, errMsg=''):
		while not os.path.isfile(file_in) and file_in != '-q':
			if not errMsg:
				errMsg = 'No file at path {}'.format(file_in)
			print errMsg
			file_in = input('Please re-enter the file path (or -q to quit): ')
		if file_in == '-q':
			sys.exit()
		return file_in

	def moveFiles(self, oldLoc, newLoc, keepOld = True):
		os.system('mv {} {}'.format(oldLoc, newLoc))
		if not keepOld:
			os.system('rm -r {}'.format(os.path.dirname(oldLoc)))

