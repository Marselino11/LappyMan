from flask import Flask, render_template, request, redirect, url_for, g
import pickle
import numpy as np
import pandas as pd
from model import load, prediksi, rekomendasi

app = Flask(__name__)

global dataset
dataset = pickle.load(open('static/model/dataset.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('homescreen.html')

load()

@app.route('/build', methods=['GET','POST'])
def build():
    if request.method == 'POST':
        applist = request.form.getlist('category')
        budgetlist = request.form.get('budget')
        # user(applist, budgetlist)
        return redirect(url_for('predict',app_list=applist,budget_list=budgetlist))
    else:
        return render_template('screen2.html',request_method=request.method)


@app.route('/build/predict/<app_list>/<budget_list>')
def predict(app_list,budget_list):
    hasil_rekomendasi = prediksi(app_list, budget_list)

    for a in hasil_rekomendasi:
        index = dataset[dataset['brand']==a].index.values[0]
    kol1 = dataset.loc[index,'processor_brand']
    kol2 = dataset.loc[index,'processor_name']
    kol3 = dataset.loc[index,'graphic']
    kol4 = dataset.loc[index,'ram_gb']
    kol5 = dataset.loc[index,'ram_type']
    kol6 = dataset.loc[index,'ssd']
    kol7 = dataset.loc[index,'hdd']
    kol8 = dataset.loc[index,'os']
    kol9 = dataset.loc[index,'battery']
    kol10 = dataset.loc[index,'display_size']
    kol11 = dataset.loc[index,'price']
    
    lappy = dataset.loc[index,'brand']
    coba(lappy)
    return render_template('screen3.html', hasil = hasil_rekomendasi,  kol_1=kol1, kol_2 = kol2, kol_3 =kol3, kol_4=kol4, kol_5=kol5, kol_6=kol6, kol_7=kol7, kol_8=kol8, kol_9=kol9, kol_10=kol10, kol_11=kol11)
           
global nilai
def coba(hasil):
    global nilai
    nilai = hasil
    return nilai
    

@app.route('/build/predict/')
def recommendations():
    laptop = nilai
    recommen = rekomendasi(laptop)

    data1 = dataset.loc[recommen[0], 'brand']
    data2 = dataset.loc[recommen[1], 'brand']
    data3 = dataset.loc[recommen[2], 'brand']
    data4 = dataset.loc[recommen[3], 'brand']
    
    return render_template('screen4.html', rekomen=recommen, ke1=data1, ke2=data2, ke3=data3, ke4=data4)

@app.route('/closing')
def close():
    return render_template('Closing.html')

if __name__ == "__main__":
    app.run(debug=True)
