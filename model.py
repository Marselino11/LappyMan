import pickle

global dataset, model, aplikasi, budget, list_apk, list_biaya

def load():
    global dataset, model, aplikasi, budget, laptop
    dataset = pickle.load(open('static/model/dataset.pkl', 'rb'))
    model = pickle.load(open('static/model/model.pkl', 'rb'))
    aplikasi = pickle.load(open('static/model/aplikasi.pkl','rb'))
    budget = pickle.load(open('static/model/budget.pkl','rb'))
    laptop = pickle.load(open('static/model/laptop.pkl','rb'))

def prediksi(app_list, budget_list):
    global list_apk, list_biaya, rek_laptop
    list_apk= app_list
    list_biaya=budget_list
    word = ""
    stat = 0
    listapp = []
    for i in app_list:
        if i == "'" and stat==0:
            stat = 1
        elif i == "'" and stat==1:
            listapp.append(word)
            stat = 0
            word = ""
        elif i != "[" and i != ']' and i != ',':
            word = word + i
    kata = listapp[1]
    kata = kata[1:]
    listapp[1] = kata
    kata = listapp[2]
    kata = kata[1:]
    listapp[2] = kata
    app1 = aplikasi.transform([listapp[0]])
    app2 = aplikasi.transform([listapp[1]])
    app3 = aplikasi.transform([listapp[2]])
    bud = budget.transform([str(budget_list)])
    rekomendasi = model.predict([[int(app1),int(app2),int(app3),int(bud)]])
    reklaptop = laptop.inverse_transform([rekomendasi])

    return reklaptop


def rekomendasi(rek_laptop):
    number_of_recommendations = 4
    cosine = pickle.load(open('static/model/cosine.pkl','rb'))
    index = dataset[dataset['brand']==rek_laptop].index.values[0]
    similarity_scores = list(enumerate(cosine[index]))
    similarity_scores_sorted = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommendations_indices = [t[0] for t in similarity_scores_sorted[1:(number_of_recommendations+1)]]

    return recommendations_indices