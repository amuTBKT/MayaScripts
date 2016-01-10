'''
Python script for renaming child joints of selected joints
Eg->Renaming finger joints in a wrist can be very tedious, but this script does
    the job in one click. Just select the wrist (in this case) and run the script
CAUTION: Be mindful of the order in which joints are parented, because it would
effect their naming convention

Naming Convention:  bn_l_finger_aij for bones used for skinning 
                    be_l_finger_a0j for bones not used for skinning
Sample:
    bn_l_finger_a01 -> bn_l_finger_a01 -> .... -> be_l_finger_a99
    bn_l_finger_b01 -> bn_l_finger_b01 -> .... -> be_l_finger_b99
    .
    .
    .
    bn_l_finger_z01 -> bn_l_finger_z01 -> .... -> be_l_finger_z99
'''

import maya.cmds as cmds

# just a list of all the alphabets
alphabets = "abcdefghijklmnopqrstuvwxyz"

# name for bones used for skinning
baseName = "bn_l_finger_%s%i%i"

# name for end bones (not used for skinning)
endName = "be_l_finger_%s0%i"

# recursive function to rename child bones (baseName_aij)
'''
@param node: current bone
@param a: name identifier for current bone and all its children
@param i: first identifier
@param j: second identifier
'''
def renameChildren(node, a, i, j):
    children = cmds.listRelatives(node, c=True)
    name = ""
    if (children == None):
        name = endName % (a, j)
        cmds.rename(node, name)
    else:
        name = baseName % (a, i, j)
        cmds.rename(node, name)
        for child in children:
            j += 1
            if (j == 10):
                i += 1;
                j = 0;
            renameChildren(child, a, i, j)
    return

# get selected bones
selectedBones = cmds.ls(sl=True)

for selectedBone in selectedBones:
    # child bones
    childBones = cmds.listRelatives(selectedBone, c=True)

    # process starts here
    childIndex = 0

    # iterate through all the children
    for child in childBones:
        # call function
        renameChildren(child, alphabets[childIndex], 0, 1) 
        # increment childIndex
        childIndex += 1 
    
