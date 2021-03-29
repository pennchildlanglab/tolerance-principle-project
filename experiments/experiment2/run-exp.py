#!/usr/bin/env python
'''
0164-empiricalyang-9noun-mf-rule-tophalf-child-exp
run by Jessie Burke (Summer 2016)


KSCHULER PLURAL MORPH METHOD
Kathryn Schuler: kathryn.schuler@gmail.com
Written on: 04/21/2015
Last Updated: 06/14/2016
-----------------

'''

"""

*********************************************************************************
SETUP EXPERIMENT PARAMTERS
*********************************************************************************
"""
EXP_INFO = {						# used to generate dialogue box to request info
	'subject':'', 					# subject ID (requests typing)
	'condition': ['5R4E-A', '5R4E-B', '3R6E-A', '3R6E-B']   	 	# list of possible conditions (user selects 1)
}
KEYS_QUIT = ['escape']				# keys that quit the experiment
KEYS_NEXT = ['space']				# keys that move on to the next trial
BREAK_AFTER = [17, 35, 53, 71]		# list of trials to take break after (exposure)
MOUSE_VISIBLE = True				# True or False, whether you want to see mouse
ISI = 0.150							# Seconds of silence between sentences
EXPOSURE = {
	'order': 'random',
	'reps': 1
	}
PRODUCTION = {
	'order': 'random',
	'reps': 1
	}

RATING = {
	'order': 'random',
	'reps': 1
	}

from psychopy import prefs
prefs.general['audioLib'] = ['pyo', 'pysoundcard']
prefs.general['audioDriver']= ['portaudio']


from psychopy import gui, core

# Request user input with dialog box
if not gui.DlgFromDict(EXP_INFO, order=['subject', 'condition']).OK:
	core.quit()
else :
	print "running subject: " + EXP_INFO['subject']
	print "on condition: "+ EXP_INFO['condition']


from psychopy import prefs, visual, info, event, data, sound, microphone
import datetime, os


"""
*********************************************************************************
SETUP VISUAL PARAMETERS
*********************************************************************************
"""
MONITOR = {
	'size': [1440, 900],	#pixel dimensions of the monitor
	'screen': 0,			#if more than 1 screen, which one to display on?
	'bg-color': 'white',	#what should the background color be?
	}

TEXT = {
	'pos': [0,300],				# [x,y] position of the instructions
	'height': 20,				# how big to make the font
	'wrap' : 800,				# how many pixels before words wrap to next line
	'color': 'gray',			# what color is the text
	'font': 'Arial'				# what font is the text
	}

PROG_BAR = {
	'pos': [0, -350],
	'height':20,
	'width':680,
	'color-outline': 'gray',
	'color-fill':'black',
	'fill-opacity':0.8,
	'level-pos':[400, -350]
	}

STIM_CARD = {
	'pos': [0, 0],
	'width': 550,
	'height':350,
	'color-line': 'gray',
	'img-size': [133, 100],
	'img-pos': [				# position of stimulus images
	(-150, 75),					# singular position (top left)
	(0, 75),					# plural n = 2 position
	(150, 75),					# plural n = 3 position
	(-150, -75),				# plural n = 4 position
	(0, -75),					# plural n = 5 position
	(150, -75)					# plural n = 6 position
	]
	}

RATING_SCALE = {
	'pos': [0, -260],
	'pos-yes': [375, -210],
	'pos-maybe': [-375, -210],
	'pos-no': [-232, -210]
	}
"""
*********************************************************************************
 The main experiment class, which contains all the experiments objects and methods.
*********************************************************************************
"""

