
#  _   _ ___  ___ _ __ ___
# | | | / __|/ _ \ '__/ __|
# | |_| \__ \  __/ |  \__ \
#  \__,_|___/\___|_|  |___/

class User:
    def __init__(self, userid, first_name, last_name, groups = None):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name

        if groups == None:
            self.groups = []
        else:
            self.groups = groups


# Return a list of all users.
def allUsers():
    return users

def userExistsByUserid(userid):
    user_list = [user for user in users if user.userid == userid]
    return len(user_list) >= 1

# Return a particular user that matches the userid
def getUserByUserid(userid):
    user_list = [user for user in users if user.userid == userid]

    if len(user_list) < 1:
        raise LookupError("user with userid '{}' does not exist".format(userid))

    return user_list[0]

# Add a new user
def addUser(user):
    if userExistsByUserid(user.userid):
        raise ValueError("user with userid '{}' already exists")

    # this'll raise an exception if group doesn't exist
    for group in user.groups:
        getGroupByName(group.name)

    users.append(user)

# Update an existing user.  Find the old user by id, make sure the new
# user's group are legit, delete the old user object, append new one.
def updateUser(new_user):
    old_user = getUserByUserid(new_user.userid)

    # yep, make sure these groups are legit
    for group in new_user.groups:
        getGroupByName(group.name)

    users.remove(old_user)
    users.append(new_user)

# Delete an existing user
def deleteUserByUserId(userid):
    user = getUserByUserid(userid)
    users.remove(user)

def userHasGroup(user, group):
    return len( [user_group for user_group in user.groups if user_group.name == group.name] ) > 0

# Add a group to a user
def addGroupToUser(user, group):
    if not userHasGroup(user, group):
        user.groups.append(group)

# Remove a group from a user
def removeGroupFromUser(user, group):
    if userHasGroup(user, group):
        user.groups.remove(group)

#   __ _ _ __ ___  _   _ _ __  ___
#  / _` | '__/ _ \| | | | '_ \/ __|
# | (_| | | | (_) | |_| | |_) \__ \
#  \__, |_|  \___/ \__,_| .__/|___/
#   __/ |               | |
#  |___/                |_|

class Group:
    def __init__(self, name):
        self.name = name

# Return true if a group already exists with this group name
def groupNameExists(group_name):
    group_list = [group for group in groups if group.name == group_name]
    return len(group_list) >= 1

def groupExists(group):
    return groupNameExists(group.name)

def addGroupByName(new_group_name):
    new_group = Group(new_group_name)
    addGroup(new_group)

def addGroup(new_group):
    if groupNameExists(new_group.name):
        raise ValueError("group with name '{}' already exists")

    groups.append(new_group)

def getGroupByName(group_name):
    group_list = [group for group in groups if group.name == group_name]

    if len(group_list) < 1:
        raise LookupError("group '{}' does not exist".format(group_name))
    else:
        return group_list[0]

def removeGroupByName(group_name):
    removeGroup(getGroupByName(group_name))

# Remove group from group list and from
# users that are members of that group.
def removeGroup(group):
    if not groupExists(group):
        raise LookupError("group '{}' does not exist".format(group.name))

    groups.remove(group)
    [removeGroupFromUser(user, group) for user in users]

# Pass in a group and a list of userid strings
def updateGroupMembership(group, userids):
    if not groupNameExists(group.name):
        raise LookupError("group '{}' does not exist".format(group_name))

    # Turn the list of userids into a list of users.  This'll throw
    # an exception for any userid that doesn't match an actual user.
    found_users = [getUserByUserid(userid) for userid in userids]

    # Iterate through ALL users
    for user in users:
        if user in found_users:
            addGroupToUser(user, group)
        else:
            removeGroupFromUser(user, group)

#  _                 _       _                         _       _
# | |               | |     | |                       | |     | |
# | |__   ___   ___ | |_ ___| |_ _ __ __ _ _ __     __| | __ _| |_ __ _
# | '_ \ / _ \ / _ \| __/ __| __| '__/ _` | '_ \   / _` |/ _` | __/ _` |
# | |_) | (_) | (_) | |_\__ \ |_| | | (_| | |_) | | (_| | (_| | || (_| |
# |_.__/ \___/ \___/ \__|___/\__|_|  \__,_| .__/   \__,_|\__,_|\__\__,_|
#                                        | |
#                                        |_|

groups = [
    Group("users"),
    Group("admins"),
    Group("execs"),
    Group("pirates")
]

users = [
    User("jsmith", "Joe", "Smith", [
        getGroupByName("admins"),
        getGroupByName("users")
    ]),
    User("jjones", "Jane", "Jones", [
        getGroupByName("users"),
        getGroupByName("execs")
    ]),
    User("jsparrow", "Jack", "Sparrow", [
        getGroupByName("users"),
        getGroupByName("pirates")
    ])
]
