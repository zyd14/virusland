# Operating parsers to extract files from output of other programs and prepare data for 
'''Really need to clean up code in this module to make more sense'''

import os
import glob
import ntpath

class JPaudaParser:
    """Class that extracts key information from output of Pauda and save to a new
    file. Example:
    >>> parser = JPaudaParser()
    >>> inpath = "data/run01.fastq"
    >>> outpath = "data/out01.fastq"
    >>> parser.parse(inpath, outpath)
    Uses JPauda .java file provided in src folder
    """
    def __init__(self, config, paudaFile):
        self.exe = 'JPauda'
        self.src = config.vlhome + '/src/'
        print('Running parser')
        self.out = config.pauda+self.get_leaf(paudaFile)+'.parsed'
        print('pauda:', config.pauda)
        print('orfs ', config.orfs)
        print('inFile: ', paudaFile)
        print('out', self.out)

    #Parse using JPauda parser        
    def parse(self, inFile):
        cmd = 'java ' + self.exe + ' ' + inFile + ' ' + self.out
        print('Command: ' + cmd)
        try:
            os.system(cmd)
        except:
            print ("Cannot execute command: " + cmdin)
        return self.out

    def get_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail.split('.')[0]


'''Needs e-value threshold, compiled faa file, pauda output file, and number of genomes 
    This module generates each of the 4 stats files for both Lambda and PAUDA outputs; HV_, coverage_, hits_by_protein_, and Krona_
'''
class CParser:
    '''Need to call cFileParse.cpp to get parsed Pauda file'''
    def __init__(self, config):
        self.cmd = "./StatsGenerator"
        self.eValue = '0.0001'
        self.faaFiles = config.faalist
        self.outDir = config.stats
        print('FAA list: ', config.faalist)
    def parse(self, typeIn, fileIn):
        #arguments: cParser PAUDA/LAMBDA/OTHER threshold faaList.txt paudaParsedInput
            print('Trying to parse')
            cmdin = self.cmd + " " + typeIn + " " + self.eValue  + " " + self.faaFiles + ' ' + fileIn + " " + self.outDir
            print('Command: ' + cmdin)
            try:
                os.system(cmdin)
            except:
                print ("Cannot execute command: " + cmdin)

