from flask import Flask
import urllib
import json
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import reqparse
from flask_restplus import inputs
from pymongo import *
from bson.objectid import ObjectId
import bson
import datetime
import re
app = Flask(__name__)
api = Api(app,
          default = 'world_bank_record',
          title = 'API',
          description='Assignment2'
)
indicator_model = api.model('Indicator', {
    'indicator_id': fields.String,
})

MONGODB_URI = 'mongodb://HaiyuLYU:lhy123177@ds251622.mlab.com:51622/my_database'
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database('my_database')
user_db = db.world_records
def getReturn(data):
    rData = {}
    rData['location'] = '/world_records/' + str(data['_id'])
    rData['collection_id'] = str(data['_id'])
    rData['creation_time'] = data['creation_time']
    rData['indicator'] = data['indicator']
    return rData

@api.route('/world_records')
class listData(Resource):
    @api.expect(indicator_model, validate=True)
    @api.response(201, 'Created')
    @api.response(404, 'Not found')
    @api.response(200, 'OK')
    def post(self):
        readIndicator = request.json
        indicator = readIndicator['indicator_id']
        data = user_db.find_one({'indicator': indicator})
        if data:
            return {'location': '/world_records/' + str(data['_id'])}, 200
        else:
            newData = []
            for j in range(1, 3):
                pageNum = str(j)
                url = 'http://api.worldbank.org/v2/countries/all/indicators/'+indicator+'?date=2012:2017&format=json&page=' + pageNum
                with urllib.request.urlopen(url) as url:
                    data1 = json.loads(url.read())
                if j == 1 and len(data1) == 1:
                    return {'message': 'Indicator_id does not exist.'}, 404
                for i in range(len(data1[1])):
                    if data1[1][i]['indicator']['id'] == indicator:
                        d = {}
                        indicator_value = data1[1][0]['indicator']['value']
                        d['country'] = data1[1][i]['country']['value']
                        d['date'] = data1[1][i]['date']
                        d['value'] = data1[1][i]['value']
                        newData.append(d)
            time = str(datetime.datetime.now())
            record = {
                'indicator': indicator,
                'indicator_value': indicator_value,
                'creation_time': time,
                'entries': newData
            }
            user_db.insert_one(record)
            data = user_db.find_one({'indicator': indicator})
            return getReturn(data),201

    @api.response(400, 'No data')
    @api.response(200, 'OK')
    def get(self):
        data = user_db.find({})
        newD = []
        for d in data:
            newD.append(getReturn(d))
        if len(newD) == 0:
            return {'message': 'No collections in list.'},400
        return newD,200
def changedIndexName(data):
    data2 = {}
    data2['collection_id'] = str(data['_id'])
    data2['indicator'] = data['indicator']
    data2['indicator_value'] = data['indicator_value']
    data2['creation_time'] = data['creation_time']
    data2['entries'] = data['entries']
    return data2

@api.route('/world_records/<string:collection_id>')
class oneData(Resource):
    @api.response(404, 'Not found')
    @api.response(200, 'OK')
    def delete(self,collection_id):
        if not bson.objectid.ObjectId.is_valid(collection_id):
            return {'message': 'Collection_id does not exist.'}, 404
        result = user_db.delete_one({'_id': ObjectId(collection_id)})
        if result.deleted_count:
            return {'message':'Collection = '+ collection_id+ ' is removed from the database!'}, 200
        else:
            return {'message': 'Collection_id does not exist.'}, 404

    @api.response(404, 'Not found')
    @api.response(200, 'OK')
    def get(self,collection_id):
        if not bson.objectid.ObjectId.is_valid(collection_id):
            return {'message': 'Collection_id does not exist.'}, 404
        data = user_db.find_one({'_id': ObjectId(collection_id)})
        if data:
            data2 = changedIndexName(data)
            return data2, 200
        else:
            return {'message': 'Collection_id does not exist.'}, 404

@api.route('/world_records/<string:collection_id>/<string:year>/<string:country>')
class trData(Resource):
    @api.response(404, 'Not found')
    @api.response(200, 'OK')
    def get(self,collection_id,year,country):
        if not bson.objectid.ObjectId.is_valid(collection_id):
            return {'message': 'Collection_id does not exist.'}, 404
        data = user_db.find_one({'_id': ObjectId(collection_id)})
        if data:
            data2 = {}
            data2['collection_id'] = str(data['_id'])
            data2['indicator'] = data['indicator']
            for d in data['entries']:
                if d['date'] == year and d['country'] == country:
                    data2['country'] = d['country']
                    data2['year'] = d['date']
                    data2['value'] = d['value']
                    break
            if len(data2) == 2:
                return {'message': 'The year or the country does not exist.'}, 404
            return data2, 200
        else:
            return {'message': 'Collection_id does not exist.'}, 404

parser = reqparse.RequestParser()
parser.add_argument('query')
@api.route('/world_records/<string:collection_id>/<string:year>')
class queryData(Resource):
    @api.response(404, 'Not found')
    @api.response(200, 'OK')
    @api.expect(parser)
    def get(self,collection_id,year):
        if not bson.objectid.ObjectId.is_valid(collection_id):
            return {'message': 'Collection_id does not exist.'}, 404
        args = parser.parse_args()
        query = str(args.get('query'))
        data = user_db.find_one({'_id': ObjectId(collection_id)})
        reQuery = re.findall(r'[a-z]+|[0-9]+', query)
        data2 = {}
        entries = []
        data2['indicator'] = data['indicator']
        data2['indicator_value'] = data['indicator_value']
        for e in data['entries']:
            if e['date'] == year:
                entries.append(e)
        if query == 'None':
            entries = sorted(entries, key=lambda x: x['value'], reverse=True)
            data2['entries'] = entries
            return data2, 200
        elif len(reQuery) == 2:
            asc = reQuery[0]
            num = int(reQuery[1])
            if asc == 'top':
                entries = sorted(entries, key = lambda x:x['value'], reverse=True)
                l = len(entries)
                if l <= num:
                    data2['entries'] = entries
                else:
                    data2['entries'] = entries[0:num]
                return data2, 200
            elif asc == 'bottom':
                entries = sorted(entries, key=lambda x: x['value'])
                l = len(entries)
                if l <= num:
                    data2['entries'] = entries
                else:
                    data2['entries'] = entries[0:num]
                return data2, 200
            else:
                return {'message': 'The query does not exist.'}, 404
        else:
            return {'message': 'The query does not exist.'}, 404

if __name__ == '__main__':
    app.run(debug=True)

