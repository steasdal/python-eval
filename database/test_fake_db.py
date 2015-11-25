import database.fake_db as db
import pytest

class TestFakeDbUsers():

    # Verify that allUsers returns our list of our three expected users.
    def test_allUsers(self):
        users = db.allUsers()
        assert len(users) == 3

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
