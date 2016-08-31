import maya.cmds as cmds

def addChildJoints(baseJoint, jointList):
    # add current joint to the list
    jointList.append(baseJoint);

    # check for parent joint
    parentJoint = cmds.listRelatives(baseJoint, p=True);
    if parentJoint != None:
        # unparent the joint
        cmds.parent(baseJoint, w=True);

    # get child joints
    childJoints = cmds.listRelatives(baseJoint, c=True);

    # recursion
    if childJoints != None:
        for childJoint in childJoints:
            addChildJoints(childJoint, jointList);

    return;

def lookAt(currentJoint, targetJoint):
    # clear orient channel
    cmds.joint(currentJoint, edit=True, o=(0, 0, 0));

    # clear rotate channel
    cmds.xform(currentJoint, ro=(0, 0, 0), r=False);

    # create a locator
    tempLocator = cmds.spaceLocator()[0];
    currentJointPosition = cmds.joint(currentJoint, p=True, q=True);
    cmds.move(currentJointPosition[0], currentJointPosition[1], currentJointPosition[2], tempLocator);

    # create aim constraint
    tempAimConstraint = cmds.aimConstraint(targetJoint, tempLocator)[0];

    # get locator's rotation
    lookAtRotation = cmds.xform(tempLocator, q=True, ws=False, ro=True);
    cmds.joint(currentJoint, edit=True, o=(lookAtRotation[0], lookAtRotation[1], lookAtRotation[2]));

    # delete locator and aim constraint
    cmds.delete(tempAimConstraint, tempLocator);

    return;

def alignJoints(jointList):
    listSize = len(jointList);
    for i in range(listSize - 2, -1, -1):
        currentJoint = jointList[i];
        lookAtJoint = jointList[i + 1];

        # align the joint
        lookAt(currentJoint, lookAtJoint);
    return;

def attachJoints(jointList):
    listSize = len(jointList);
    for i in range(1, listSize):
        currentJoint = jointList[i];
        parentJoint = jointList[i - 1];

        # parent the joint
        cmds.parent(currentJoint, parentJoint);

        # reset end joint
        if i == listSize - 1:
            cmds.joint(currentJoint, edit=True, o=(0, 0, 0));
            cmds.xform(currentJoint, ro=(0, 0, 0), r=False);

    return;

# stores all the joints selected (child joints included)
selectedJoints = [];

# base joint
selectedJoint = cmds.ls(sl=True)[0];

# add all the selected joints to the list
addChildJoints(selectedJoint, selectedJoints);

# align the joints
alignJoints(selectedJoints);

# reattach the joints
attachJoints(selectedJoints);
