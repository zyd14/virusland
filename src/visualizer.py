#VirusLand Visualizer

import os
import sys

class Virus_visualizer:
	def __init__(self, config):
		self.cwd=config.cwd
		print('do something')
	def runVisuals(self):
		cmdin = 'java -jar ' + self.cwd + '/virusGraphics.jar'
		print('Running command: ' + cmdin)
		
		os.system(cmdin)