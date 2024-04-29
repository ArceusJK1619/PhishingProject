from flask import Flask, request, jsonify, render_template
from process import predict

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    prediction =""
    image = "default.jpg"
    if request.method == "POST":
        url = str(request.form['url'])
        if len(url) > 0:
            prediction,color,image= predict(url)
        #do proccess with url here.
        if len(prediction)>0:
            return render_template('index.html', prediction = prediction, color = color,image = image)
        else:
            return render_template('index.html',image = image)
    else:
        return render_template('index.html',image= image)

if __name__ == '__main__':
    app.run(debug=True)