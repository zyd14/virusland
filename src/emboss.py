# Class of managing Emboss: instantiate this class so that command of Emboss
# and match user's system setting
'''A module to predict ORFs from sequences assembed by Velvet
Input: assembled velvet sequence .fa file
Output: .fa file containing predicted ORF regions'''
import ntpath
import pipes
import glob
import subprocess

class EmbossPack:
    def __init__(self, config):
        self.emIn = config.assemblies
        self.emOut = config.orfs
    def get_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail.split('.')[0]
    def ORF_find(self, folder, outDir):       
        files = glob.glob(folder+'/*')
        outname=None
        for i in files:
            print i
            k = pipes.quote(i)
            outname =  outDir + self.get_leaf(k) +'_ORF.fa'
            args = 'getorf -sequence %s -outseq %s -minsize 117 -find 3' % (k, outname)
            print(args)
            subprocess.call(args, shell=True)
        print('Emboss output name: ', outname)
        return outname