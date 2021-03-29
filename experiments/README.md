# Experiments

The `experiments` directory contains the stimuli and code for running the experiments. In each experiment folder, you'll find:

- `conditions` directory - the condition files used to run the experiment
- `images` directory - the image stims used by the experiment
- `sounds` directory - the sounds used by the experiment
- `run-exp.py` is the program that runs the experiment 

The `instructions-text.docx` file includes the instructions we provide for children (and adult controls). This document includes some notes (as comments) about why specific choices were made in the instructions.

A few other notes:
- To run the experiment, you'll need install [PsychoPy](https://www.psychopy.org/). PsychoPy comes with all past versions, so you can run an experiment from any former version of the software. This experiment was run in version 1.85.4. 
- You'll run the experiment from PsychoPy's Coder View. (Open the .py file, then hit the green run button); You'll be prompted to enter the subjectID and select the condition.
- The image stimuli and visual elements were articulated in exact pixels, which worked best for the computers that ran this study in the lab. If you have a newer macbook/retina display you likely have a lot more pixels, so the text and images might look really small or seem slightly off to you. You can adjust the size of things in the code section labeled SETUP VISUAL PARAMETERS.


You can add the following lines to the `run-exp.py` file to force psychopy to open the experiment in this version.

```
import psychopy
psychopy.useVersion('1.85.4')
```