#---------------------------------------------------------------------------------------------------#                                                                               #
# Checking proper data formats, reading .json, converting .json to python list, appending to .json. #
#---------------------------------------------------------------------------------------------------#
import json
import os

def loadJson(file_name):
    '''
    Load .json file, convert to python list, and return it.
    '''
    if os.stat(file_name).st_size == 0:     # If file is empty, throw empty return value
        return False

    with open(file_name, "r") as f:         # Open file to read
        data = json.load(f)

    f.close()                               # Close file
    return data

def checkFormat(file_name, new_data):
    '''
    Check what kind of format 'new data' to be added is in.
    '''
    with open(file_name, "r") as f:         # Open file to read
        data = json.load(f)

    try:                                    # This will fail if new_data is not a Python dictionary type
        data.append(json.loads(new_data))   # Append 'new_data' to .json file
        f.close()                           # Close file
        return True
    except ValueError as e:                 # Throw ValueError
        f.close()                           # Close file
        return False

def writeJson(file_name, new_data):
    '''
    Load .json file, append 'new data' that follows .json dict format, and write to file.
    '''
    with open(file_name, "r") as f:     # Open file to read
        data = json.load(f)

    data.append(json.loads(new_data))   # Append 'new_data' to .json file

    with open(file_name, "w") as f:     # Open file to write
        json.dump(data, f, indent=4)    # Dump 'data'

    f.close()                           # Close file

def writeAnyFormat(file_name, new_data):
    '''
    Load .json file, append 'new data' (any format), and write to file.
    '''
    with open(file_name, "r") as f:     # Open file to read
        data = json.load(f)
    
    data.append(new_data)               # Append 'new_data' to .json file

    with open(file_name, "w") as f:     # Open file to write
        json.dump(data, f, indent=4)    # Dump 'data'

    f.close()                           # Close file