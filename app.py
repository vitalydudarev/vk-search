import vk_api
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("search.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template("s.html")
    if request.method == 'POST':
    	api = vk_api.VkApi("")
    	req_text = request.form['value']
        return "[{\"link\":\"http://cs422619.vk.me/u3504388/audios/6738a49929d7.mp3?extra=0AInPNc4OrsJ0fL4TVLB96WYW3FxkP_HDZzB9mHzNVwPddA6nPdfGddcK_gFbvoQX6yrCltxOm_ZbOVxm1i1hSAsKn1Fhp95bYtzlBPa219sA5eyLXq9DaDv7wxedL8BY2zd3K4v8sG2\", \"title\":\"A State of Trance Episode 720 (2015-07-02)\"}]"
        #return api.search(req_text)

if __name__ == "__main__":
    app.run(debug=True)