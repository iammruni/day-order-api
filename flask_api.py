from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt
import api_key


# Initialize flask app and api
app = Flask(__name__)
api = Api(app)

info_path = './data/maindb.csv'

# info endpoint


class info(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('key', required=True, type=str)
		args = parser.parse_args()
		print(args)

		if not 'key' in args:
			return{
				'message': {
					'key': 'Missing required parameter. API Key missing!'
				}
			}, 403

		else:
			res = api_key.ver(args['key'], "get")
			if res[0]:
				data = pd.read_csv(info_path, header=0)
				data = data.to_dict('list')
				return data, 200
			else:
				return{
					'message': res[1]
				}, res[2]

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('day_order', required=True, type=int)
		parser.add_argument('key', required=True, type=str)
		args = parser.parse_args()

		if not 'key' in args:
			return{
				'message': {
					'key': 'Missing required parameter. API Key missing!'
				}
			}, 403

		else:
			res = api_key.ver(args['key'], "post")
			if res[0]:
				if 0 <= args['day_order'] <= 5:
					data = pd.read_csv(info_path)
					data['day_order'] = int(args["day_order"])
					data['working_day'] = (True if(0 < args["day_order"] <= 5) else False)
					time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
					data['lastupdated'] = time_now
					data.to_csv(info_path, index=False)
					return data.to_dict(), 200
				else:
					return {
						'message': f"day_order arg passed ({args['day_order']}) has a range of 0-5."
					}, 409
			else:
				return{
					'message': res[1]
				}, res[2]

# set 'info' class at 'info' endpoint


api.add_resource(info, '/info')

if __name__ == "__main__":
	app.run(threaded=True, port=5000, debug=True)