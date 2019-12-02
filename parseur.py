import sys
import re
import subprocess
import os
from shutil import rmtree
from os.path import basename, splitext

# FONCTIONS

def recupererParagrapheDuMot(lines, words):
	for line in range(0,len(lines)):
		for word in words:
			if lines[line].lower().find(word.lower()) != -1:
				print("[" + words[0] + "]")
				while(lines[line].rstrip() != ""):
					print("\t" + lines[line+1], end = '')
					line = line+1
					if(re.search("^\d",lines[line+1])):
						break
				print()
				return 1;
	return 0;
	
# MOTS A VERIFIER

abstractArray = ["ABSTRACT"]

# CHECK FICHIER

if not sys.argv[1].endswith(".pdf"):
	print("Not a pdf file...")
	sys.exit()
else:
	subprocess.run(["pdftotext", sys.argv[1]])

file_to_open = sys.argv[1].replace(".pdf", ".txt")

# LECTURE DU FICHIER

f = open(file_to_open, "r")
lines = f.readlines()

# CREATION DE LA STRUCTURE DE SORTIE

try:
	os.mkdir("parseur_sortie")
except:
	rmtree("parseur_sortie")
	os.mkdir("parseur_sortie")

sys.stdout = open('parseur_sortie/' + sys.argv[1].replace('.pdf','.txt'), 'w')

# NOM FICHIER

print("[ORIGINAL]\n\t" + sys.argv[1] + "\n")

# ELEMENTS TROUVE

trouveAbstract = 0;



# TITRE

print("[TITRE]")

print("\t" + sys.argv[1].split("_")[2].replace('.pdf','') + "\n")

# RECHERCHE ET IMPRESSION

if not trouveAbstract and recupererParagrapheDuMot(lines, abstractArray) == 1: 
	trouveAbstract = 1

f.close()
