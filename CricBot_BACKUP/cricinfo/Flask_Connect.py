# Flask_Connect.py
from flask import Flask, request, jsonify
from a import GetAns
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
chatBot = GetAns()

@app.route('/getAns', methods=["POST"])
def home():
    payload = request.get_json()
    prompt = payload.get('prompt', '')
    resp = chatBot.getValue(prompt=prompt).get('pageProps', {}).get('parsedData', {})
    if 'errorMessage' in resp:
        return jsonify({'message': 'error', 'error': resp['errorMessage']}), 400
    
    data_list = resp.get('scrappedData', {}).get('data', {}).get('cmpData', {}).get('parsedData', [])
    filters_str = resp.get('scrappedData', {}).get('filtersData', '')
    limited = data_list[:5]
    combined = [{'row': item, 'filters': filters_str} for item in limited]
    return jsonify({'message': 'success', 'data': combined}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)












# # Flask_Connect.py
# from flask import Flask, request, jsonify
# from a import GetAns
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# chatBot = GetAns()

# @app.route('/getAns', methods=["POST"])
# def home():
#     payload = request.get_json()
#     prompt = payload.get('prompt', '')
#     all_data = chatBot.getValue(prompt=prompt)\
#         .get('pageProps', {})\
#         .get('parsedData', {})\
#         .get('scrappedData', {})\
#         .get('data', {})\
#         .get('cmpData', {})\
#         .get('parsedData', [])
#     limited = all_data[:5]
#     return jsonify({'message': 'success', 'data': limited}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8080)













# from flask import Flask,request,jsonify
# from a import GetAns
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# chatBot = GetAns()


# def formList(data):
#   list = []
#   for value in data:
#     if value=='Details':
#       for key in data['Details']:
#         list.append(data['Details'][key]);
#     else:
#       list.append(data[value])

#   return list


# @app.route('/getAns',methods=["POST"])
# def home():
#   data = request.get_json()
#   prompt = data['prompt']
#   print(prompt)
#   # query = chatBot.getValue(prompt=prompt)['pageProps']['parsedData']['query']
#   data = chatBot.getValue(prompt=prompt)['pageProps']['parsedData']['scrappedData']['data']['cmpData']['parsedData']

#   res = list(map(lambda x: 
#       formList(x)
#   ,data))
#   print(res)

#   # data = query, result
  
#   return jsonify({'message':'sucess','data':res}),200

# if __name__== '__main__':
#   app.run(host='0.0.0.0',debug=True,port=8080)