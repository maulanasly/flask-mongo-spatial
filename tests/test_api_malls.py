from . import MongoSpatialTest
import json


class MallTest(MongoSpatialTest):
    """docstring for AddMall"""

    def add_mall(self, mall):
        client = self.app.test_client()
        resp = client.post('/mall', headers={"Content-Type": "application/json"}, data=json.dumps(mall))
        return resp

    def test_add_mall(self):
        mall = {
            "address": {
                "building": "25-27",
                "street": "paskal hyper square, jl. pasirkaliki",
                "zipcode": "40181"
            },
            "location": {
                "coordinates": [107.5928451, -6.9149731],
                "type": "Point"
            },
            "city": "bandung",
            "contact": "(022) 86082942",
            "country": "indonesia",
            "district": "jawa barat",
            "mall_id": 8,
            "name": "23 paskal shopping centre"
        }
        resp = self.add_mall(mall)
        self.assertOK(resp)

    def get_mall(self, mall_id):
        client = self.app.test_client()
        resp = client.get('/mall/%d' % mall_id)
        return resp

    def test_get_mall(self):
        resp = self.get_mall(8)
        expected_mall = {
            "address": {
                "building": "25-27",
                "street": "paskal hyper square, jl. pasirkaliki",
                "zipcode": "40181"
            },
            "location": {
                "coordinates": [107.5928451, -6.9149731],
                "type": "Point"
            },
            "city": "bandung",
            "contact": "(022) 86082942",
            "country": "indonesia",
            "district": "jawa barat",
            "mall_id": 8,
            "name": "23 paskal shopping centre"
        }
        self.assertOK(resp)
        data = json.loads(resp.content)
        self.assertDictEqual(data, expected_mall)

    def put_mall(self, mall_id, mall):
        client = self.app.test_client()
        resp = client.put('/mall/%d' % mall_id, headers={"Content-Type": "application/json"}, data=json.dumps(mall))
        return resp

    def test_put_mall(self):
        mall = {
            "address": {
                "building": "25-27",
                "street": "paskal hyper square, jl. pasirkaliki",
                "zipcode": "40180"
            },
            "location": {
                "coordinates": [107.5928451, -6.9149731],
                "type": "Point"
            },
            "city": "bandung",
            "contact": "(022) 86082942",
            "country": "indonesia",
            "district": "jawa barat",
            "mall_id": 8,
            "name": "23 paskal shopping centre"
        }
        resp = self.put_mall(8, mall)
        self.assertOK(resp)

    def delete_mall(self, mall_id):
        client = self.app.test_client()
        resp = client.delete('/mall/%d' % mall_id)
        return resp

    def test_delete_mall(self):
        resp = self.delete_mall(8)
        self.assertOK(resp)
