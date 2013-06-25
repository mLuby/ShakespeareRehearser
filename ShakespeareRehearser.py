
# Set URL here:
home = "http://shakespeare.mit.edu/"

# Get the HTML.
import urllib
page = urllib.urlopen(home).read()

# Get plays stored as [(PLAY NAME,www.page.com)]

html = page
urlj = 0
plays = []
while True:
	urli = html.find('a href=\"',urlj)
	urlj = html.find('\">',urli)
	anchori = urlj
	anchorj = html.find('<',anchori)
	if urli == -1:
		break
	url = home+html[urli+8:urlj].replace('index','full')
	anchor = html[anchori+2:anchorj].replace('\n','')
	# switch them if wrong
	plays.append((anchor,url))

# list the plays
i = 1
while i < len(plays):
	print str(i)+'. '+plays[i][0]
	i = i + 1

# ask for user to enter an int to choose a play.
selection = int(raw_input('Enter a number to select a play:'))

# Clear screen
import os
os.system('cls' if os.name=='nt' else 'clear')

# Announce user character choice.
print 'You chose '+plays[selection][0]+'.'

# Get the HTML.
play = plays[selection][1]

page = urllib.urlopen(play).read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(page)

# Get characters stored as <b>CHARACTER NAME</b>
characters = []
unsortedCharacters = soup.findAll('b')
# Strip tags to leave strings
for character in unsortedCharacters:
	characters.append(character.string)
# Remove duplicates.
characters = list(set(characters))

# Display ordered list of characters.
i = 1
for character in characters:
	print str(i)+'. '+character
	i = i + 1
# ask for user to enter an int to choose a character.
selection = raw_input('Enter a number to select a character:')
# turn selection into a 0-based index int
selection = int(selection) - 1

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

# Announce user character choice.
print 'You chose '+characters[selection]+'. Press enter to continue:'

# Get character's lines.
html = page
i=0
j=0
act = ''
scene = ''

from  AppKit import NSSpeechSynthesizer
import time
import sys
# if len(sys.argv) < 2:
text = raw_input('> ')
# else:
	# text = sys.argv[1]
nssp = NSSpeechSynthesizer
ve = nssp.alloc().init()
voices = ["com.apple.speech.synthesis.voice.Alex","com.apple.speech.synthesis.voice.Vicki","com.apple.speech.synthesis.voice.Victoria","com.apple.speech.synthesis.voice.Zarvox" ]
# for voice in nssp.availableVoices():
ve.setVoice_(voices[0])
def speak(txt):
	ve.startSpeakingString_(txt)
	while ve.isSpeaking():
	  time.sleep(1)
	return txt

# from os import system
# def speak(txt):
# 	system('say'+txt)
# 	return txt

while True:
	oldi = i
	# get indices around your speech
	i = html.find('<b>'+characters[selection]+'</b>',j)
	j = html.find('</blockquote>',i)

	# get indices around previous speech
	previ = html.rfind('<b>', oldi, i)
	prevj = html.find('</blockquote>', previ, i)

	# end the loop before printing if reached EOF
	if i == -1 or j == -1:
		break

	# prev speaker
	prevSpeech = ''
	for string in BeautifulSoup(html[previ:prevj].replace('<blockquote>',':')).stripped_strings:
		line = str(repr(string))
		# join lines and remove u for unicode 
		prevSpeech = prevSpeech + line[1:len(line)]

	# remove line breaks and quotes
	prevSpeech = prevSpeech.replace('\'\'',' ')
	# remove 'exeunt'
	prevSpeech = prevSpeech.replace('Exeunt','')
	# remove double quotation marks
	prevSpeech = prevSpeech.replace('"','')
	print prevSpeech
	speak(prevSpeech)

	# your character
	for string in BeautifulSoup(html[i:j]).stripped_strings:
	    print repr(string)[1:]

	raw_input('Press enter to continue...')
