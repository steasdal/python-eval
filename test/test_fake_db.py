import database.fake_db as db
import pytest

#                        _            _
#                       | |          | |
#  _   _ ___  ___ _ __  | |_ ___  ___| |_ ___
# | | | / __|/ _ \ '__| | __/ _ \/ __| __/ __|
# | |_| \__ \  __/ |    | ||  __/\__ \ |_\__ \
#  \__,_|___/\___|_|     \__\___||___/\__|___/
#

class TestFakeDbUsers():

    # Verify that allUsers returns our list of our three expected users.
    def test_allUsers(self):
        users = db.allUsers()
        assert len(users) == 3

    # Verify that userExists returns true for an existing user, false otherwise
    def test_userExistsById(self):
        assert db.userExistsByUserid("jsmith")
        assert db.userExistsByUserid("jjones")
        assert db.userExistsByUserid("jsparrow")
        assert not db.userExistsByUserid("pjiasasdf9")
        assert not db.userExistsByUserid("ha-898ashdf")

    # Get a particular user by userid
    def test_getUserByUserid(self):
        user = db.getUserByUserid("jsmith")
        assert user.first_name == "Joe"
        assert user.last_name == "Smith"
        for group in user.groups:
            assert group.name in ["admins", "users"]

    # Verify that getUserByUserid raises a LookupError
    # if a user with does not exist with that userid
    def test_getUserByUserId_nonexistent(self):
        with pytest.raises(LookupError):
            db.getUserByUserid(";apoijpoiajsdf")

    # Verify that we can add a new user with no groups
    def test_addUser_no_groups(self):
        user_count = len(db.allUsers())
        db.addUser(db.User("u001", "joe", "user", [] ))
        assert len(db.allUsers()) == (user_count + 1)

    # Verify that we can add a new user with groups
    def test_addUser(self):
        user_count = len(db.allUsers())
        db.addUser(db.User("u002", "jimmy", "user", [
            db.Group("users"),
            db.Group("pirates")
        ]))
        assert len(db.allUsers()) == (user_count + 1)

    # Verify that addUser throws an exception when we attempt to
    # add a user with the same userid as an existing user.
    def test_addUser_conflict(self):
        db.addUser(db.User("u003", "jack", "user"))

        with pytest.raises(ValueError):
            db.addUser(db.User("u003", "jack", "user"))

    # Verify that addUser throws an exception when we
    # attempt to add a user with groups that don't exist.
    def test_addUser_bad_groups(self):
        with pytest.raises(LookupError):
            db.addUser(db.User("u004", "who", "cares", [db.Group("ap-8u9-8aojoia")]))

    # Verify that updateUser throws an exception if we
    # attempt to update a nonexistent user.
    def test_updateUser_nonexistent(self):
        with pytest.raises(LookupError):
            db.updateUser(db.User("u005", "what", "ever"))

    # Verify that updateUser throws an exception if
    # one of this new user's groups doesn't already exist.
    def test_updateUser_bad_groups(self):
        db.addUser(db.User("u006", "tammy", "nguyen", [db.getGroupByName("admins")]))

        with pytest.raises(LookupError):
            db.updateUser(db.User("u006", "tammy", "nguyen", [db.Group("o089ujasdf")]))

    # Verify that updateUser can actually update an existing user
    def test_updateUser(self):
        db.addUser(db.User("u007", "jeff", "hernandez", [
            db.getGroupByName("users"),
            db.getGroupByName("execs")
        ]))

        db.updateUser(db.User("u007", "joe", "gonzalez", [
            db.getGroupByName("admins"),
            db.getGroupByName("pirates")
        ]))

        user = db.getUserByUserid("u007")

        assert user.userid == "u007"
        assert user.first_name == "joe"
        assert user.last_name == "gonzalez"

        for group in user.groups:
            assert group.name in ["admins", "pirates"]

    # Can we delete a user?
    def test_deleteUser(self):
        user = db.User("u008", "trad", "miller")

        db.addUser(user)
        assert db.userExistsByUserid(user.userid)

        db.deleteUserByUserId(user.userid)
        assert not db.userExistsByUserid(user.userid)

    # Verify that userHasGroup returns true if a user has a
    # particular group in its group list, false otherwise.
    def test_userHasGroup(self):
        user = db.User("u009", "tronald", "dump", [
            db.getGroupByName("execs"),
            db.getGroupByName("pirates")
        ])

        assert db.userHasGroup(user, db.getGroupByName("execs"))
        assert db.userHasGroup(user, db.getGroupByName("pirates"))
        assert not db.userHasGroup(user, db.getGroupByName("admins"))
        assert not db.userHasGroup(user, db.getGroupByName("users"))

    # Can we add and remove groups from a user?
    def test_addGroupToUser(self):
        user = db.User("u010", "jimmy", "franco", [
            db.getGroupByName("admins")
        ])

        assert len(user.groups) == 1
        assert "users" not in [group.name for group in user.groups]

        db.addGroupToUser(user, db.getGroupByName("users"))

        assert len(user.groups) == 2
        assert "admins" in [group.name for group in user.groups]
        assert "users" in [group.name for group in user.groups]

        db.removeGroupFromUser(user, db.getGroupByName("admins"))

        assert len(user.groups) == 1
        assert "admins" not in [group.name for group in user.groups]

#                                _            _
#                               | |          | |
#   __ _ _ __ ___  _   _ _ __   | |_ ___  ___| |_ ___
#  / _` | '__/ _ \| | | | '_ \  | __/ _ \/ __| __/ __|
# | (_| | | | (_) | |_| | |_) | | ||  __/\__ \ |_\__ \
#  \__, |_|  \___/ \__,_| .__/   \__\___||___/\__|___/
#   __/ |               | |
#  |___/                |_|

