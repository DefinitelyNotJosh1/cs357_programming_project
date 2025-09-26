# A* Converter
# This program converts a DFA or NFA to an A* automaton.
# Author: Joshua Krasnogorov
# CS357 Programming Project

import numpy as np
import json
import glob


##
# getInput
# Description: Get input from JSON files in the input folder, also does error checking
#
# Parameters:  
#       None
# Returns: 
#       List of lists, each containing the states, alphabet, initial state, accepting states, and file name
##
def getInput():

    inputs = []
    # Find all JSON files in the input folder
    json_files = glob.glob("input/*.json")
    
    if not json_files:
        print("Please place a valid DFA or NFA in JSON format into the input folder.")
        exit()
    
    # Go through all JSON files
    for json_file in json_files:
        # print(f"Reading from: {json_file}")
        file_name = json_file.split(".")[0].split("\\")[-1]
        # print(f"File name: {file_name}")
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                inputs.append([data["states"], data["alphabet"], data["initial"], data["accepting"], file_name])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error: unable to parse {e} in {json_file}")
            print(f"Skipping file {json_file}")
    
    if len(inputs) == 0:
        print("Please place a valid DFA or NFA in JSON format into the input folder.")
        exit()
    
    return inputs


##
# addStartState
# Description: Adds a new start state to the NFA/DFA, updates the states and accepting states accordingly
# Makes the new start state the name of the original start state (e.g. q0), and makes the old start state 
# the name of the original start state plus 1 (e.g. q01).
#
# Parameters:  
#       states: Dictionary of the states and their transitions in the NFA
#       initial: The initial state of the NFA
#       accepting: The accepting states of the NFA
# Returns: 
#       newStates: Dictionary of the states and their transitions in the NFA with the new start state
#       accepting: The accepting states of the NFA with the new start state
##
def addStartState(states, initial, accepting):
    newStates = []

    newStartState = initial
    # Make old start state "qX1"
    oldStartState = initial + "1"

    # Add epsilon transition from new start state to old start state
    newStates.append({"state": newStartState, "epsilon": oldStartState})
    for state in states:
        # If the state is an accepting state, add the new start state to accepting states
        # Now find the old start state
        if state["state"] == newStartState:
            # If the old start state is an accepting state, add the new start state to accepting states
            if state["state"] in accepting:
                accepting.append(oldStartState)
            # Now re-label the old start state
            state["state"] = oldStartState
            newStates.append(state)
        else:
            newStates.append(state)

    # Update all old transitions 
    for state in newStates:
        if state["state"] == newStartState:
            continue
        for key, value in list(state.items()):
            if isinstance(value, list):
                state[key] = [oldStartState if v == newStartState else v for v in value]
            elif value == newStartState:
                state[key] = oldStartState

    return newStates, accepting


##
# addEpsilon
# Description: Adds an epsilon transition to the accepting states, as well as updates accepting states
#
# Parameters:  
#       states: Dictionary of the states and their transitions in the NFA
#       initial: The (old) initial state of the NFA
#       accepting: The accepting states of the NFA
# Returns: 
#       newStates: Dictionary of the states and their transitions in the NFA with the new transitions
#       accepting: The updated accepting states of the NFA
##
# Add epsilon transition to accepting states, as well as update accepting states
def addEpsilon(states, initial, accepting):
    newStates = []
    for state in states:
        if state["state"] in accepting:
            # For accepting states, add epsilon transition to q01
            newState = state.copy()  # Copy the existing state
            newState["epsilon"] = initial + "1"  # Add epsilon transition to q01
            newStates.append(newState)
        else:
            newStates.append(state)

       # Add new start state to accepting states
    if initial not in accepting:
        accepting.append(initial)
    
    return newStates, accepting


##
# writeToFile
# Description: Writes new NFA to json file
#
# Parameters:  
#       states: Dictionary of the states and their transitions in the NFA
#       alphabet: The alphabet of the NFA
#       initial: The initial state of the NFA
#       accepting: The accepting states of the NFA
#       file_name: The name of the file to write to
# Returns: 
#       None
##
##
def writeToFile(states, alphabet, initial, accepting, file_name):
    with open("output/" + file_name + "_output.json", "w") as file:
        json.dump({"states": states, "alphabet": alphabet, "initial": initial, "accepting": accepting}, file, indent=4)



##
# Main
# Description: Main function, just runs everything.
#
# Parameters:  
#       None
# Returns: 
#       None
##
def Main():

    print("|---------------------------------|")
    print("|      Starting A* Converter      |")
    print("|---------------------------------|")
    # Get input
    inputs = getInput()
    for input in inputs:
        print(f"Processing file: {input[4]}")
        states, alphabet, initial, accepting, file_name = input

        # Add start state
        newStates, accepting = addStartState(states, initial, accepting)

        # Add epsilon transition to accepting states
        newStates, accepting = addEpsilon(newStates, initial, accepting)

        # Write to file
        writeToFile(newStates, alphabet, initial, accepting, file_name)
        print("Written to file: output/output_" + file_name)
        print("Done")

# Call main function
Main()
