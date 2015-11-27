from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal, reqparse, abort
import database.fake_db as db
import ast

app = Flask(__name__)
api = Api(app)

link_fields = {
    'rel': fields.String,
    'href': fields.String
}

greeting_fields = {
    'greeting': fields.String,
    'users': fields.Nested(link_fields),
    'groups': fields.Nested(link_fields)
}

user_list_fields = {
    'userids': fields.List(fields.String)
}

group_field = {
    'name': fields.String
}

user_fields = {
    'userid': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'groups': fields.Nested(group_field)
}


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
        return {'users': [marshal(user, user_fields) for user in db.allUsers()]}

    # Create a new user
    def post(self):
        args = self.reqparse.parse_args()

        try:
            group_names = ast.literal_eval(args['groups'])
            groups = [db.getGroupByName(group_name) for group_name in group_names]

            user = db.User(
                args["userid"],
                args["first_name"],
                args["last_name"],
                groups
            )

            db.addUser(user)
            return {'user': marshal(user, user_fields)}, 201

        # User already exists with this userid
        except ValueError as ve:
            print( str(ve) )
            abort(409)

        # One or more of the groups are invalid
        except LookupError as le:
            print( str(le) )
            abort(400)


class UserEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True, help='No first name provided', location='json')
        self.reqparse.add_argument('last_name', type=str, required=True, help='No last name provided', location='json')
        self.reqparse.add_argument('groups', type=str, required=True, help='No groups defined', location='json')
        super(UserEndpoint, self).__init__()

    # Return a particular user
    def get(self, userid):

        try:
            user = db.getUserByUserid(userid)
            return {'user': marshal(user, user_fields)}

        # Can't find a user with this userid
        except LookupError as le:
            print( str(le) )
            abort(404)

    # Update a particular user
    def put(self, userid):
        args = self.reqparse.parse_args()

        groups = []

        try:
            group_names = ast.literal_eval(args['groups'])
            groups = [db.getGroupByName(group_name) for group_name in group_names]

        # One of the groups is invalid.
        except LookupError as le:
            print( str(le) )
            abort(400)

        try:
            new_user = db.User(
                userid,
                args['first_name'],
                args['last_name'],
                groups
            )

            db.updateUser(new_user)
            return {'user': marshal(new_user, user_fields)}, 200

        # Can't find a user for this userid
        except LookupError as le:
            print( str(le) )
            abort(404)

    # Delete a particular user
    def delete(self, userid):

        try:
            db.deleteUserByUserId(userid)
            return {"result": "User with id '{}' successfully deleted".format(userid)}, 200

        # Can't find user with this userid
        except LookupError as le:
            print( str(le) )
            abort(404)


class GroupsEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='No group name provided', location='json')
        super(GroupsEndpoint, self).__init__()

    # Return a list of all groups
    def get(self):
        return {'groups': [marshal(group, group_field) for group in db.allGroups()]}

    # Create a new, empty group
    def post(self):
        args = self.reqparse.parse_args()

        try:
            new_group = db.Group(args['name'])
            db.addGroup(new_group)
            return marshal(new_group, group_field)

        # This group already exists
        except ValueError as ve:
            print( str(ve) )
            abort(409)


class GroupEndpoint(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userids', type=str, required=True, help='No member list provided', location='json')
        super(GroupEndpoint, self).__init__()

    # Return a list containing userids of all users in a particular group
    def get(self, groupname):
        try:
            group = db.getGroupByName(groupname)
            return marshal({'userids': db.getUserIdsForGroup(group)}, user_list_fields)

        # Group dosn't exist.
        except LookupError as le:
            print( str(le) )
            abort(404)

    # Update group membership.  The request body will contain a list of
    # user id's.  This method will add this group to each user's group list
    # and remove this group for any user not on the list.
    def put(self, groupname):
        args = self.reqparse.parse_args()

        try:
            group = db.getGroupByName(groupname)
            userids = ast.literal_eval(args['userids'])
            db.updateGroupMembership(group, userids)

            return marshal({'userids': userids}, user_list_fields), 200

        # Group doesn't exist or one of the
        # userids doesn't match an existing user.
        except LookupError as le:
            print( str(le) )
            abort(404)

    # Delete a group.  This will remove the group from the group list
    # as well as remove the group from each user's group list.
    def delete(self, groupname):

        try:
            db.removeGroupByName(groupname)
            return {"result": "Group '{}' successfully deleted".format(groupname)}, 200

        # Can't find the group
        except LookupError as le:
            print( str(le) )
            abort(404)


api.add_resource(RootEndpoint, '/', endpoint='root')
api.add_resource(UsersEndpoint, '/users/', endpoint ='users')
api.add_resource(UserEndpoint, '/users/<userid>', endpoint ='user')
api.add_resource(GroupsEndpoint, '/groups/', endpoint ='groups')
api.add_resource(GroupEndpoint, '/groups/<groupname>', endpoint ='group')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
