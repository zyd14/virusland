'''A class to handle Pauda processes 
Still needs update to paudaLocation so that it uses relative path / able to 
find Pauda on other machines
Might also want some way to handle building index when index folder exists but has nothing in it;
Pauda will throw error if index folder exists but has nothing in it
'''
import glob
import subprocess
import ntpath

class PaudaPack:
    def __init__(self, config, fileName):
        self.paudaLocation = config.paudaloc
        self.inFolder = config.orfs
        self.inFiles = glob.glob(config.orfs + '*')
        self.inFile = fileName
        print(self.inFiles)
        self.index = config.paudaindex
        print('inFile: ', self.inFile)
        self.blastxOut = config.pauda + self.get_leaf(self.inFile) + '_pauda.blastx'

    '''Execute Pauda run'''
    def runPauda(self, inFile):
        subprocess.call([self.paudaLocation + '/pauda-run', '--slow', inFile, self.blastxOut, self.index])
        return self.blastxOut

    '''Generate file names'''
    def get_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail.split('.')[0]
    