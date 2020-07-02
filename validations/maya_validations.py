# maya validation checks

# find installed Maya on the machine, then call mayapy.exe and run the script.


try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass
