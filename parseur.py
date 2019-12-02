import sys
import re
import subprocess
import os
from shutil import rmtree
from os.path import basename, splitext
import argparse

# COMMAND LINE ARGUMENTS AND OPTIONS
parser = argparse.ArgumentParser(description='Convert a pdf file to txt (or xml)', usage='python3 parseur.py [-x|-t] <pdf_to_convert>')
parser.add_argument('-x', '--xml',
					help='output to a xml file', 
					action="store_true", 
					default=False)
parser.add_argument('-t', '--txt',
					help='output to a txt file', 
					action="store_true", 
					default=False)
parser.add_argument(help='pdf file to convert',
					dest='pdf_to_convert')

args = parser.parse_args()

if(args.xml == False and args.txt == False):
	print("Please choose between -x and -t")	
	sys.exit()
elif(args.xml == True and args.txt == True):
	print("Please choose only one option between -x and -t")
	sys.exit()

# args.xml = true/false
# args.txt = true/false
# args.pdf_to_convert = pdf a converti


# FONCTIONS

def recupererParagrapheDuMot(lines, words, skipnum=1):
	sortie = ""
	for line in range(0,len(lines)):
		for word in words:
			if lines[line].lower().find(word.lower()) != -1:
				while(lines[line].rstrip() != ""):
					sortie += lines[line+1].rstrip()
					line = line+1
					if(not skipnum and re.search("^\d",lines[line+1])):
						break
				return sortie
	return "";

def concatXML(var, text):
	var = var.replace("&","&amp;")
	print("\t<"+text+">"+var+"</"+text+">")

# CHECK FICHIER

if not args.pdf_to_convert.endswith(".pdf"):
	print("Not a pdf file...")
	sys.exit()
else:
	subprocess.run(["pdftotext", args.pdf_to_convert])

# LECTURE DU FICHIER

file_to_open = args.pdf_to_convert.replace(".pdf", ".txt")

f = open(file_to_open, "r")
lines = f.readlines()

# CREATION DE LA STRUCTURE DE SORTIE

try:
	os.mkdir("parseur_sortie")
except:
	rmtree("parseur_sortie")
	os.mkdir("parseur_sortie")

# NOM FICHIER

original = args.pdf_to_convert

# TITRE

splitted = args.pdf_to_convert.split("_")
titre = ""
auteur = ""
if(len(splitted) == 3):
	titre = splitted[2].replace('.pdf','').rstrip()
	auteur = splitted[0].replace('.pdf','').rstrip()
else:
	titre = args.pdf_to_convert

# RECHERCHE ET IMPRESSION

abstract = recupererParagrapheDuMot(lines, ["Abstract"]);
references = recupererParagrapheDuMot(lines, ["References"],1);


# PRINT TXT

if(args.xml == True):
	sys.stdout = open('parseur_sortie/' + args.pdf_to_convert.replace('.pdf','.xml'), 'w')
	print("<article>")
	concatXML(original,"preamble")
	concatXML(titre,"titre")
	concatXML(auteur,"auteur")
	concatXML(abstract,"abstract")
	concatXML(references,"biblio")
	print("</article>")
elif(args.txt == True):
	sys.stdout = open('parseur_sortie/' + args.pdf_to_convert.replace('.pdf','.txt'), 'w')
	print("[PREAMBLE]")
	print("\t" + original + "\n")
	print("[TITRE]")
	print("\t" + titre + "\n")
	print("[ABSTRACT]")
	print("\t" + abstract + "\n")

f.close()
