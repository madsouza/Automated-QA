from distutils.core import setup
import py2exe # py2exe downloaded online. Most common/ commercial method of creating executables from .py files

setup(windows=[r'Interface.py'])# <-- here you input the pathway
                                                                    #     to the file you will run
                                                                    #     Brackets and 'r' are to negate 
                                                                    #     spaces inside folder names
                                                                    
# Input into command prompt:
# C:\Python27\python "Z:\Coop Students\2016\Term 1\Executable Files\Setup.py" py2exe
# |                 |       |                                             |   |    |
# |                 |       |                                             |   |    | 
# |                 |       |                                             |   |    |
# |Since pathway cannot     |                                             |   |    |
# |be altered, must call    |Call the setup file to create the executable.|   |Opens file using
# |python before            |Brackets and 'r' are to negate spaces inside |   |py2exe module
# |inputting .py files      |folder names.                                | 


# executable saves to 'dist' folder, U:\ drive. File in 'build' not needed.
# Executable must be located in folder with all other files in 'dist',
#      references them as a library

# Once all files from dist folder saved into new folder, including new executable,
# create a shortcut and pin to desktop. Watch your creation come to life. Or produce an error.

# IdiotProofExecutables Incorporated