class InconInputExperiment(object):
	def __init__(self):
		self.expClock = core.Clock()
		self.today = datetime.datetime.now()
		self.dataFile = EXP_INFO['subject']+'-'+self.today.strftime('%Y-%m-%d-%H%M%S')
		self.dataFolder = 'data/'+EXP_INFO['subject']+'-'+self.today.strftime('%Y-%m-%d-%H%M%S')
		self.win = visual.Window(units='pix', winType = 'pyglet', screen = MONITOR['screen'], color = MONITOR['bg-color'],
			size = MONITOR['size'], fullscr = False, allowGUI = True
		)
		self.mouse = event.Mouse(win = self.win)
		self.word = sound.Sound(value = 'sounds/gentif.wav', sampleRate = 44100)
		self.instructions = visual.TextStim(self.win,
			text = '', pos = TEXT['pos'], color = TEXT['color'], height = TEXT['height'],
			font = TEXT['font'], wrapWidth = TEXT['wrap']
		)
		self.level = visual.TextStim(self.win,
			text = '', pos = PROG_BAR['level-pos'], color = TEXT['color'], height = TEXT['height'],
			font = TEXT['font'], wrapWidth = TEXT['wrap']
		)
		self.card = visual.Rect(self.win, units = 'pix', pos = STIM_CARD['pos'], width = STIM_CARD['width'],
			height = STIM_CARD['height'], lineColor = STIM_CARD['color-line']
		)
		self.progressOutline = visual.Rect(self.win,
			units = 'pix', pos = PROG_BAR['pos'], width = PROG_BAR['width'], height = PROG_BAR['height']+3, lineColor = PROG_BAR['color-outline']
		)
		self.progressBar = visual.Rect(self.win,
			units = 'pix', pos = PROG_BAR['pos'], width = PROG_BAR['width'], height = PROG_BAR['height'], fillColor = PROG_BAR['color-fill'], opacity = PROG_BAR['fill-opacity']
		)
		self.girl2 = visual.ImageStim(self.win,
		 	image = 'images/girl2.png', pos = RATING_SCALE['pos-yes']
		)
		self.girl1 = visual.ImageStim(self.win,
		 	image = 'images/girl1.png', pos = RATING_SCALE['pos-maybe']
		)
		self.ratingScale = visual.RatingScale(self.win,
			pos = RATING_SCALE['pos'],  low=1, high=2, precision = 1, textColor = TEXT['color'],
			marker = 'triangle', size = 1, stretch = 1.0, lineColor = TEXT['color'],
			markerColor = 'blue', scale = None, acceptPreText = "?",
			respKeys = ['1', '2'], choices= ["1", "2"], markerStart = 0.5
		)
#		self.mic = microphone.AdvAudioCapture(stereo = False, chnl = 2)


	def setupExperiment(self):
		self.win.setMouseVisible(MOUSE_VISIBLE)
		self.makeDir(self.dataFolder)
		self.displayInstructions("INSTRUCTIONS")


	def runExperiment(self):
		self.exposure()
		self.productionTest()
		self.ratingTest()
		self.displayInstructions("THANKS! STICKER BREAK!")
		core.quit()


	def exposure(self):
		EXP_INFO['expPhase'] = 'exposure'
		whichLevel = 'level 1 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-exposure.xlsx', EXPOSURE['order'], EXPOSURE['reps'])
		self.writeData(self.dataFolder+'/'+self.dataFile+'-exposure.csv',
				['subject', 'condition', 'expPhase', 'trialNum', 'case', 'noun', 'num', 'det'], newLine = False)
		self.displayInstructions("LEVEL 1", isTrial = True)
		self.generateDisplay(whichLevel = whichLevel, isInstructional = True)
		event.waitKeys(keyList=KEYS_NEXT)
		for trial in self.trials :
			self.displayInstructions("LEVEL 1", isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.playSentence('gentif', trial.noun, trial.det)
			self.writeData(self.dataFolder+'/'+self.dataFile+'-exposure.csv',
				[EXP_INFO['subject'], EXP_INFO['condition'], EXP_INFO['expPhase'], self.trials.thisN, trial.case, trial.noun, trial.num, trial.det])
			event.waitKeys(keyList=KEYS_NEXT)
			if self.trials.thisN in BREAK_AFTER:
				self.displayInstructions("STICKER BREAK!!")
			if event.getKeys(['escape']): core.quit()
		self.displayInstructions("STICKER BREAK!!")


	def productionTest(self):
		EXP_INFO['expPhase'] = 'production'
		whichLevel = 'level 2 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-production.xlsx', PRODUCTION['order'], PRODUCTION['reps'])
		self.writeData(self.dataFolder+'/'+self.dataFile+'-production.csv',
				['subject', 'condition', 'expPhase', 'trialNum', 'det', 'plural', 'noun', 'singular', 'type'], False)
		self.displayInstructions("LEVEL 2", isTrial = True)
		self.generateDisplay(whichLevel = whichLevel, isInstructional = True)
		event.waitKeys(keyList=KEYS_NEXT)
		for trial in self.trials :
