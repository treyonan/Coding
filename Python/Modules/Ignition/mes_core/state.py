'''
This function takes two arguments from the tag event -- the reasonCode and the lineID. When called from the tag event,
this function will fill in the end time of the previous state history entry and create a new entry for the current state.

'''
import system
from datetime import datetime
import time

def storeStateHistory(reasonCode, lineID):	

	db = 'mes_core'
	stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	data = system.db.runPrepQuery('select ID, ReasonName FROM statereason where ReasonCode = ? and ParentID = ?', [reasonCode, lineID], db)
	
	for row in data:
		reasonID = row[0]
		reasonName = row[1]
		
	endQuery = 'update statehistory set EndDateTime = ? where lineID = ? and EndDateTime is NULL'
	query = 'insert into statehistory(StateReasonID, ReasonName, LineID, ReasonCode, StartDateTime) values(?, ?, ?, ?, ?)'
	system.db.runSFPrepUpdate(endQuery, [stamp, lineID], [db])
	time.sleep(2)
	system.db.runSFPrepUpdate(query, [reasonID, reasonName, lineID, reasonCode, stamp], [db])