"""
Program configuration entries
"""

#File distribution modes determine how the files are scattered across different cloud storage platforms
#Modes:
#	0 - Store on the storage with the greatest quota, calculated before any changes are made
#	1 - Store on the storage with the greatest quota, recalculated everytime a file is uploaded (might be inaccurate, depending on the sizes of directories, and server storage architecture)
#	2 - Store on the storage according to the results given by a prediction API
FILE_DISTRIBUTION_MODE = 1

AUTO_SYNC = True