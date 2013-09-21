"""
Program configuration entries
"""

#File distribution modes determine how the files are scattered across different cloud storage platforms
#Modes:
#	0 - Store on the storage with the greatest quota, calculated before any changes are made
#	1 - Store on the storage with the greatest quota, recalculated everytime a file is uploaded (might be inaccurate, depending on the sizes of directories, and server storage architecture)
FILE_DISTRIBUTION_MODE = 0