#!/usr/bin/python3
#USAGE:  Python 3.6.9
#python3 imgOcr2translate.py -i imagesdirectory/

# by Antonio "Visi@n" Broi broi.antonio@gmail.com
# http://www.broi.it aNTbRO

 
# LICENSE M.I.T.              https://opensource.org/licenses/MIT
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
#OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
#OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
#from colour_demosaicing import demosaicing_CFA_Bayer_bilinear
import os
import sys
import locale
import subprocess
import googletrans
from googletrans import Translator
import signal
import time
from datetime import datetime

os.environ["PYTHONIOENCODING"] = "utf-8" 
myLocale=locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8") 


#print(("""\
#
#  _____________________________________
#( CHECKMATE TO TRANSLATE by IMAGES IN PYTHON BY )
#( VISION                              )
# -------------------------------------
#    """).encode('utf-8'))
#     
#daemon=(("""\
#   o         ,        ,
#    o       /(        )`
#     o      \ \___   / |
#            /- _  `-/  '
#           (/\/ \ \   /\
#           / /   | `    \
#           O O   ) /    |
#           `-^--'`<     '
#          (_.)  _  )   /
#           `.___/`    /
#             `-----' /
#<----.     __ / __   \
#<----|====O)))==) \) /====
#<----'    `--' `.__,' \
#             |        |
#              \       /
#        ______( (_  / \______
#      ,'  ,-----'   |        \
#      `--{__________)        \/
#
#
#    """).encode('utf-8'))
#    
print(("""\
'af':'afrikaans','sq':'albanian','am':'amharic','ar':'arabic','hy':'armenian','az':'azerbaijani',
'eu': 'basque','be':'belarusian','bn':'bengali','bs':'bosnian','bg':'bulgarian','ca':'catalan',
'ceb':'cebuano','ny':'chichewa','zh-cn':'chinese(simplified)','zh-tw':'chinese(traditional)',
'co':'corsican','hr':'croatian','cs':'czech','da':'danish','nl':'dutch','en':'english',
'eo':'esperanto','et':'estonian','tl':'filipino','fi':'finnish','fr':'french','fy':'frisian',
'gl':'galician','ka':'georgian','de':'german','el':'greek','gu': 'gujarati','ht':'haitian creole',
'ha':'hausa','haw':'hawaiian','iw':'hebrew','hi':'hindi','hmn':'hmong','hu':'hungarian',
'is':'icelandic','ig':'igbo','id':'indonesian','ga':'irish','it': 'italian','ja': 'japanese',
'jw':'javanese','kn':'kannada','kk':'kazakh','km':'khmer','ko':'korean','ku': 'kurdish (kurmanji)',
'ky':'kyrgyz','lo':'lao','la':'latin','lv':'latvian','lt':'lithuanian','lb':'luxembourgish',
'mk':'macedonian','mg':'malagasy','ms':'malay','ml':'malayalam','mt':'maltese','mi':'maori',
'mr':'marathi','mn':'mongolian',  'my':'myanmar (burmese)','ne':'nepali','no':'norwegian','ps':'pashto',
'fa':'persian','pl':'polish',     'pt':'portuguese','pa':'punjabi','ro':'romanian','ru': 'russian',
'sm':'samoan','gd':scots gaelic','sr':'serbian','st':'sesotho','sn':'shona','sd':'sindhi',
'si':'sinhala','sk':'slovak','sl':'slovenian','so':'somali','es':'spanish','su':'sundanese',    
'sw':swahili','sv':'swedish','tg':'tajik','ta':'tamil','te':'telugu','th': 'thai',
'tr':'turkish','uk':'ukrainian','ur':'urdu','uz':'uzbek','vi':'vietnamese','cy':'welsh',
'xh':'xhosa','yi':'yiddish','yo':'yoruba','zu':'zulu','fil':'Filipino','he':'Hebrew'
    
    """).encode('utf-8'))
    


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
ap.add_argument("-1", "--lang1", default="en",
	help="language to translate, default en")