#			self.startRecording(self.trials.thisN, trial.noun, str(trial.plural))
			self.displayInstructions("LEVEL 2", isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.generateDisplay(trial.noun, trial.singular, whichLevel)
			self.playSentence('gentif', trial.noun, trial.det)
			event.waitKeys(keyList=KEYS_NEXT)
			self.displayInstructions("LEVEL 2: YOUR TURN!", isTrial = True)
			self.generateDisplay(trial.noun, trial.plural, whichLevel)
			self.writeData(self.dataFolder+'/'+self.dataFile+'-production.csv',
				[EXP_INFO['subject'], EXP_INFO['condition'], EXP_INFO['expPhase'], self.trials.thisN, trial.det, trial.plural, trial.noun, trial.singular, trial.type])
			event.waitKeys(keyList=KEYS_NEXT)
			self.win.flip()
#			self.stopRecording(waitbuffer = 0.5)
			if event.getKeys(['escape']): core.quit()
#		self.stopRecording(waitbuffer = 0.5, switchoffmic = True)
		self.displayInstructions("STICKER BREAK!!")




	def ratingTest(self):
		EXP_INFO['expPhase'] = 'rating'
		whichLevel = 'level 3 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-rating.xlsx', RATING['order'], RATING['reps'] )
		self.writeData(self.dataFolder+'/'+self.dataFile+'-rating.csv',
				['subject', 'condition', 'expPhase', 'trialNum', 'num', 'noun', 'error', 'marker1', 'marker2', 'whichCorrect', 'rating', 'RT'], False)
		while self.ratingScale.noResponse:
			self.displayInstructions("LEVEL 3", isTrial = True)
			self.ratingScale.draw()
			self.drawGirls()
			# self.checkno.draw()
			self.generateDisplay(whichLevel = whichLevel, isInstructional = True)
		self.ratingScale.reset()

		for trial in self.trials:
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.displayInstructions("LEVEL 3", isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.drawGirls(self.girl1)
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.playSentence('gentif', trial.noun, trial.marker1)
			core.wait(1.0)
			self.drawGirls(self.girl2)
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.playSentence('gentif', trial.noun, trial.marker2)
			while self.ratingScale.noResponse:
				self.ratingScale.draw()
				self.drawGirls()
				# self.checkmaybe.draw()
				# self.checkno.draw()
				self.generateDisplay(trial.noun, trial.num, whichLevel)
			rating, decisionTime = self.getRatingData(self.trials, self.ratingScale.getRating(), self.ratingScale.getRT())
			self.writeData(self.dataFolder+'/'+self.dataFile+'-rating.csv',
				[EXP_INFO['subject'], EXP_INFO['condition'], EXP_INFO['expPhase'], self.trials.thisN, trial.num, trial.noun, trial.error, trial.marker1, trial.marker2, trial.whichcorrect, rating, decisionTime])
			self.ratingScale.reset()
			if event.getKeys(['escape']): core.quit()


	def makeDir(self, thisDir):
		if not os.path.exists(thisDir):
			os.makedirs(thisDir)

	def loadTrials(self, thisFile, thisMethod = 'random', numReps=1):
		self.conditionsFile = data.importConditions(thisFile)
		self.trials = data.TrialHandler(self.conditionsFile,
			method = thisMethod, nReps = numReps, extraInfo = EXP_INFO)


	def generateDisplay(self, thisNoun = None, thisNum = None, whichLevel = 0, isInstructional = False):
		self.card.draw()
		if isInstructional == False:
			self.drawTrialImages(thisNoun, thisNum)
		self.drawProgressBar(whichLevel)
		self.win.flip()

	def drawTrialImages(self, thisNoun, thisNum):
		self.images = []
		self.numImages = range(1, (thisNum+1))
		for n in range(1, (thisNum+1)) :
			thisImage = visual.ImageStim(self.win, units = 'pix', size = STIM_CARD['img-size'],
				pos = STIM_CARD['img-pos'][n-1], image='images/'+thisNoun+'.png')
			self.images.append(thisImage)
		for img in self.images :
			img.draw()

	def displayInstructions(self, whichText = '', isTrial = False):
		self.instructions.setText(whichText)
		self.instructions.draw()
		if isTrial == False:
			self.win.flip()
			event.waitKeys(keyList=KEYS_NEXT)
			if event.getKeys(['escape']): core.quit()
		else: pass

	def playSentence(self, thisVerb, thisNoun, thisDet, thisISI = ISI):
		core.wait(0.5)
		self.sentence = [thisVerb, thisNoun, thisDet]
		print self.sentence
		for word in self.sentence :
			self.playSound(word)
			core.wait(thisISI)

	def playSound(self, thisWord):
		if thisWord != None :
			self.word.setSound('sounds/'+thisWord+'.wav')
			self.word.play()
			core.wait(self.word.getDuration())
		else :
			pass

	def drawGirls(self, whoTalking = None):
		girls = [self.girl1, self.girl2]
		for girl in girls :
			if girl == whoTalking :
				girl.setOpacity(1.0)
			else:
				girl.setOpacity(0.25)
			girl.draw()

	def drawProgressBar(self, whichLevel = '0'):
		self.progressOutline.draw()
		self.progressBar.draw()
		self.level.setText(whichLevel)
		self.level.draw()

	def changeProgressBar(self, thisTrial, numTrials):
		pixels_per_trial = PROG_BAR['width']/(numTrials)
		pixels_this_trial = (thisTrial+1)*pixels_per_trial
		width = PROG_BAR['width'] - pixels_this_trial
		newxpos = ((-PROG_BAR['width']/2) + (PROG_BAR['width']/2 - pixels_this_trial))/2
		self.progressBar.setWidth(width)
		self.progressBar.setPos([newxpos, PROG_BAR['pos'][1]])

#	def startRecording(self, thisTrial, thisNoun, thisNum):
#		self.mic.record(sec = 30,
#			filename = self.dataFolder+"/trial"+str(thisTrial)+
#			"-"+thisNoun+"-plural"+thisNum+".wav")
#
#	def stopRecording(self, waitbuffer = 0.5, switchoffmic = False):
#		self.mic.recorder.stop()
#		self.mic.stop()
#		self.mic.reset()
#		core.wait(waitbuffer)
#		if switchoffmic == True:
#			self.displayInstructions("please wait... turning off mic...will advance automatically when finished...", isTrial = True)
#			self.win.flip()
#			microphone.switchOff()
#			core.wait(5)

	def getRatingData(self, trialHandler, rating, decisionTime):
		trialHandler.addData('rating', rating)
		trialHandler.addData('RT', decisionTime)

		return rating, decisionTime

	def writeData(self, thisData, theDataList, newLine = True):
		dataFile = open(thisData, 'a')
		if newLine :
			makeNewLine = '\n'
			dataFile.write(makeNewLine)
		for data in theDataList:
			data = str(data)
			dataContent = data + ','
			dataFile.write(dataContent)
		dataFile.close()

# Turn on the microphone
# psychopy likes it if you do this before you start the experiment
#microphone.switchOn(sampleRate = 44100)
#core.wait(5)


# start experiment
exp = InconInputExperiment()
exp.setupExperiment()
exp.runExperiment()
