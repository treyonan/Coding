# put this file in C:\Program Files\Inductive Automation\Ignition\user-lib\pylib

import system

#--------------------------------------------------------------------------#

def dataset(**kwargs):
	
	for key, value in kwargs.items():
	
		if key == "dataset":
			dataset = value				
			rawHeaders = dataset.getColumnNames()
			headers = []
			for i in rawHeaders:
				headers.append(str(i))
			pyDataSet = toPyDataSet(dataset=value)
			dataset = toDataSet(pyDataSet=pyDataSet, headers=headers)
			
	return dataset
				
#--------------------------------------------------------------------------#

def toPyDataSet(**kwargs):

	for key, value in kwargs.items():
	
		if key == "dataset":
			dataset = value
			pyDataSet = system.dataset.toPyDataSet(dataset)
			
	return pyDataSet
	
#--------------------------------------------------------------------------#

def toDataSet(**kwargs):

	for key, value in kwargs.items():
	
		if key == "headers":
			headers = value			
		elif key == "data":
			data = value
		elif key == "pyDataSet":
			pyDataSet = value
			rawHeaders = pyDataSet.getColumnNames()
			headers = []
			for i in rawHeaders:
				headers.append(str(i))			
			data = []
			for row in pyDataSet:				
				data.append(row)
	
	dataset = system.dataset.toDataSet(headers, data)
	return dataset
	
#--------------------------------------------------------------------------#

