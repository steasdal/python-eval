from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal, reqparse, abort
import ast

app = Flask(__name__)
api = Api(app)

#  _                 _       _                         _       _
# | |               | |     | |                       | |     | |
# | |__   ___   ___ | |_ ___| |_ _ __ __ _ _ __     __| | __ _| |_ __ _
# | '_ \ / _ \ / _ \| __/ __| __| '__/ _` | '_ \   / _` |/ _` | __/ _` |
# | |_) | (_) | (_) | |_\__ \ |_| | | (_| | |_) | | (_| | (_| | || (_| |
# |_.__/ \___/ \___/ \__|___/\__|_|  \__,_| .__/   \__,_|\__,_|\__\__,_|
#                                        | |
#                                        |_|

users = [
    {
        "first_name": "Joe",
        "last_name": "Smith",
        "userid": "jsmith",
        "groups": ["admins", "users"]
    },
    {
        "first_name": "Jane",
        "last_name": "Jones",
        "userid": "jjones",
        "groups": ["users", "execs"]
    },
    {
        "first_name": "Jack",
        "last_name": "Sparrow",
        "userid": "jsparrow",
        "groups": ["users", "pirates"]
    }
]

groups = ["admins", "users", "execs", "pirates"]

#                 _             _       _
#                | |           (_)     | |
#   ___ _ __   __| |_ __   ___  _ _ __ | |_ ___
#  / _ \ '_ \ / _` | '_ \ / _ \| | '_ \| __/ __|
# |  __/ | | | (_| | |_) | (_) | | | | | |_\__ \
#  \___|_| |_|\__,_| .__/ \___/|_|_| |_|\__|___/
#                  | |
#                  |_|

link_fields = {
    'rel': fields.String,
    'href': fields.String
}

greeting_fields = {
    'greeting': fields.String,
    'users': fields.Nested(link_fields),
    'groups': fields.Nested(link_fields)
}

user_fields = {
    'userid': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'groups': fields.String,
    'uri': fields.Url('user')
}

user_list_fields = {
    'userids': fields.List(fields.String)
}

group_list_fields = {
    'groups': fields.List(fields.String)
}

class UsersEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userid', type=str, required=True, help='No userid provided', location='json')
        self.reqparse.add_argument('first_name', type=str, required=True, help='No first name provided', location='json')
        self.reqparse.add_argument('last_name', type=str, required=True, help='No last name provided', location='json')
        self.reqparse.add_argument('groups', type=str, required=True, help='No groups defined', location='json')
        super(UsersEndpoint, self).__init__()

    # Return all users
    def get(self):
        return {'users': [marshal(user, user_fields) for user in users]}

    # Create a new user
    def post(self):
        args = self.reqparse.parse_args()

        if userExists(args['userid']):
            print("User '{}' already exists".format(args['userid']))
            abort(409)

        if nonexistentGroup(args['groups']):
            abort(400)

        user_groups = ast.literal_eval(args['groups'])

        user = {
            "userid": args['userid'],
            "first_name": args['first_name'],
            "last_name": args['last_name'],
            "groups": user_groups
        }

        users.append(user)
        return {'user': marshal(user, user_fields)}, 201


class RootEndpoint(Resource):

    # Return a greeting message and some HATEOAS-style links to the users and groups endpoints
    def get(self):

        user_link = {
            "rel": "users",
            "href": "/users/"
        }

        group_link = {
            "rel": "groups",
            "href": "/groups/"
        }

        greeting = {
            "greeting": "Welcome to the python-eval web service.",
            "users": user_link,
            "groups": group_link
        }

        return marshal(greeting, greeting_fields), 200



class UserEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True, help='No first name provided', location='json')
        self.reqparse.add_argument('last_name', type=str, required=True, help='No last name provided', location='json')
        self.reqparse.add_argument('groups', type=str, required=True, help='No groups defined', location='json')
        super(UserEndpoint, self).__init__()

    # Return a particular user
    def get(self, userid):
        user_set = [user for user in users if user['userid'] == userid]

        if len(user_set) == 0:
            print("User '{}' does not exist".format(userid))
            abort(404)

        if len(user_set) > 1:
            print("Strangely, multiple users were found with userid '{}'".format(userid))
            abort(500)

        user = user_set[0]

        return {'user': marshal(user, user_fields)}

    # Update a particular user
    def put(self, userid):
        user_set = [user for user in users if user['userid'] == userid]

        if len(user_set) == 0:
            print("User '{}' does not exist".format(userid))
            abort(404)

        if len(user_set) > 1:
            print("Strangely, multiple users were found with userid '{}'".format(userid))
            abort(500)

        args = self.reqparse.parse_args()

        if nonexistentGroup(args['groups']):
            abort(400)

        user = user_set[0]

        user_groups = ast.literal_eval(args['groups'])

        user["first_name"] = args["first_name"]
        user["last_name"] = args["last_name"]
        user["groups"] = user_groups

        return {'user': marshal(user, user_fields)}, 200

    # Delete a particular user
    def delete(self, userid):
        user_set = [user for user in users if user['userid'] == userid]

        if len(user_set) == 0:
            print("User '{}' does not exist".format(userid))
            abort(404)

        if len(user_set) > 1:
            print("Strangely, multiple users were found with userid '{}'".format(userid))
            abort(500)

        user = user_set[0]
        users.remove(user)

        return {"result": "User with id '{}' successfully deleted".format(userid)}, 200

class GroupsEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='No group name provided', location='json')
        super(GroupsEndpoint, self).__init__()

    # Return a list of all groups
    def get(self):
        return marshal({'groups': groups}, group_list_fields)

    # Create a new, empty group
    def post(self):
        args = self.reqparse.parse_args()

        if args['name'] in groups:
            print("Group '{}' already exists".format(args['name']))
            abort(409)

        groups.append(args['name'])

        return marshal({'groups': groups}, group_list_fields)

class GroupEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userids', type=str, required=True, help='No member list provided', location='json')
        super(GroupEndpoint, self).__init__()

    # Return a list containing userids of all users in a particular group
    def get(self, groupname):
        if groupname not in groups:
            abort(404)

        userids = []

        for user in users:
            for group in user["groups"]:
                if group == groupname:
                    userids.append(user["userid"])
                    break

        return marshal({'userids': userids}, user_list_fields)

    # Update group membership.  The request body will contain a list of
    # user id's.  This method will add this group to each user's group list.
    def put(self, groupname):
        if groupname not in groups:
            abort(404)

        args = self.reqparse.parse_args()

        parsed_userids = ast.literal_eval(args['userids'])

        print("parsed userids: {}".format(", ".join(parsed_userids)))

        for user in users:
            if user['userid'] in parsed_userids:
                addGroup(user, groupname)
            else:
                removeGroup(user, groupname)

        return marshal({'userids': parsed_userids}, user_list_fields), 200

    # Delete a group.  This will remove the group from the group list
    # as well as remove the group from each user's group list.
    def delete(self, groupname):
        if groupname not in groups:
            abort(404)

        for user in users:
            removeGroup(user, groupname)

        groups.remove(groupname)

        return {"result": "Group '{}' successfully deleted".format(groupname)}, 200


api.add_resource(RootEndpoint, '/', endpoint='root')
api.add_resource(UsersEndpoint, '/users/', endpoint ='users')
api.add_resource(UserEndpoint, '/users/<userid>', endpoint ='user')
api.add_resource(GroupsEndpoint, '/groups/', endpoint ='groups')
api.add_resource(GroupEndpoint, '/groups/<groupname>', endpoint ='group')

#            _              __                  _   _
#           (_)            / _|                | | (_)
#  _ __ ___  _ ___  ___   | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
# | '_ ` _ \| / __|/ __|  |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | | | | | | \__ \ (__   | | | |_| | | | | (__| |_| | (_) | | | \__ \
# |_| |_| |_|_|___/\___|  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#

# Return true if a user exists with the specified userid
def userExists(userid):
    result = False

    for user in users:
        if user['userid'] == userid:
            result = True
            break

    return result


# Return true if any of the groups in raw_groups don't exist in groups
def nonexistentGroup(raw_groups):
    result = False

    # Parse the group list string into an actual list
    parsed_groups = ast.literal_eval(raw_groups)

    # If the group is not in our list of groups, raise an
    for group in parsed_groups:
        if group not in groups:
            result = True
            print("Group '{}' is not in groups".format(group))

    return result


# add a group to a user's group list
def addGroup(user, group):

    user_groups = user['groups']

    if group not in user_groups:
        user_groups.append(group)


# remove a group from a user's group list
def removeGroup(user, group):

    user_groups = user['groups']

    if group in user_groups:
        user_groups.remove(group)

#   __ _ _ __  _ __
#  / _` | '_ \| '_ \
# | (_| | |_) | |_) |
#  \__,_| .__/| .__/
#       | |   | |
#       |_|   |_|

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
