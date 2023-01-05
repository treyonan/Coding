'''
This script is designed to take two arguments, [message, level], for the Ignition logging engine. Message is the payload published to the MES logger
and the level is the severity of the log to publish to.
Options are fatal, error, warn, info, debug and trace.

'''
import system


def log(name, level, message):
	logger = system.util.getLogger(name)
	try:
		func = getattr(logger, level)
		func(message)
	except AttributeError:
		print("{} not found".format(level)) 
		