ap.add_argument("-2", "--lang2", default="ar",
	help="language source, default ar")
		
args = vars(ap.parse_args())

if not os.path.exists('text'):
	os.makedirs('text')	
if not os.path.exists('translate'):
	os.makedirs('translate')	
translator =  Translator()
	
# make a list of all the available images 
images = os.listdir(args["image"]) 



for image in images:
	
	basess=os.path.basename(str(args["image"]+image))
	#print(basess)
	bases=os.path.splitext(basess)
	#print(bases)
	base=os.path.splitext((bases)[0])
	#print(str(base))
	
	# load the image
	image = cv2.imread(args["image"]+image)
	
	

	# load the input image, convert it from BGR to RGB channel ordering,
	# and use Tesseract to localize each area of text in the input image
	#image = cv2.imread(args["image"])
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	## alternative bgr to rgb
#	rgb = np.array(demosaicing_CFA_Bayer_bilinear(image, pattern))
	
	results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
	#print(str(results)+'results')
	


	# loop over each of the individual text localizations
	for i in range(0, len(results["text"])):
		# extract the bounding box coordinates of the text region from
		# the current result
		x = results["left"][i]
		y = results["top"][i]
		w = results["width"][i]
		h = results["height"][i]

		# extract the OCR text itself along with the confidence of the
		# text localization
		global text
		text = results["text"][i]
		conf = int(results["conf"][i])
######################################

		
		#filenameEN1 = open("text/filename"+str(args["lang1"])+".txt", "a")
		filenameEN1 = open("text/"+str(base)+str(args["lang1"])+"origin.txt", "a+")
		filenameEN1.write(str(text.strip())+" " )
		filenameEN1.close()
######################################			

		# filter out weak confidence text localizations
		if conf > args["min_conf"]:
			# display the confidence and text to our terminal
			#print("Confidence: {}".format(conf))
			#print("Text: {}".format(text))
			#print("")

				
			
			

			# strip out non-ASCII text so we can draw the text on the image
			# using OpenCV, then draw a bounding box around the text along
			# with the text itself
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
				1.2, (0, 0, 255), 3)
				
			
	
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)

################################# TRANSLATE #########################
# make a list of all the available images 
testos = os.listdir("text/") 



for testo in testos:
	
	basess=os.path.basename('text/'+testo)
	#print(basess)
	bases=os.path.splitext(basess)
	#print(bases)
	base=os.path.splitext((bases)[0])
	#print(str(base))
	
	with open('text/'+testo, 'r') as fp:
		for line in fp:
			print(line)
	
############### translate and write to file	
	
			
			#rigatransEN = translator.translate(line,src=str(args["lang2"]), dest=str(args["lang1"]))
			rigatransEN = translator.translate(line, dest=str(args["lang1"]))
			print("traduct origin: "+line)
			print("traduct destination: "+rigatransEN.text)
			print("             ")
			
			command = "flite -t "+"\""+(line)+"\""
			subprocess.Popen(command, shell=True)
			time.sleep(2)
		
			command = "flite -t "+"\""+(rigatransEN.text)+"\""
			subprocess.Popen(command, shell=True)
			time.sleep(2)
			
			command = "notify-send "+"\""+(line)+"\""
			subprocess.Popen(command, shell=True)
			time.sleep(2)
		
			command = "notify-send "+"\""+(rigatransEN.text)+"\""
			subprocess.Popen(command, shell=True)
			time.sleep(2)		
			
			#filenameEN = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+"_"+str(args["lang1"])+".csv"
			filenameEN = str(base)+"_"+str(args["lang1"])+".csv"
			filenameEN = open("translate"+"/"+filenameEN, "a+")
			rigatransENencod = rigatransEN.text.encode('utf8', 'replace')
			filenameEN.write(str(rigatransENencod.strip())+" " )
			filenameEN.close()	
			
command = "cowthink -f daemon 'CHECKMATE TO TRANSLATE IN PYTHON By Visi@n'"
subprocess.Popen(command, shell=True)
exit
