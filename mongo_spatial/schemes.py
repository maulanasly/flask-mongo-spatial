from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class Mall(object):

    resource_fields = {
        'mall_id': fields.Integer(),
        'name': fields.String(),
        'address': fields.Raw(),
        'contact': fields.String(),
        'country': fields.String(),
        'district': fields.String(),
        'city': fields.String(),
        'location': fields.Raw()
    }
    required = ['name']


@swagger.model
@swagger.nested(
    malls=Mall.__name__)
class MallList(object):
    """docstring for ClassName"""

    resource_fields = {
        "malls": fields.List(fields.Nested(Mall.resource_fields)),
        "count": fields.Integer()
    }

    required = ['malls']
