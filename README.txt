INSTALLATION
System Requirements
•	*nix OS
•	Minimum RAM requirement= 16GB; dependent upon Velvet needs (function of k, number of reads, and read size)
•	Java runtime environment version 1.6 or higher
•	Tested in BioLinux7 and Ubuntu 12.04.1 LTS, 64-bit OS

Required Compilers/Interpreters and Software
Compilers (typically distributed in *nix OS): javaC, g++ and python

Software:
Velvet: https://github.com/dzerbino/velvet/tree/master 
•	Reference Velvet’s README.txt for instructions for compiling.
•	VirusLand assumes location of Velvet is within the /bin directory.
•	Tested using version 1.0.19 (current as of June 1, 2015)
Emboss: http://emboss.sourceforge.net/download/ 
•	Reference Emboss site listed here for instructions regarding unpacking and compiling.
•	VirusLand assumes location of Emboss is within the /bin directory.
•	Tested using version 6.6.0 (current as of June 1, 2015)
Lambda: http://www.seqan.de/projects/lambda/ 
•	Reference Lambda site for instructions regarding unpacking and compiling.
•	VirusLand assumes location of Lambda is within the /bin directory.
•	Tested using version 0.4.7 (current as of June 1, 2015)
Bowtie2: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml 
•	Reference Bowtie2 site for instructions regarding unpacking and compiling.
•	VirusLand assumes location of Bowtie2 is within the /bin directory
•	Adding Bowtie 2 directory to your PATH environment variable.
•	Tested using version 2.1.0 (current as of June 1, 2015)
PAUDA: http://ab.inf.uni-tuebingen.de/software/pauda/ 
•	Application must be unzipped; VirusLand assumes location is within the /bin directory
•	PAUDA is dependent upon the Bowtie2 software. Bowtie2 must be installed as well.
•	Tested using version 1.0.1 (current as of June 1, 2015)

Each tool should be added to your PATH environment variable. Note, the Bio-Linux OS includes Velvet, EMBOSS and Bowtie2 requiring only the installation of Lambda and PAUDA.


Installing VirusLand
Unzip the VirusLand installation package maintaining the file structure.
