import os
import glob
import sys
from configuration import Configuration
'''This module is to be run after preCompiler.py and before virusLand.py.
It will build all the needed indexes prior to analysis.
buildIndexes.py should be run after any time the reference FAA or GBK files are updated

Usage: python buildIndexes.py pathToConfigFile
'''
class IndexBuilder:
    def __init__(self, argv):
        print('Building indexes')
        configPath = argv[1]
        config = Configuration()
        config.indexSetup(configPath)
        self.FAAs = config.faadir
        self.GBKs = config.gbkdir
        self.outFAA = config.faa
        self.faaAll = config.faaAll
        self.faaList = config.faalist
        self.outGBK = config.gbk
        self.gbkList = config.gbkList
        self.paudaloc = config.paudaloc
        self.paudaindex = config.paudaindex
        self.lambindex = config.lambindex
        self.taxindex = config.taxindex
        self.taxIndexFile = config.taxIndexFile
        self.cwd = config.cwd
        self.createFolders()
        self.buildIndexes()

    def createFolders(self):
        #Creates index containing folders
        folders=[self.outFAA, self.outGBK, self.lambindex, self.taxindex]
        for j in folders:
            if os.path.isdir(j):
                print('Folder %s already written'%j)
            else: 
                os.makedirs(j)
    def buildIndexes(self):
        '''Checks to see if index directories have been created; if not,
        create index files and folders'''
        if os.path.isfile(self.faaList)==False:
            self.makeListFile(self.FAAs, 'faa', self.outFAA)
            #self.concatFAAs()
        else:
            print('faaList.txt already exists, skipping creation (delete current copy if trying to create new index)')

        if os.path.isfile(self.faaAll)==False:
            self.concatFAAs()
        else:
            print('allFAAs.faa already created, skipping creation (delete current copy if trying to create new index')

        if os.path.isfile(self.gbkList)==False:
            self.makeListFile(self.GBKs, 'gbk', self.outGBK)
        else:
            print('GBK file already exists, skipping creation (delete current copy if trying to create new index')

        if os.path.isdir(self.paudaindex)==False:
            self.paudaIndex()
        else:
            print('Pauda index already created (delete entire paudaindex folder and re-run to create index)')

        if os.path.isdir(self.lambindex)==False:
            os.makedirs(self.lambindex)
            #self.lambdaIndex()
        else:
            #self.lambdaIndex()
            print('Lambda index folder exists, creating file')

        if os.path.isfile(self.taxIndexFile)==False:
            self.runTaxFromGBK(self.gbkList, self.taxIndexFile)
        else:
            print('Taxonomy index file already exists, skipping creation')


    def concatFAAs(self):
        '''A function to write a file containing a concatenation of all the FAA 
        genome files, to be used by PAUDA and downstream visualization modules.
        Requires that FAA folder location is specified in the config.vl file''' 
        
        search = self.FAAs + '*/*.faa > '
        outCmd = search + self.faaAll
        os.system('cd ' + self.FAAs)
        os.system('cat ' + outCmd)
    
    def makeListFile(self, direct, typ, out):
        '''A function which writes out a file containing a list of the the gbk locations,
        to be used by a downstream visualization module. Requires that the location of 
        the folder containing the gbks is specified in the config.vl file'''
        print('Writing list file')
        path = direct + '*/*.' + typ
        print(path)
        fileNames = glob.glob(path)
        fileOut = out + typ + 'List.txt'
        print(fileOut)
        myFile = open(fileOut, 'w')  
        for x in fileNames:
            myFile.write(x + '\n')
        myFile.close()

    def paudaIndex(self):
        os.system(self.paudaloc + '/pauda-build ' + self.faaAll + ' ' + self.paudaindex)

    def lambdaIndex(self):
        #lambda index files go to faa folder by default - may want to change
        args='sudo lambda_indexer -d %s'%(self.faaAll)
        os.system(args)

    def runTaxFromGBK(self, inpath, outpath):
        """Builds index file for Krona from gbkList.txt"""
        cmdin = self.cwd + '/TaxIndexer.vl' + " " + str(inpath) + " " + str(outpath)
        os.system(cmdin)

argv = sys.argv
buildIndexes = IndexBuilder(argv)