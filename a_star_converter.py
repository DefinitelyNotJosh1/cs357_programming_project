# A* Converter
# This program converts a DFA or NFA to an A* automaton.
# Author: Joshua Krasnogorov
# CS357 Programming Project

import numpy as np
import json
import glob


# get input from json file
def getInput():
    # Find all JSON files in the input folder
    json_files = glob.glob("input/*.json")
    
    if not json_files:
        print("Please place a valid DFA or NFA in JSON format into the input folder.")
        exit()
    
    # Use the first JSON file found
    json_file = json_files[0]
    print(f"Reading from: {json_file}")

    # Get the file name without the path
    file_name = json_file.split(".")[0].split("\\")[-1]
    print(f"File name: {file_name}")
    
    # Try to parse the file
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            return data["states"], data["alphabet"], data["initial"], data["accepting"], file_name
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error: unable to parse {e} in {json_file}")
        print("Please place a valid DFA or NFA in JSON format into the input folder.")
        exit()


# Originally was going to increment all states, but it's easier to just 
# make the previous q0 state to q01, and new start state q0. 
# Make sure to update accepting states.
def addStartState(states, initial, accepting):
    newStates = []
    oldStartState = initial
    if oldStartState == "q0":
        oldStartState = "q01"
    newStates.append({"state": "q0", "epsilon": oldStartState})
    for state in states:
        if state["state"] == "q0":
            if state["state"] in accepting:
                accepting.append("q01")
            state["state"] = "q01"
            newStates.append(state)
        else:
            newStates.append(state)
    
    return newStates, accepting


# Add epsilon transition to accepting states, as well as update accepting states
def addEpsilon(states, accepting):
    newStates = []
    for state in states:
        if state["state"] in accepting:
            # For accepting states, add epsilon transition to q01
            newState = state.copy()  # Copy the existing state
            newState["epsilon"] = "q01"  # Add epsilon transition to q01
            newStates.append(newState)
        else:
            newStates.append(state)
    
    if "q0" not in accepting:
        accepting.append("q0")
    
    return newStates, accepting


# Writes new NFA to json file
def writeToFile(states, alphabet, initial, accepting, file_name):
    with open("output/" + file_name + "_output.json", "w") as file:
        json.dump({"states": states, "alphabet": alphabet, "initial": initial, "accepting": accepting}, file, indent=4)



# Main function, just runs everything.
def Main():
    # Get input
    states, alphabet, initial, accepting, file_name = getInput()
    if states is (None or "") or alphabet is (None or "") or initial is (None or "") or accepting is None:
        print("Unable to parse file. Please place a valid DFA or NFA in JSON format into the input folder.")
        exit()

    # Add start state
    newStates, accepting = addStartState(states, initial, accepting)

    # Add epsilon transition to accepting states
    newStates, accepting = addEpsilon(newStates, accepting)

    # Write to file
    writeToFile(newStates, alphabet, initial, accepting, file_name)
    print("Written to file: output/output_" + file_name)
    print("Done")

# Call main function
Main()
