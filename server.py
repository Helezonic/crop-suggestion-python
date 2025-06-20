from flask import Flask, render_template, request, redirect, url_for, jsonify
from sklearn.neighbors import KNeighborsClassifier
app = Flask(__name__)

_code = ""
@app.route('/')
def index2():
    return render_template('index.html')

@app.route('/Register')
def Register():
    return render_template('register.html')

@app.route("/users/index", methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route("/users/graph", methods=["GET", "POST"])
def login():
    return render_template('chart.html')

@app.route("/users/logs", methods=["GET", "POST"])
def logs():
    return render_template('logs.html')

@app.route("/users/analyse", methods=["POST"])
def analyse():
    if(request.method == "POST"):
        import pandas as pd
        import numpy as np
        import os
        # Check if running locally or on Vercel
        if os.getenv("ENV") == "production":
            # Load files from Vercel's static hosting
            optimum = pd.read_csv("./optimum1.csv")
            price = pd.read_csv("./optimum2.csv") 
        else:
            # Load files from local directory
            optimum = pd.read_csv("./optimum1.csv")
            price = pd.read_csv("./optimum2.csv")


        optimum['N'] = optimum.N.astype(float)
        optimum['P'] = optimum.P.astype(float)
        optimum['K'] = optimum.K.astype(float)
        optimum['TEMPERATURE'] = optimum.TEMPERATURE.astype(float)
        X= optimum.drop("CLASS", axis=1)
        y= optimum.CLASS

        from sklearn.neighbors import KNeighborsClassifier
        clf = KNeighborsClassifier(n_neighbors=3)
        clf.fit(X,y)

        data = request.json
        print(f"Received data: {data}")
        nitrogen = data.get('nitrogen')
        phosphorous = data.get('phosphorous')
        potassium = data.get('potassium')
        temperature = data.get('temperature')
        pH = data.get('pH')

        if not data:
            return {"error": "All soil parameters required"}


        else:
            
            columns = ['N', 'P', 'K', 'pH', 'TEMPERATURE']
            values = np.array([nitrogen, phosphorous, potassium, pH, temperature])
            pred = pd.DataFrame(values.reshape(-1, len(values)), columns=columns)

            print(pred)

            prediction = clf.predict(pred)
            print(f"prediction : {prediction}")

            optimum = optimum[optimum['CLASS'] != prediction[0]]
            X = optimum.drop("CLASS", axis=1)
            y = optimum.CLASS
            clf = KNeighborsClassifier(n_neighbors=3)
            clf.fit(X,y)
            prediction1 = clf.predict(pred)
            print(f"prediction1 : {prediction1}")

            optimum = optimum[optimum['CLASS'] != prediction1[0]]
            X = optimum.drop("CLASS", axis=1)
            y = optimum.CLASS
            clf = KNeighborsClassifier(n_neighbors=3)
            clf.fit(X,y)
            prediction2 = clf.predict(pred)
            print(f"prediction2 : {prediction2}")

            p1 = prediction1[0]
            p2 = prediction2[0]
            p1 = p1 -1
            p2 = p2 -1

            if(prediction == 7):
                return render_template('crops.html', crop="Tomato" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 1):
                return render_template('crops.html', crop="Garlic" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 2):
                return render_template('crops.html', crop="Onion" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 3):
                return render_template('crops.html', crop="Orange" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 4):
                return render_template('crops.html', crop="Peas" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 5):
                return render_template('crops.html', crop="Potato" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 6):
                return render_template('crops.html', crop="Rice" , crop1=prediction1[0], crop2=prediction2[0])
                
            elif(prediction == 8):
                return render_template('crops.html', crop="Sugarcane" , crop1=prediction1[0], crop2=prediction2[0])
                
            
                
            
            return jsonify({
            "success": True,
            "redirect": "/crops.html",
            "message": "Analysis complete"
        })

        
    

if (__name__ == "__main__"):
    app.run()