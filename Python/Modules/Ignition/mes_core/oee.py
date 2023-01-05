"""

"""

# db variable
 
db = 'mes_core'

# call our log for calc

shared.mes_core.logging.log('MES Core: Calculating OEE', 'info')

def calcQuality(totalCountPath, goodCountPath, oeeQualityPath):
	totalCount = system.tag.readBlocking(totalCountPath)[0].value
	goodCount = system.tag.readBlocking(goodCountPath)[0].value
	
	try:
		quality = float(goodCount)/float(totalCount)
	
	except:
		quality = 1
		
	system.tag.writeBlocking([oeeQualityPath], [quality])
	return quality
	
def calcAvailability(runTimePath, totalTimePath, oeeAvailabilityPath):
	runTime = system.tag.readBlocking(runTimePath)[0].value
	totalTime = system.tag.readBlocking(totalTimePath)[0].value
	
	try:
		availability = float(runTime)/float(totalTime)
	except:
		availability = 1
		
	system.tag.writeBlocking([oeeAvailabilityPath], [availability])
	return availability
	
def calcPerformance(totalCountPath, targetCountPath, oeePerformancePath):
	totalCount = system.tag.readBlocking(totalCountPath)[0].value
	targetCount = system.tag.readBlocking(targetCountPath)[0].value
	
	try:
		performance = float(totalCount)/float(targetCount)
	except:
		performance = 1
		
	system.tag.writeBlocking([oeePerformancePath], [performance])
	return performance
	
def getTagIDs(lineID, db=db):
	listOfTags = []
	id = system.tag.readBlocking(lineID)[0].value
	
	query - 'select ID from counttag where parentID = ?'
	data = system.db.runPrepQuery(query, [id], db)
	
	for row in data:
		tagID = row[0]
		liftOfTags.append(tagID)
		
	return liftOfTags
	
def getGoodCount(goodCountPath, startTimePath, endTimePath, tagID, countTypeID, db=db):
	id = system.tag.readBlocking(lineID)[0].value
	
	query = """
		select sum(Count) from counthistory
		where TagID = ? and
		CountTypeID = ? and
		`TimeStamp` between ? and ?
	
	"""
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	endTime = system.tag.readBlocking(endTimePath)[0].value
	data = system.db.runPrepQuery(query, [tagID, countyTypeID, startTime, endTime], db)	
	
	goodCount = 'None'
	
	for row in data:
		goodCount = row[0]
		
	if goodCount == None:
		goodCount = 0
	else:
		pass
		
	system.tag.writeBlocking([goodCountPath], [goodCount])
	
	return goodCount
	
def getBadCount(badCountPath, startTimePath, endTimePath, tagID, counTypeID, db=db):
	query = """
		select sum(Count) from counthistory
		where tagID = ? and
		CountTypeID = ? and
		`TimeStamp` between ? and ?
	
	"""
	
	startTime = system.tag.readBlocking(startTimePath)[0].value
	endTime = system.tag.readBlocking(endTimePath)[0].value
	
	data = system.db.runPrepQuery(query, [tagID, countTypeID, startTime, endTime], db)
	
	badCount = 'None'
	
	for row in data:
		badCount = row[0]
	if badCount == None:
		badCount = 0
	else:
		pass
		
	system.tag.writeBlocking([badCountPath], [badCount])
		
	return badCount