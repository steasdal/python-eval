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

    if len(user_list) < 1:
        raise LookupError("user with userid '{}' does not exist".format(userid))

# Return a particular user that matches the userid
def getUserByUserid(userid):
    user_list = [user for user in users if user.userid == userid]

    if len(user_list) < 1:
        raise LookupError("user with userid '{}' does not exist".format(userid))

    return user_list[0]











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
    if not groupNameExists(group_name):
        raise LookupError("group '{}' does not exist".format(group_name))

    [groups.remove(group) for group in groups if group.name == group_name]

def removeGroup(group):
    removeGroupByName(group.name)




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

