# -*- coding: utf-8 -*-
"""
2023-10-05
@author: Chip Lab

Plotting functions for general analysis scripts 
"""

from analysisfunctions import * # includes numpy and constants
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import scipy.optimize as curve_fit
from tabulate import tabulate # pip install tabulate
from data import *
import pandas as pd

# All of the functions you can fit to 

 

def fitting_type(filename,names=['freq','sum95'], avg=False, datatype='raw', fittype='Sin', guess=None):
	if avg is True:
		fitdata = avgdata_data(filename, names)
	else:
		if datatype == 'raw':
			fitdata = data(filename,  names)
		elif datatype == 'exclude':
			fitdata = data_exclude(filename, names)
		elif datatype == 'exclude multiple points':
			fitdata = data_exclude_points(filename, names)
		else:
			fitdata = 'nothing'
# 	print(fitdata)
# 	print(fitdata)
	if fittype == 'Cos':
		if guess is None:	
			guess = [-0.2, 0, 10, 202]
		popt, pcov = curve_fit.curve_fit(Cos, fitdata[2], fitdata[3],p0=guess)
		ym = Cos(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Cos(fitdata[2],*popt)
	if fittype == 'Sin':
		if guess is None:	
			guess = [(max(fitdata[3])-min(fitdata[3])),0.05,-2,21]
		popt, pcov = curve_fit.curve_fit(Sin, fitdata[2], fitdata[3],p0=guess)
		ym = Sin(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Sin(fitdata[2],*popt)
	if fittype == 'Gaussian':
		if guess is None:	
			guess = [-(max(fitdata[3])-min(fitdata[3])),fitdata[2][fitdata[3].argmin()],0.04,np.mean(fitdata[3])]
		popt, pcov = curve_fit.curve_fit(Gaussian, fitdata[2], fitdata[3],p0=guess)
		ym = Gaussian(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Gaussian(fitdata[2],*popt)
	if fittype == 'Lorentzian':
		if guess is None:
			guess = [(max(fitdata[3])-(sorted(set(fitdata[3]))[2])), 1, fitdata[2][fitdata[3].argmin()], 0.04, np.mean(fitdata[3])]
		popt, pcov = curve_fit.curve_fit(Lorentzian, fitdata[2], fitdata[3],p0=guess)
		ym = Lorentzian(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Lorentzian(fitdata[2],*popt)
	if fittype == 'Sinc':
		if guess is None:
			guess = [(max(fitdata[3])-(sorted(set(fitdata[3]))[2])),(sorted(set(fitdata[2]))[1]+sorted(set(fitdata[2]))[-1])/2, (sorted(set(fitdata[2]))[1]-sorted(set(fitdata[2]))[-1])/2, np.mean(fitdata[3])]
		popt, pcov = curve_fit.curve_fit(Sinc, fitdata[2], fitdata[3],p0=guess)
		ym = Sinc(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Sinc(fitdata[2],*popt)	
	if fittype == 'Sinc2':
		if guess is None:
			guess = [(max(fitdata[3])-(sorted(set(fitdata[3]))[0])),(sorted(set(fitdata[3]))[1]+sorted(set(fitdata[3]))[0]), 4, np.mean(fitdata[3])]
		popt, pcov = curve_fit.curve_fit(Sinc2, fitdata[2], fitdata[3],p0=guess)
		ym = Sinc2(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Sinc2(fitdata[2],*popt)
	if fittype == 'TrapFreq':
		if guess is None:
			guess = [10000, 0.05, 20  ,-2 , 100, -0.1]
		popt, pcov = curve_fit.curve_fit(TrapFreq, fitdata[2], fitdata[3],p0=guess)
		ym = TrapFreq(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - TrapFreq(fitdata[2],*popt)
	if fittype == 'TrapFreq2':
		if guess is None:
			guess = [10000, 0.05, 20  ,-2 , 100]
		popt, pcov = curve_fit.curve_fit(TrapFreq2, fitdata[2], fitdata[3],p0=guess)
		ym = TrapFreq2(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - TrapFreq2(fitdata[2],*popt)
	if fittype == 'RabiFreq':
		if guess is None:
			guess = [1,1,1,0]
		popt, pcov = curve_fit.curve_fit(RabiFreq, fitdata[2], fitdata[3],p0=guess)
		ym = RabiFreq(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - RabiFreq(fitdata[2],*popt)
	if fittype == 'Parabola':
		if guess is None:
			guess = [-3000, 44.82, 3000]
		popt, pcov = curve_fit.curve_fit(Parabola, fitdata[2], fitdata[3],p0=guess)
		ym = Parabola(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Parabola(fitdata[2],*popt)
	if fittype == 'Linear':
		if guess is None:
			guess = [(max(fitdata[3])-min(fitdata[3]))/(max(fitdata[2])-min(fitdata[2])),fitdata[2][fitdata[3].argmin()]]
		popt, pcov = curve_fit.curve_fit(Linear, fitdata[2], fitdata[3],p0=guess)
		ym = Linear(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Linear(fitdata[2],*popt)
	if fittype == 'Exponential':
		if guess is None:
			guess = [max(fitdata[3])-min(fitdata[3]), 1]
		popt, pcov = curve_fit.curve_fit(Exponential, fitdata[2], fitdata[3],p0=guess)
		ym = Exponential(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - Exponential(fitdata[2],*popt)
	if fittype == 'RabiLine':
		if guess is None:
			guess = [1, 1, 1, 1, 1, 1, 1, 0]
		popt, pcov = curve_fit.curve_fit(RabiLine, fitdata[2], fitdata[3],p0=guess)
		ym = RabiLine(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - RabiLine(fitdata[2],*popt)
	if fittype == 'ErfcFit':
		if guess is None:
			guess = [1, 1, 1, 0]
		popt, pcov = curve_fit.curve_fit(ErfcFit, fitdata[2], fitdata[3],p0=guess)
		ym = ErfcFit(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - ErfcFit(fitdata[2],*popt)
	if fittype == 'SinplusCos':
		if guess is None:
			guess = [1, 1, 1, 0]
		popt, pcov = curve_fit.curve_fit(SinplusCos, fitdata[2], fitdata[3],p0=guess)
		ym = SinplusCos(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),*popt)
		residuals = fitdata[3] - SinplusCos(fitdata[2],*popt)
# 	else:
# 		popt, pcov, ym, residuals = [0,0,0,0]
	
	return popt, pcov, ym, residuals

#plotting the data and fitting to chosen function 

def plots(filename, datatype='raw', names=['freq','sum95'], avg=False, guess=None, fittype='Sin'):
	"""
	Inputs: filename, header names - names=['',''], guess for fit (None is automated guess) [A, omega, p, C], fittype (Sin, Cos, Gaussian, Lorentzian, Sinc, Sinc2, TrapFreq, TrapFreq2, RabiFreq, Parabola, Linear, Exponential, RabiLine, ErfcFit, SinplusCos) 
	
	Returns: data plotted with chosen fit
	"""
	fig1 = plt.figure(0)
	if avg is True:
		fitdata = avgdata_data(filename, names)
	else:
		if datatype == 'raw':
			fitdata = data(filename, names, datatype=datatype)
		if datatype == 'exclude':
			fitdata = data_exclude(filename, names)
		if datatype == 'exclude multiple points':
			fitdata = data_exclude_points(filename, names)
# 	print(fitdata)
	plt.title(f"{fittype} fit for {filename}")
	xlabel = f"{fitdata[0]}"
	ylabel = f"{fitdata[1]}"
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.plot(fitdata[2], fitdata[3], 'go')
	
	popt, pcov, ym, residuals = fitting_type(filename, names, avg, fittype=fittype, guess=guess)
	
	errors = np.sqrt(np.diag(pcov))
	freq = 0.01
	period = 1/freq
	delay = popt[1] % (3.141592654) /freq
	values = list([*popt, freq, period, delay])
	#errors = np.concatenate((errors, [errors[1]/2/3.14, period * errors[1]/popt[1], delay * errors[2]/popt[2]]))
	print(tabulate([['Values', *values], ['Errors', *errors]], headers=['Amplitude','phase','offset', 'freq', 'period', 'delay']))
	
	plt.plot(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),ym)
	
	return fig1


# residuals 

def residuals(filename, datatype, names=['delay time', 'sum95'], guess=None, fittype='Sin'):
	"""
	Inputs: filename, header names - names=['','']
	
	Returns: residuals plot 
	"""
	if datatype == 'raw':
		fitdata = data(filename, names)
	if datatype == 'exclude':
		fitdata = data_exclude(filename, names)
	if datatype == 'exclude multiple points':
		fitdata = data_exclude_points(filename, names)
	xlabel = f"{fitdata[0]}"
	ylabel = f"{fitdata[1]}"
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

#really residuals from fitting_type not ym but it is throwing a fit if i call it residuals for some reason lmao 

	ym = fitting_type(filename, names, fittype, guess)[3]
	

	fig2 = plt.figure(1)
	plt.plot(fitdata[2],fitdata[3]*0,'-')
	plt.plot(fitdata[2], ym, 'g+')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel +" Residuals")
	return fig2


def avgdata_data(filename, names, fittype='Gaussian', guess=None):
	fitdata = data(filename, names, fittype)

	namex = data(filename, names)[0] 
	namey = data(filename, names)[1] #choosing x , y columns from .dat 
	x = data(filename, names)[2]
	y = data(filename, names)[3]
	data2 = pd.DataFrame({namex: x, namey: y}) 
    
	avgdata = data2.groupby([namex])[namey].mean()
	
	return avgdata


def avgdata(filename, names, guess=None, fittype='Gaussian'):
	fig1 = plt.figure(0)
	fitdata = data(filename, names, fittype)
	plt.title(f"{fittype} fit for Averaged Data in {filename}")
	xlabel = f"{fitdata[0]}"
	ylabel = f"{fitdata[1]}"
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
    
	namex = data(filename, names)[0] 
	namey = data(filename, names)[1] #choosing x , y columns from .dat 
	x = data(filename, names)[2]
	y = data(filename, names)[3]
	data2 = pd.DataFrame({namex: x, namey: y}) 
    
	avgdata = data2.groupby([namex])[namey].mean()


	avgdata.plot( marker = '.', linestyle = 'none')
    
	popt, pcov, ym, residuals = fitting_type(filename, names, fittype=fittype, guess=guess)
	
	errors = np.sqrt(np.diag(pcov))
    # freq = 0.01
# 	period = 1/freq
# 	delay = popt[1] % (3.141592654) /freq
	values = list([*popt])
	#errors = np.concatenate((errors, [errors[1]/2/3.14, period * errors[1]/popt[1], delay * errors[2]/popt[2]]))
	print(tabulate([['Values', *values], ['Errors', *errors]], headers=['Amplitude','phase','offset', 'freq', 'period', 'delay']))
	
	plt.plot(np.linspace(max(fitdata[2]),min(fitdata[2]),num=200),ym)
	
	return fig1
            