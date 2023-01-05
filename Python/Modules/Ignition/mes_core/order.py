'''


'''
from shared.mes_core.model import getLineID

db = 'mes_core'

def addProductCode(productCode, description, disable = 0, db=db):
	query = """
	insert productcode(ProductCode, Description, Disable, TimeStamp)
	values(?, ?, ?, now())
	on duplicate key update
	ProductCode = values(ProductCode),
	Description = values(Description),
	Disable = values(Disable),
	TimeStamp = now()
	
	"""
	
	key = system.db.runPrepUpdate(query, [productCode, description, disable], db, getKey=1)
	return key
	
def updateProductCodeLineStatus(productCode, modelPath, enable=True, db=db): # allows us to say which 
	try:
		productCodeID = system.db.runScalarPrepQuery("""
			select ID from productcode
			where ProductCode = ?
		""", [productCode], db)
		
		lineID = getLineID(modelPath)
		
		pclID = system.db.runScalarPrepQuery("""
			select ID from productcodeline
			where ProductCodeID = ?
			and LineID = ?
		""", [productCodeID, lineID], db)
		
		if pclID:
			system.db.runPrepUpdate("""
			update productcodeline
			set Enable = ?, TimeStamp = now()
			where ProductCodeID = ?
			and LineID = ?		
		""", [enable, productCodeID, lineID], db)
		
		else:
			system.db.runPrepUpdate("""
			insert productcodeline(ProductCodeID, LineID, Enable, TimeStamp)
			values(?, ?, ?, now())
		""", [productcodeID, lineID, enable], db)
			
		return 1
		
	except:
		return 0
		
def addWorkOrderEntry(workOrder, productCode, quantity, db=db):
	pcID = system.db.runScalarPrepQuery("""
		select ID
		from productcode
		where ProductCode = ?
		""", [productCode], db)
		
	query = """
		insert workorder(WorkOrder, Quantity, Closed, Hide, TimeStamp, ProductCodeID, ProductCode)
		values(?, ?, 0, 0, now(), ?, ?)
		on duplicate key update
			Quantity = values(Quantity)
		,	ProductCodeID = values(ProductCodeID)
		,	ProductCode = values(ProductCode)
		,	TimeStamp = now()
	"""
	system.db.runPrepUpdate(query, [WorkOrder, quantity, pcID, productCode], db)
	
	
def updateWorkOrderEntry(oldWorkOrderID, newWorkOrder, productCode, quantity, db=db):
	pcID = system.db.runScalarPrepQuery("""
		select ID
		from productcode
		where 	ProductCode = ?
		""", [productCode], db)
	
	query = """
		update workorder
		set WorkOrder = ?
		,	Quantity = ?
		,	ProductCodeID = ?
		,	ProductCode = ?
		where ID = ?	
	"""
	system.db.runPrepUpdate(query, [newWorkOrder, quantity, pcID, productCode, oldWorkOrderID], db)
			
		