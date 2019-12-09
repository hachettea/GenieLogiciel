# coding: utf-8
import sys
import signal
import re
import subprocess
import os
from shutil import rmtree
from os.path import basename, splitext
import argparse

def quit_properly(sig, frame):
	print("\nProgram halted, bye!")
	sys.exit(0)
signal.signal(signal.SIGINT, quit_properly)

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

# MENU 

folderOfPdf = []
for file in os.listdir(args.folder_to_convert):
	if file.endswith(".pdf"):
		folderOfPdf.append(file)
print("pdf files found in the folder given\n")
for i in range(0,len(folderOfPdf)):
	print(i, "-", folderOfPdf[i])

pdf_files_to_convert = []	
print("\nType the number in front of the pdf file to add it for the converter (when done, type ok):")

while(True):
	x = input()
	if(x == "ok"):
		break
	try: 
		int(x)
	except:
		x = -1
	if(int(x) > len(folderOfPdf)-1 or int(x) < len(folderOfPdf)-1):
		print("Invalid input")
	else:
		if(folderOfPdf[int(x)] in pdf_files_to_convert):
			print("This file is already added")
		else:
			pdf_files_to_convert.append(folderOfPdf[int(x)])	
			print(folderOfPdf[int(x)] + " added to be converted")

# FONCTIONS

def recupererParagrapheDuMot(lines, words):
	sortie = ""
	for line in range(0,len(lines)):
		for word in words:
			if lines[line].find(word.upper()) != -1 or lines[line].find(word) != -1:					
				
				if(lines[line+1].rstrip() == ""):
					line+=1
				while(len(lines[line]) < 5 ):
					sortie += lines[line].rstrip()
					line+=1

				while(lines[line].rstrip() != ""):
					sortie += lines[line].rstrip()
					line+=1
				
				return sortie
	return "";

def recupererCorps(lines, arrayVarsAvant, arrayVarsApres):
	
	#	récuperation de la derniere partie avant le corps + premiere partie après
	# 	check de si la fin du début est egal au courrant -> si oui -> ecrire
	#	check de si le debut de la fin est egal au courrant -> si oui -> stop + return

	sortie = ""
	for line in range(0,len(lines)):
		# skip du debut
		if(lines[line].rstrip().endswith(arrayVarsAvant[-1][-10:])):
			line+=3
			while(lines[line].rstrip()[:10] != arrayVarsApres[0][:10]):
				sortie += lines[line-2].rstrip()
				line+=1
	return sortie

def delControlChars(s): 	# from https://rosettacode.org/wiki/Strip_control_codes_and_extended_characters_from_a_string#Python
	return "".join(i for i in s if 31 < ord(i) < 127)


def concatXML(var, text):
	var = delControlChars(var)

	var = var.replace("\"","&quot;")	# correction xml des caracteres utilisé par le format
	var = var.replace("&","&amp;")
	var = var.replace("\'","&apos;")
	var = var.replace("<","&it;")
	var = var.replace(">","&gt;")

	print("\t<"+text+">"+var+"</"+text+">")  # ajout des balies XML



def convertFile(file_pdf):

	if not file_pdf.endswith(".pdf"):
		print("Not a pdf file...")
		sys.exit()
	else:
		subprocess.run(["pdftotext", args.folder_to_convert + "/" + file_pdf])

	# LECTURE DU FICHIER

	file_to_open = args.folder_to_convert + "/" + file_pdf.replace(".pdf", ".txt")

	f = open(file_to_open, "r")
	lines = f.readlines()

	# NOM FICHIER

	original = file_pdf

	# TITRE

	splitted = file_pdf.split("_")
	titre = ""
	auteur = ""
	if(len(splitted) == 3):
		titre = splitted[2].replace('.pdf','').rstrip()
		auteur = splitted[0].replace('.pdf','').rstrip()
	else:
		titre = file_pdf

	# RECHERCHE ET IMPRESSION

	abstract = recupererParagrapheDuMot(lines, ["Abstract"])
	introduction = recupererParagrapheDuMot(lines, ["Introduction"])
	conclusion = recupererParagrapheDuMot(lines, ["Conclusion"])
	discussion = recupererParagrapheDuMot(lines, ["Discussion"])
	references = recupererParagrapheDuMot(lines, ["References"])

	corps = recupererCorps(lines,[abstract,introduction],[conclusion,discussion,references])

	# PRINT TXT / XML

	if(args.xml == True):
		sys.stdout = open('./parseur_sortie/' + file_pdf.replace('.pdf','.xml'), 'w')
		print("<article>")
		concatXML(original,"preamble")
		concatXML(titre,"titre")
		concatXML(auteur,"auteur")
		concatXML(abstract,"abstract")
		concatXML(introduction,"introduction")
		concatXML(corps,"corps")
		concatXML(conclusion,"conclusion")
		concatXML(discussion,"discussion")
		concatXML(references,"biblio")
		print("</article>")
	elif(args.txt == True):
		sys.stdout = open('./parseur_sortie/' + file_pdf.replace('.pdf','.txt'), 'w')
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
try: 
	os.listdir(args.folder_to_convert)
except:
	print("Not a folder...")
	sys.exit()

if len(pdf_files_to_convert) != 0:
	try: 	# verif dossier de sortie + destruction si existant
		os.mkdir("./parseur_sortie")
	except:
		rmtree("./parseur_sortie")
		os.mkdir("./parseur_sortie")
	
print("> Start")
for file in pdf_files_to_convert:
	if file.endswith(".pdf"):
		sys.stdout = oldstdout  # restauration stdout
		print("\t> processing: " + file)
		convertFile(file)

sys.stdout = oldstdout
print("> Done")
