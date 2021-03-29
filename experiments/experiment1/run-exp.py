#!/usr/bin/env python
'''
KSCHULER PLURAL MORPH METHOD
Kathryn Schuler: kathryn.schuler@gmail.com
Date: 04/21/2015
Updated: 07/10/2015
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



from psychopy import gui

# Request user input with dialog box
if not gui.DlgFromDict(EXP_INFO, order=['subject', 'condition']).OK:
		core.quit()

from psychopy import visual, core, info, event, data, sound, microphone
import datetime, os


"""





*********************************************************************************
SETUP ONSCREEN INSTRUCTIONS
*********************************************************************************
"""
#These appear before for the exposure phase
EXPOSE_INSTRUCT = '''
This game is going to teach you a new language called Silly Speak.
You will see a picture and hear a sentences that describes that picture in silly speak.
All you have to do for this part of the game is repeat the sentence.
Press spacebar when you are ready to continue.
'''
#These appear on every exposure trial
EXPOSE_TRIAL_INSTRUCT = '''
Repeat the sentence aloud.  Press spacebar to continue.
'''
#These appear when the subjects is given a break (trials selected in BREAK_AFTER)
BREAK_INSTRUCT = '''
Now we will take a short break.  Press spacebar when you are ready to continue.
'''
#These appear before the production phase
PRODUCE_INSTRUCT = '''
Great Job!  The next part of the game is a little bit different.
For this part, you will see a picture and hear the sentence that describes it.  
Then, you will see a second picture and be asked to describe the picture in silly speak!
Just try your best! 
'''
#These appear during the singular portion of every production trial
PRODUCE_TRIAL_INSTRUCT_SINGULAR = '''
If the sentence for this picture is...
Repeat the sentence aloud. Press spacebar to continue.
'''
#These appear during the plural portion of every production trial
PRODUCE_TRIAL_INSTRUCT_PLURAL = '''
What is the sentence for this picture?
Say your answer aloud. Press spacebar to continue.
'''
#These appear before the rating phase
RATING_INSTRUCT = '''
Great Job!  You are almost done.  For the last part of the game, you will see
a picture and hear a sentence that describes it.  Your job is to judge whether the sentence matches the picture!  Just try your best! 
'''
#These appear during every rating trial
RATING_TRIAL_INSTRUCT = '''
How well did the sentence match the picture?
'''
#These appear at the end of the experiment.
END_INSTRUCT = '''
Thanks for playing! The experiment is over.
'''
"""
*********************************************************************************
SETUP VISUAL PARAMETERS
*********************************************************************************
"""
MONITOR = {
	'size': [1440, 900],	#pixel dimensions of the monitor
	'screen': 1,			#if more than 1 screen, which one to display on?
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
	'pos': [0, -250],
	'pos-stars': [0, -200]
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
		self.dataFolder = 'data/'+EXP_INFO['subject']+'-'+self.today.strftime('%Y-%m-%d')
		self.win = visual.Window(units='pix', winType = 'pyglet', screen = MONITOR['screen'], color = MONITOR['bg-color'],
			size = MONITOR['size'], fullscr = True, allowGUI = True
		)
		self.word = sound.Sound(value = 'sounds/gentif.wav')
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
		self.ratingScale = visual.RatingScale(self.win, 
			pos = RATING_SCALE['pos'],  low=1, high=5, precision = 1, textColor = TEXT['color'],
			marker = 'triangle', size = 0.60, stretch = 1.0, lineColor = TEXT['color'],
			markerColor = 'blue', scale = None
			)
		self.stars = visual.ImageStim(self.win,
			image = 'images/stars.jpeg', pos = RATING_SCALE['pos-stars']
		)
	
	def setupExperiment(self):
		self.win.setMouseVisible(MOUSE_VISIBLE)
		self.makeDir(self.dataFolder)
        print 'made directory'
		
	def runExperiment(self):
		self.exposure()
		self.productionTest()
		self.ratingTest()
		self.displayInstructions(END_INSTRUCT)
		
	def exposure(self):
		EXP_INFO['expPhase'] = 'exposure'
		whichLevel = 'level 1 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-exposure.xlsx', EXPOSURE['order'], EXPOSURE['reps'])
		self.displayInstructions(EXPOSE_INSTRUCT)
		for trial in self.trials :
			self.displayInstructions(EXPOSE_TRIAL_INSTRUCT, isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.playSentence('gentif', trial.noun, trial.det)
			self.trials.saveAsWideText(self.dataFolder+'/'+self.dataFile+'-exposure.csv', delim=',', appendFile = True)
			event.waitKeys(keyList=KEYS_NEXT)
			if self.trials.thisN in BREAK_AFTER:
				self.displayInstructions(BREAK_INSTRUCT)

			
	def productionTest(self):
		EXP_INFO['expPhase'] = 'production'
		whichLevel = 'level 2 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-production.xlsx', PRODUCTION['order'], PRODUCTION['reps'])
		self.displayInstructions(PRODUCE_INSTRUCT)
		for trial in self.trials :
			self.displayInstructions(PRODUCE_TRIAL_INSTRUCT_SINGULAR, isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.generateDisplay(trial.noun, trial.singular, whichLevel)
			self.playSentence('gentif', trial.noun, trial.det)
			event.waitKeys(keyList=KEYS_NEXT)
			self.displayInstructions(PRODUCE_TRIAL_INSTRUCT_PLURAL, isTrial = True)
			self.generateDisplay(trial.noun, trial.plural, whichLevel)
			self.trials.saveAsWideText(self.dataFolder+'/'+self.dataFile+'-production.csv', delim=',', appendFile = True)
			event.waitKeys(keyList=KEYS_NEXT)
			
	def ratingTest(self):
		EXP_INFO['expPhase'] = 'rating'
		whichLevel = 'level 3 of 3'
		self.loadTrials('conditions/'+EXP_INFO['condition']+'-rating.xlsx', 'random', 1)
		self.displayInstructions(RATING_INSTRUCT)
		for trial in self.trials:
			self.displayInstructions(RATING_TRIAL_INSTRUCT, isTrial = True)
			self.changeProgressBar(self.trials.thisN, self.trials.nTotal)
			self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.playSentence('gentif', trial.noun, trial.det)
			while self.ratingScale.noResponse:
				self.ratingScale.draw()
				self.stars.draw()
				self.generateDisplay(trial.noun, trial.num, whichLevel)
			self.getRatingData(self.trials, self.ratingScale.getRating(), self.ratingScale.getRT())
			self.trials.saveAsWideText(self.dataFolder+'/'+self.dataFile+'-rating.csv', delim=',', appendFile = False)
			self.ratingScale.reset()

	
	def makeDir(self, thisDir):
		if not os.path.exists(thisDir):
			os.makedirs(thisDir)
   		
	def loadTrials(self, thisFile, thisMethod = 'random', numReps=1):
		self.conditionsFile = data.importConditions(thisFile)
		self.trials = data.TrialHandler(self.conditionsFile, 
			method = thisMethod, nReps = numReps, extraInfo = EXP_INFO)
		
	
	def generateDisplay(self, thisNoun, thisNum, whichLevel):
		self.card.draw()
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
	
	def startRecording(self, thisTrial, thisNoun, thisNum):
		self.mic.record(sec = 5, 
			filename = self.dataFolder+"/trial"+str(thisTrial)+
			"-"+thisNoun+"-plural"+thisNum+".wav")
	
	def stopRecording(self):
		self.mic.stop()
	
	def getRatingData(self, trialHandler, rating, decisionTime):
		trialHandler.addData('rating', rating)
		trialHandler.addData('RT', decisionTime)


		
# start experiment
exp = InconInputExperiment()
exp.setupExperiment()
exp.runExperiment()