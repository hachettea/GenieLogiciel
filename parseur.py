import sys
import re
import subprocess
import os
from shutil import rmtree
from os.path import basename, splitext
import argparse

# COMMAND LINE ARGUMENTS AND OPTIONS
parser = argparse.ArgumentParser(description='Convert a folder of pdf files to txt (or xml)', usage='python3 parseur.py [-x|-t] <folder_to_convert>')
parser.add_argument('-x', '--xml',
					help='output to a xml file', 
					action="store_true", 
					default=False)
parser.add_argument('-t', '--txt',
					help='output to a txt file', 
					action="store_true", 
					default=False)
parser.add_argument(help='folder containing the pdf files to convert',
					dest='folder_to_convert')

args = parser.parse_args()

if(args.xml == False and args.txt == False):
	print("Please choose between -x and -t")	
	sys.exit()
elif(args.xml == True and args.txt == True):
	print("Please choose only one option between -x and -t")
	sys.exit()

# args.xml = true/false
# args.txt = true/false
# args.folder_to_convert = dossier de pdf a convertir


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
	var = var.replace("&","&amp;")	# correction xml de & (utilisé par le format)
	print("\t<"+text+">"+var+"</"+text+">")  # ajout des balies XML



def convertFile(pdf_to_convert):

	if not pdf_to_convert.endswith(".pdf"):
		print("Not a pdf file...")
		sys.exit()
	else:
		subprocess.run(["pdftotext", pdf_to_convert])

	# LECTURE DU FICHIER

	file_to_open = pdf_to_convert.replace(".pdf", ".txt")

	f = open(file_to_open, "r")
	lines = f.readlines()

	# NOM FICHIER

	original = pdf_to_convert

	# TITRE

	splitted = pdf_to_convert.split("_")
	titre = ""
	auteur = ""
	if(len(splitted) == 3):
		titre = splitted[2].replace('.pdf','').rstrip()
		auteur = splitted[0].replace('.pdf','').rstrip()
	else:
		titre = pdf_to_convert

	# RECHERCHE ET IMPRESSION

	abstract = recupererParagrapheDuMot(lines, ["Abstract"]);
	references = recupererParagrapheDuMot(lines, ["References"],1);


	# PRINT TXT / XML

	if(args.xml == True):
		sys.stdout = open('parseur_sortie/' + pdf_to_convert.replace('.pdf','.xml'), 'w')
		print("<article>")
		concatXML(original,"preamble")
		concatXML(titre,"titre")
		concatXML(auteur,"auteur")
		concatXML(abstract,"abstract")
		concatXML(references,"biblio")
		print("</article>")
	elif(args.txt == True):
		sys.stdout = open('parseur_sortie/' + pdf_to_convert.replace('.pdf','.txt'), 'w')
		print("[PREAMBLE]")
		print("\t" + original + "\n")
		print("[TITRE]")
		print("\t" + titre + "\n")
		print("[ABSTRACT]")
		print("\t" + abstract + "\n")

	f.close()
	os.remove(file_to_open) # suppression du fichier de base convertit par pdftotext


oldstdout = sys.stdout # backup interface stdout

# CREATION DE LA STRUCTURE DE SORTIE

try: 	# verrif dossier de sortie + destruction si existant
	os.mkdir("parseur_sortie")
except:
	rmtree("parseur_sortie")
	os.mkdir("parseur_sortie")

folder = ""		# vérification folder
try: 
	folder = os.listdir(args.folder_to_convert)
except:
	print("Not a folder!")
	sys.exit()


print("> Start")
for file in folder:
	if file.endswith(".pdf"):
		sys.stdout = oldstdout  # restauration stdout
		print("\t> processing: " + file)
		convertFile(args.folder_to_convert + "/" + file)

sys.stdout = oldstdout
print("> Done")
