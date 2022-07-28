import joblib
import numpy as np
from flask import request, Flask,render_template


app=Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/cancer")
def cancer():
    return render_template("cancer.html")


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    loaded_model = joblib.load("cancer_model")
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list, 30)
    try:
        if(int(result)==1):
            prediction='You may have Cancer'
        else:
            prediction='You are Healthy'
    except TypeError:
        prediction = 'You are healthy' 
    return(render_template("result.html", prediction=prediction))


if __name__ == "__main__":
    app.run(debug=True)
