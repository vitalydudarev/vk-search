import vk_api
import config
from flask import Flask, render_template, request

app = Flask(__name__)
config = config.load_config('config.json')

@app.route("/")
def hello():
    return render_template("search.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    if request.method == 'POST':
    	api = vk_api.VkApi(config.access_token, config.proxy)
    	query = request.form['value']
        return api.search(query)

if __name__ == "__main__":
    app.run(debug=True)