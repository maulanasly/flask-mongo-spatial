from flask import current_app
from flask_restful import Resource, reqparse, marshal_with
from flask_restful_swagger import swagger
from mongo_spatial import mongo
from mongo_spatial.schemes import Mall, MallList


get_mall_parser = reqparse.RequestParser()
get_mall_parser.add_argument('mall_id')
get_mall_parser.add_argument('name')

add_mall_parser = reqparse.RequestParser()
add_mall_parser.add_argument('mall_id', type=int, required=True)
add_mall_parser.add_argument('name', type=str, required=True)
add_mall_parser.add_argument('address', type=dict, required=False)
add_mall_parser.add_argument('contact', type=str, required=False)
add_mall_parser.add_argument('country', type=str, required=False)
add_mall_parser.add_argument('district', type=str, required=False)
add_mall_parser.add_argument('city', type=str, required=False)
add_mall_parser.add_argument('location', type=dict, required=False)

get_all_mall_parser = reqparse.RequestParser()
get_all_mall_parser.add_argument('longitude', type=float)
get_all_mall_parser.add_argument('latitude', type=float)
get_all_mall_parser.add_argument('distance', type=long)

update_mall_parser = reqparse.RequestParser()
update_mall_parser.add_argument('mall_id', type=int, required=True)
update_mall_parser.add_argument('name', type=str, required=False)
update_mall_parser.add_argument('address', type=dict, required=False)
update_mall_parser.add_argument('contact', type=str, required=False)
update_mall_parser.add_argument('country', type=str, required=False)
update_mall_parser.add_argument('district', type=str, required=False)
update_mall_parser.add_argument('city', type=str, required=False)
update_mall_parser.add_argument('location', type=dict, required=False)


class MallCreationAPI(Resource):
    """docstring for MallAPI"""

    @swagger.operation(
        notes="""Add mall / registered new mall""",
        parameters=[
            {
                "name": "mall",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": Mall.__name__,
                "paramType": "body"
            }
        ],
        responseClass=Mall.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(Mall.resource_fields)
    def post(self):
        args = add_mall_parser.parse_args()
        prepare_mall_data = {
            "mall_id": args['mall_id'],
            "name": args['name'],
            "address": args['address'],
            "contact": args['contact'],
            "country": args['country'],
            "district": args['district'],
            "city": args['city'],
            "location": args['location']
        }
        response = mongo.db.malls.insert_one(prepare_mall_data)
        current_app.logger.info('{}'.format(response.__dict__))
        return "created", 201


class MallAPI(Resource):
    """docstring for MallAPI"""

    @swagger.operation(
        notes="""Retrieve data mall""",
        parameters=[
        ],
        responseClass=Mall.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(Mall.resource_fields)
    def get(self, mall_id=None):
        # args = get_mall_parser.parse_args()
        mall = mongo.db.malls.find_one({'mall_id': int(mall_id)})
        current_app.logger.info('dataset:{}'.format(mongo.db.dataset))
        return mall, 200

    @swagger.operation(
        notes="""Update mall""",
        parameters=[
            {
                "name": "mall",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": Mall.__name__,
                "paramType": "body"
            }
        ],
        responseClass=Mall.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(Mall.resource_fields)
    def put(self, mall_id):
        args = update_mall_parser.parse_args()
        prepare_mall_data = {}
        name = args['name']
        address = args['address']
        contact = args['contact']
        country = args['country']
        district = args['district']
        city = args['city']
        location = args['location']
        if name:
            prepare_mall_data['name'] = name
        if address:
            prepare_mall_data['address'] = address
        if contact:
            prepare_mall_data['contact'] = contact
        if country:
            prepare_mall_data['country'] = country
        if district:
            prepare_mall_data['district'] = district
        if city:
            prepare_mall_data['city'] = city
        if location:
            prepare_mall_data['location'] = location
        response = mongo.db.malls.update({'mall_id': mall_id}, {"$set": prepare_mall_data})
        current_app.logger.info(response)
        return "no content", 204

    @swagger.operation(
        notes="""Delete data malls""",
        parameters=[
        ],
        responseClass=Mall.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(Mall.resource_fields)
    def delete(self, mall_id=None):
        mongo.db.malls.remove({'mall_id': int(mall_id)})
        return "no content", 204


class MallListAPI(Resource):
    """docstring for MallListAPI"""

    """docstring for MallAPI"""

    @swagger.operation(
        notes="""Retrieve list of mall""",
        parameters=[
            {
                "name": "longitude",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "long",
                "paramType": "query"
            },
            {
                "name": "latitude",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "long",
                "paramType": "query"
            },
            {
                "name": "distance",
                "description": "",
                "required": False,
                "allowMultiple": False,
                "dataType": "integer",
                "paramType": "query"
            }
        ],
        responseClass=MallList.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
        ]
    )
    # @requires_auth
    @marshal_with(MallList.resource_fields)
    def get(self):
        args = get_all_mall_parser.parse_args()
        filters = {}
        if args['longitude'] and args['latitude']:
            lonlat = [args["longitude"], args["latitude"]]
            filters = {"location": {"$near": {"$geometry": {"type": "Point", "coordinates": lonlat}, "$maxDistance": 5000}}}
        current_app.logger.info(mongo.db.__dict__)
        mall_cursor = mongo.db.malls.find(filters)
        malls = [mall for mall in mall_cursor]
        return {'malls': malls, "count": len(malls)}, 200
