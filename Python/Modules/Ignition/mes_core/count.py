"""
This script is for handling count events from ignition tags. Events are summed and stored in the mes_core database.
"""

def storeCountHistory(currentCount, lastCount, tagID, countTypeID):
	"""
	This function takes four arguments from the tag event--the currentCount, lastCount, tagID and countTypeID. 
	When called from the tag event, this function will calculate the count delta and then insert a new count
	history record with the delta, count type, tagID and timestamp.  We return the currentValue to the tag event
	so the value can be written to the last count tag to be used by the next count delta calculation.
	"""
	import system
	from datetime import datetime
	import time
	db = "mes_core" 	# change this later to system.read and not hard code
	stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	countDelta = currentCount - lastCount 	# change this later to use Try and Except
	
	if abs(countDelta) >= 1:
		query = "insert into counthistory(TagID, CountTypeID, Count, TimeStamp) values(?, ?, ?, ?)"
		system.db.runSFPrepUpdate(query, [tagID, countTypeID, countDelta, stamp] , [db])
		return currentCount
		
	else:
		return -1

