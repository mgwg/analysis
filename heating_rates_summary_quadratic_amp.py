# -*- coding: utf-8 -*-
"""
@author: Chip Lab

Plots data fitted in heating_rates_fitting.py and theory lines from modified
Tilman code bulkvisctrap_class.py.

Relies on data_class.py, library.py, and bulkvisctrap_class.py
"""
from data_class import Data
from library import *
from bulkvisctrap_class import BulkViscTrap, BulkViscTrapToTF
from itertools import chain
from matplotlib import cm
from scipy.optimize import curve_fit

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import os
import pickle

# data_folder = 'data\\heating'
data_folder = 'data//heating//reanalyzed'
pkl_filename = 'heating_rate_fit_reanalyzed_results.pkl'
pkl_file = os.path.join(data_folder, pkl_filename)

plotting = True
debugging_plots = False
plot_legend = True

scale_5kHz = 5

def quadratic(x, a, b):
	return a*x**2 + b

def linear(x, a, b):
	return a*x + b

colors = ["blue", "red", "green", "orange", 
		  "purple", "black", "pink", "brown"]

markers = ["o", "s", "^", "D", "h"]

############ LOAD DATA ############
try: # open pkl file if it's there
	with open(pkl_file, 'rb') as f:
		lr = pickle.load(f) # load all results in file
except FileNotFoundError: # if file not there then complain
	print("Can't find data results pickle file, you silly billy.")
	
filename_list = ["2024-04-05_C_UHfit.dat", "2024-03-26_B_UHfit.dat",
				 "2024-03-26_C_UHfit.dat"]
	
### select the data
lr = lr[lr.filename.isin(filename_list) == True]
amp_data = lr[((lr.filename != "2024-03-26_C_UHfit.dat") | (lr.freq != 5))]

############## PLOTTING ##############		
# change matplotlib options
plt.rcParams.update({"figure.figsize": [8,10]})
fig, axs = plt.subplots(2,1)
num = 500
font = {'size'   : 12}
plt.rc('font', **font)
legend_font_size = 10 # makes legend smaller, so plot is visible

### plot	
ax = axs[0]
ylabel = "Scaled Heating Rate $\partial_t E/E/A^2$ (Hz)"
ylabel = "Scaled Heating Rate $\partial_t E/E$ (Hz)"
xlabel = "Amplitude of Drive"
ax.set(ylabel=ylabel, xlabel=xlabel)

ax_res = axs[1]
ylabel = "Residual Heating Rate (Hz)"
ax_res.set(ylabel=ylabel, xlabel=xlabel)

# amp_data = amp_data.drop(amp_data.loc[amp_data.freq!=5].index)

for freq, color in zip(amp_data.freq.unique(), colors):
	df = amp_data.loc[amp_data.freq==freq]
	
 	# df = df.drop(df.loc[df.freq>0.4].index)
	
	xx = np.array(df["A"])
	yy = np.array(df["heating"])
	yerr = np.array(df["e_heating"]) 
	
	label = r"$f=${:.0f} kHz".format(freq)
	
	if df.freq.values[0] == 5:
		yy = scale_5kHz*yy
		yerr = scale_5kHz*yerr
		label = r"$f=${:.0f}kHz scaled by x{}".format(freq, scale_5kHz)
	
	popt, pcov = curve_fit(quadratic, xx, yy, sigma=yerr)
	perr = np.sqrt(np.diag(pcov))
	
	popt2, pcov2 = curve_fit(linear, xx, yy, sigma=yerr)
	perr2 = np.sqrt(np.diag(pcov2))
	
	ax.errorbar(xx, yy, yerr=yerr, fmt='o', capsize=2, color=color, label=label)
	xlist = np.linspace(0, max(xx), num)
	ax.plot(xlist, quadratic(xlist, *popt), '-', color=color)
	ax.plot(xlist, linear(xlist, *popt2), '--', color=color)
	
	ax_res.errorbar(xx, yy- quadratic(xx, *popt), yerr, fmt='o', capsize=2, 
				  color=color)
	ax_res.plot(xx,np.zeros(len(xx)), 'k--')

ax.legend()
plt.show()

