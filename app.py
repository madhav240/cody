from flask import Flask, render_template, request,  jsonify
from utils import *
import os
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == "POST":
		data = request.get_data(cache=False).decode("utf-8") 
		if 'X-File-Name' not in request.headers.keys():
			return getdoc(data)
		else:
			html = gethtml(data, request.headers['X-File-Name'])
			return jsonify(html)

	return render_template('base.html', data=",".join(os.listdir("docs")))

if __name__ == '__main__':
    app.run()