# Physics with tagged protons: exclusive di-lepton production for the 2020 CMSDAS

General information on CMSDAS 2020:
* [CMSDAS2020 main page](https://indico.cern.ch/e/cmsvdas2020)
* [All long exercises](https://indico.cern.ch/event/886923/page/20498-long-exercises-and-descriptions)
* [Exercise Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolCERN2020TaggedProtonsLongExercise)

**Recommended:**: watch [here](https://videos.cern.ch/record/2730189) the short exercise introduction video.

## Recommended way to run the exercise (SWAN)
[![SWAN](https://swanserver.web.cern.ch/swanserver/images/badge_swan_white_150.png)](https://cern.ch/swanserver/cgi-bin/go/?projurl=https://github.com/CMSDAS/pps-long-exercise.git)

To run the notebooks with regular CERN resources:
* Open a [SWAN session](https://swan.cern.ch) (the defaults are good, as of writing this pick software stack 97a and make sure to use Python3)
* In the SWAN session, click on the item on the right-hand side that says "Download Project from git" ![Download Project from git](img/download_project_trim.png)
* Copy-paste https://github.com/CMSDAS/pps-long-exercise.git

## Table of content

1. [Optimization notebook](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Event-selection-optimization.ipynb) - here we will optimize event selection using a simple figure of merit to decide which cut is optimal

2. [Proton recontsruction](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Proton-Reconstruction.ipynb) - In this notebook, we will select events with protons, tagged by the forward proton spectrometer (PPS), and practice how to correlate the information obtained by PPS with the event measured in the central detector.

3. [Clasification notebook](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Classification-Training.ipynb) - here we will prepare a simple setup to train a multivariate discriminator to separate the signal from the background.

4. [Background estimation + statistical analysis notebook (CBA)](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Background-Estimation.ipynb) - here we will use the ABCD method to estimate the background rates in the signal region and extract sensitivity using the Cut-and-Count approach. 

5. [Background estimation + statistical analysis notebook (MVA)](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Background-Estimation_shape.ipynb) - here we will use the ABCD method to estimate the background rates in the signal region and use the BDT output from [Clasification notebook](https://nbviewer.jupyter.org/github/cmsdas/pps-long-exercise/blob/master/Classification-Training.ipynb) in shape analysis. 


