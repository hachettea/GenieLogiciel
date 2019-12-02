import sys
import re
import subprocess
import os
from shutil import rmtree
from os.path import basename, splitext

# FONCTIONS

def recupererParagrapheDuMot(lines, words, sortie):
	for line in range(0,len(lines)):
		for word in words:
			if lines[line].lower().find(word.lower()) != -1:
				while(lines[line].rstrip() != ""):
					sortie += lines[line+1].rstrip()
					line = line+1
					if(re.search("^\d",lines[line+1])):
						break
				return sortie;
	return "";

def concatXML(var, text):
	print("\t<"+text+">"+var+"\t</"+text+">")

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

# ==================
original = ""
titre = ""
abstract = ""
# ==================

# NOM FICHIER

original = sys.argv[1]

# TITRE

# ========================================
# TODO: Découper l'année et l'auteur
# ========================================

titre = sys.argv[1].split("_")[2].replace('.pdf','')

# RECHERCHE ET IMPRESSION

abstract = recupererParagrapheDuMot(lines, ["ABSTRACT"], abstract);

# ========================================
# TODO: Trouver le reste des sections
# ========================================


# PRINT TXT

if(len(sys.argv) == 3):
	sys.stdout = open('parseur_sortie/' + sys.argv[1].replace('.pdf','.txt'), 'w')
	if(sys.argv[2] == "-x"):
		print("<article>")
		concatXML(original,"original")
		concatXML(titre,"titre")
		concatXML(abstract,"abstract")
		print("</article>")
	if(sys.argv[2] == "-t"):
		print("[ORIGINAL]")
		print("\t" + original + "\n")
		print("[TITRE]")
		print("\t" + titre + "\n")
		print("[ABSTRACT]")
		print("\t" + abstract + "\n")
else:
	print("Utilisation: python3 parseur.py -x/-t")
	print("\t-x pour sortir en xml")
	print("\t-t pour sortir en text avec balises")


# FIN

f.close()
