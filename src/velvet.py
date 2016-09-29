''' Class managing velvet: instantiate this class so that command of velvet
 can match user's system settings.
 author: Zach Romer
 date: 2014/12/08
VelvetPackage fetches the reads to be assembled and calls velvet with the
appropriate parameters provided in the config file'''

import glob
import subprocess
import os
import ntpath

class VelvetPackage:

    def __init__(self, config):
        self.fmt = config.velvetformat
        self.out = config.assemblies
        self.seq1=config.seq1
        self.seq2=config.seq2
        print('Velvet seq1: ', self.seq1)
        print('Velvet seq2: ', self.seq2)
        self.kmer = config.velvetkmer
        self.readType = config.velvetreadtype
        print('Reads: ',config.velvetreadtype)
        self.vCmd = None
        print('velvet hashing and graphing complete')

    def callVelvet(self):
        '''Call velvet with parameters provided in contig file'''
        print ('velvet output directory: ' + self.out)
        print ('PairedType: ', self.readType)
        
        r1 = self.seq1
        r2 = self.seq2

        #Generate unique names for output
        r1Name = self.get_leaf(r1)
        r2Name = self.get_leaf(r2)
        print('r1: ', r1Name, 'r2:', r2Name)
        fileName = r1Name + 'X' + r2Name
        outFolder = self.out + '/' + fileName

        #Output velvet system commands
        print('velvet hashing ' + fileName)
        subprocess.call(['velveth', outFolder, str(self.kmer), self.fmt, self.readType,  r1, r2])
        print('velvet graphing ' + r1Name + 'X' + r2Name)
        x = '-exp_cov auto'
        print('velvetg on ', outFolder)
        os.system('velvetg '+ outFolder+ ' '+ x)

        #Move contig files, clean up unnecessary files
        self.moveFiles(outFolder, fileName)

    def moveFiles(self, folder, fileName):
        '''Move contig files out of velvet processing folder and delete uneeded
        velvet processing files to free up memory'''
        contigFile = folder+'/contigs.fa'
        fileRename = self.out + '/' + fileName + '.fa'
        os.system('cd ' + folder)
        os.system('mv ' + contigFile + ' ' + fileRename)
        os.system('rm -r ' + folder)

    def get_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail.split('.')[0]