class TestFakeDbGroups():

    # Verify that groupNameExists works as expected
    def test_groupNameExists(self):
        assert db.groupNameExists("users")
        assert db.groupNameExists("admins")
        assert db.groupNameExists("execs")
        assert db.groupNameExists("pirates")
        assert not db.groupNameExists("scoundrels")

    # Verify that groupExists works as expected
    def test_groupExists(self):
        assert db.groupExists(db.Group("users"))
        assert db.groupExists(db.Group("admins"))
        assert db.groupExists(db.Group("execs"))
        assert db.groupExists(db.Group("pirates"))
        assert not db.groupExists(db.Group("scallywags"))

    # Verify that we can add a group by name
    def test_addGroup_new_group(self):
        assert not db.groupNameExists("new_group_001")
        db.addGroupByName("new_group_001")
        assert db.groupNameExists("new_group_001")

    # Verify that we can add a group by object
    def test_addGroup_by_object(self):
        new_group = db.Group("new_group_002")

        assert not db.groupNameExists("new_group_002")
        db.addGroup(new_group)
        assert db.groupNameExists("new_group_002")

    # Verify that attempting to add an existing
    # group results in a ValueError exception
    def test_addGroupByName_exists(self):
        new_group = db.Group("new_group_005")

        assert not db.groupNameExists("new_group_005")
        db.addGroupByName("new_group_005")

        with pytest.raises(ValueError):
            db.addGroupByName("new_group_005")

        with pytest.raises(ValueError):
            db.addGroup(new_group)

    # Verify that attempting to adda
    def test_addGroup_exists(self):
        new_group = db.Group("new_group_006")

        assert not db.groupNameExists(new_group.name)
        db.addGroup(new_group)

        with pytest.raises(ValueError):
            db.addGroup(new_group)

    # Verify that we can get a group by name
    def test_getGroupByName(self):
        group_admins = db.getGroupByName("admins")
        assert group_admins.name == "admins"

    # Verify that getGroupByName throws an exception
    # when we attempt to get a nonexistent group.
    def test_getGroupByName_nonexistent(self):
        with pytest.raises(LookupError):
            db.removeGroupByName("009ij9p0jasdf92j3")

    # Verify that we can remove a group by name
    def test_removeGroup_by_name(self):
        assert not db.groupNameExists("new_group_003")
        db.addGroupByName("new_group_003")
        assert db.groupNameExists("new_group_003")
        db.removeGroupByName("new_group_003")
        assert not db.groupNameExists("new_group_003")
        
    # Verify that we can remove a group by object
    def test_removeGroup_by_object(self):
        new_group = db.Group("new_group_004")

        assert not db.groupNameExists("new_group_004")
        db.addGroup(new_group)
        assert db.groupNameExists("new_group_004")
        db.removeGroup(new_group)
        assert not db.groupNameExists("new_group_004")

    # Verify that removeGroup removes the group from
    # all users that are members of that group.
    def test_removeGroup_from_users(self):
        new_group = db.Group("sweet_new_group")
        db.addGroup(new_group)

        db.addUser(db.User("u020", "aaa", "aaa", [new_group]))
        db.addUser(db.User("u021", "bbb", "bbb", [new_group]))

        assert len( [user for user in db.allUsers() if new_group in user.groups] ) == 2

        db.removeGroup(new_group)

        assert len( [user for user in db.allUsers() if new_group in user.groups] ) == 0

    # Verify that removeGroupByName throws an exception
    # when we attempt to remove a nonexistent group
    def test_removeGroupByName_nonexistent(self):
        with pytest.raises(LookupError):
            db.removeGroupByName("lkjopjojaposijoasijdfosijdf")

    # Verify that removeGroup throws an exception
    # when we attempt to remove a nonexistent group
    def test_removeGroup_nonexistent(self):
        with pytest.raises(LookupError):
            db.removeGroup(db.Group("ppoijpaoij9a8us9d8pjasdf"))

    # Verify that getUserIdsForGroup only returns userids for a particular group.
    def test_getUserIdsForGroup(self):
        new_group = db.Group("particularly_sweet_group")
        db.addGroup(new_group)

        db.addUser(db.User("u025", "aaa", "aaa", [new_group]))
        db.addUser(db.User("u026", "bbb", "bbb", [new_group]))
        db.addUser(db.User("u027", "ccc", "ccc", [db.getGroupByName("admins")]))

        for userid in db.getUserIdsForGroup(new_group):
            assert userid in ["u025", "u026"]
            assert userid not in ["u027"]

    # Verify that updateGroupMembership does that thing it's supposed to do.
    def test_updateGroupMembership(self):
        new_group = db.Group("even_sweeter_new_group")
        db.addGroup(new_group)

        db.addUser(db.User("u030", "aaa", "aaa", [db.getGroupByName("pirates"), new_group]))
        db.addUser(db.User("u031", "bbb", "bbb", [db.getGroupByName("admins"), new_group]))
        db.addUser(db.User("u032", "ccc", "ccc", [db.getGroupByName("execs")]))
        db.addUser(db.User("u033", "ddd", "ddd", [db.getGroupByName("users")]))

        for userid in [user.userid for user in db.allUsers() if new_group in user.groups]:
            assert userid in ["u030", "u031"]

        db.updateGroupMembership(new_group, ["u032", "u033"])

        for userid in [user.userid for user in db.allUsers() if new_group in user.groups]:
            assert userid in ["u032", "u033"]
