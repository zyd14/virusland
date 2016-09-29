import subprocess
import glob
import ntpath
import pipes
import sys
import os
import re


''' Need to either have user create lamda index or have function to do so.
Lambda index is created using lambda_indexer -d DATABASE.fasta
Add function for generating more appropriate name if Python will let me'''

class Lambs:
	'''Needs Indexing function to be called once'''
	'''Also requires faaAll concatenated faa file'''
	def __init__(self, config, fileName):
		self.faaIndex = config.faaAll
		self.lambdaOut = config.lamb
		self.ORFs = config.orfs 
		self.fileIn = fileName
	def get_leaf(self, path):
		head, tail = ntpath.split(path)
		return tail.split('.')[0]

	'''Call ORF-finding Lambda function'''
	def ORF_find(self):
		fileIn = self.fileIn
		basepath = self.ORFs
		files = glob.glob(basepath+'/*')
		for i in files:
			k = pipes.quote(i)
			name = self.get_leaf(k).split('.')
			print('File name is: ', name[0])
			outname = self.lambdaOut+name[0]+'.m8'
			print(outname)
			args = 'sudo lambda -q %s -d %s -o %s' % (k, self.faaIndex, outname)
			print(args)
			subprocess.call(args, shell=True)
			os.system('sudo chmod 666 '+outname)
		return outname
		
		'''Parses ORF output file for downstream analysis'''
	def lambda_parser(self, fileIn):
		basepath = self.lambdaOut
		outname = basepath+self.get_leaf(fileIn)+'_chopped.m8'
		f = open(fileIn, 'r')
		o = open(outname, 'w')
		while True:
			line = f.readline()
			if line == "":
				f.close()
				o.close()
				break
			output = re.split(r'\t+', line)
			o.write(output[0]+"\t"+output[1]+"\t"+output[10]+"\n")
		return outname
				
