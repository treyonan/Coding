'''

'''

from datetime import datetime, timedelta
from java.lang import Exception

db = 'mes_core'


def calcFinishTime(parentPath, db=db):

	query = """
		select r.ID as 'ID', wo.WordOrder as 'WorkOrder', r.RunStartTime as 'StartTime', sch.ScheduleFinishDateTime as 'FinishTime',
		sch.Quantity as 'Quantity' from Run r 
		left join Schedule sch
		on r.ScheduleID = sch.ID
		left join WorkOrder wo
		on sch.WorkOrderID = wo.ID
		where r.ID = ?
		and r.Closed = 0
	"""
	
	runID = system.tag.readBlocking([parentPath+'/OEE/RunID'])[0].value
	
	if runID > -1:
		
		runData = system.db.runPrepQuery(query, [runID], db)
		# get order quantity from run table
		
		for row in  runData:
			quantity = row['Quantity']
			
		# calculate how many parts remain to produce and grab the current production rate
		goodParts = system.tag.readBlocking([parentPath+'/OEE/Good Count'])[0].value
		remainingParts = quantity - goodParts
		productionRate = system.tag.readBlocking([parentPath+'/OEE/Production Rate'])[0].value
		
		#get current time and hours remaining in order
		
		currentTime = datetime.now().replace(microsecond=0)
		
		if productionRate > 0:
			pass
		else:
			productionRate = 1
			
		hoursRemaining = remainingParts/productionRate
		
		#calc estimated finish time by adding remaining hours to current time
		finishTime = currentTime + timedelta(hours=hoursRemaining)
		return finishTime.replace(microseconds=0)
		
	else:
		return 'No Order'
		
		
		
def updateRun(runID, db=db): # gets called anytime you calculate OEE
	try:		
		# build a query to retrieve lineID and linePath
		
		lineQuery = """
			Select l.ID as 'Line ID', CONCAT('mes_core',e.NAME,'/',s.NAME,'/',a.NAME,'/',l.NAME,'/Line') as 'Line Path' 
			from run r
			left join schedule sch
			on r.ScheduleID = sch.ID
			left join line l
			on sch.LineID = l.ID
			left join area a
			on l.parentID = a.ID
			left join site s
			on a.parentID = s.ID
			left join enterprise e
			on s.parentID = e.ID
			where r.ID = ?
		"""
		
		data = system.db.runPrepQuery(lineQuery, [runID], db)
		
		for row in data:
			lineID = row['Line ID']
			linePath = row['Line Path']
			
		# calculate Finish Time
		finishTime = calcFinishTime(linePath)
		
		# get TimeStamp and Format
		timeStamp = datetime.now()
		timeStamp = timeStamp.replace(microseconds=0)
		
		#tagPaths
		infeedPath = linePath + '/Dispatch/OEE Infeed/Count'
		outfeedPath = linePath + '/Dispatch/OEE Outfeed/Count'
		wastePath = linePath + '/Dispatch/OEE Waste/Count'
				
		#these tags were added for stop run function
		totalCountPath = linePath + '/OEE/Total Count'	
		badCountPath = linePath + '/OEE/Bad Count'
		goodCountPath = linePath + '/OEE/Good Count'
		oeeQualityPath = linePath + '/OEE/OEE Quality'
		oeePerformancePath = linePath + '/OEE/OEE Performance'
		oeeAvailabilityPath = linePath + '/OEE/OEE Availability'
		oeePath = linePath + '/OEE/OEE'
		runTimePath = linePath + '/OEE/Runtime'
		unplannedDowntimePath = linePath + '/OEE/Unplanned Downtime'
		plannedDowntimePath = linePath + '/OEE/Planned Downtime'
		totalTimePath = linePath + '/OEE/Total Time'
		
		#read all of our tags
		infeed = system.tag.readBlocking(infeedPath)[0].value
		outfeed = system.tag.readBlocking(outfeedPath)[0].value
		waste = system.tag.readBlocking(wastePath)[0].value
		totalCount = system.tag.readBlocking(totalCountPath)[0].value
		badCount = system.tag.readBlocking(badCountPath)[0].value
		goodCount = system.tag.readBlocking(goodCountPath)[0].value
		quality = system.tag.readBlocking(oeeQualityPath)[0].value
		performance = system.tag.readBlocking(oeePerformancePath)[0].value
		availability = system.tag.readBlocking(oeeAvailabilityPath)[0].value
		oee = system.tag.readBlocking(oeePath)[0].value
		runTime = system.tag.readBlocking(runTimePath)[0].value
		unplannedDownTime = system.tag.readBlocking(unplannedDowntimePath)[0].value
		plannedDownTime = system.tag.readBlocking(plannedDowntimePath)[0].value
		totalTime = system.tag.readBlocking(totalTimePath)[0].value
		
		# update Run Query
		query = """
			Update Run set
			CurrentInfeed = ?,
			CurrentOutfeed = ?,
			CurrentWaste = ?,
			TotalCount = ?,
			WasteCount = ?,
			GoodCount = ?,
			Availability = ?,
			Performance = ?,
			Quality = ?,
			OEE = ?,
			Runtime = ?,
			UnplannedDowntime = ?,
			PlannedDowntime = ?,
			TotalTime = ?,
			TimeStamp = ?,
			Closed = ?,
			EstimatedFinishTime = ?,
			Where ID = ?
		"""	
		
		args = [infeed, outfeed, waste, totalCount, badCount, goodCount, availability, performance, quality, oee, runTime, unplannedDownTime, plannedDownTime, totalTime, str(timeStamp), 0, str(finishTime), runID)
		system.db.runPrepUpdate(query, args, db)
		
		return 1
		
	except:
		return 0
		
		
		
		
		