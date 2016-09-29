import subprocess
import os

'''File for compiling taxonomy reference from GBK list file
Only needs to be run once at beginning of program'''

class Krona_generator:
    def __init__(self, config):
        print('Executing KronaGenerator')
        self.cwd = config.cwd
        self.out = config.kronaFiles + 'Krona_Lambda_stats.txt'
        self.taxGenomeHits(config.taxIndexFile, config.stats+'KronaStats_LAMBDA', self.out)
        self.out = config.kronaFiles + 'Krona_PAUDA_stats.txt'
        self.taxGenomeHits(config.taxIndexFile, config.stats+'KronaStats_PAUDA', self.out)

    def taxGenomeHits(self, inTax, inStats, outpath):
        """Requires taxFromGBK output, cParser output Krona_LAMBDA or Krona_PAUDA, and output file name with directory """
        print('Generating Krona files for ', inStats)
        cmdin = self.cwd + '/KronaPrep' + " " + str(inTax) + " " + str(inStats) + " " + str(outpath) 
        print("Cmdin: " + cmdin)
        os.system(cmdin)
