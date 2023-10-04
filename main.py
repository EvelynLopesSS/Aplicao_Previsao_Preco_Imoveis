from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
from mapping import cidade_mapping, bairro_mapping, tipo_imovel_mapping, andar_mapping, status_mapping
from babel.numbers import format_currency

app = Flask(__name__)


def predict_price(Area, Beira_Mar, Valor_M, Closet, Qtde_Quartos, Qtde_Suites, WC, DCE, Vaga_Garagem,
                  Elevador, Portaria_24h, Gerador, Central_Gas, Bicicletario, Cidade_encoded, Bairro_encoded,
                  Tipo_Imovel_encoded, Andar_encoded, Status_encoded):
    
    model = joblib.load('Imoveismodelo.pkl')

    example = [[Area, Beira_Mar, Valor_M, Closet, Qtde_Quartos, Qtde_Suites, WC, DCE, Vaga_Garagem,
                Elevador, Portaria_24h, Gerador, Central_Gas, Bicicletario, Cidade_encoded, Bairro_encoded,
                Tipo_Imovel_encoded, Andar_encoded, Status_encoded]]

    predicted_price = model.predict(example)

    return predicted_price[0]


@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    formatted_price = None
    if request.method == 'POST':
        Area = int(request.form['Area'])
        Beira_Mar = int(request.form['Beira_Mar'])
        Valor_M = int(request.form['Valor_M'])
        Closet = int(request.form['Closet'])
        Qtde_Quartos = int(request.form['Qtde_Quartos'])
        Qtde_Suites = int(request.form['Qtde_Suites'])
        WC = int(request.form['WC'])
        DCE = int(request.form['DCE'])
        Vaga_Garagem = int(request.form['Vaga_Garagem'])
        Elevador = int(request.form['Elevador'])
        Portaria_24h = int(request.form['Portaria_24h'])
        Gerador = int(request.form['Gerador'])
        Central_Gas = int(request.form['Central_Gas'])
        Bicicletario = int(request.form['Bicicletario'])
        Cidade_encoded = int(request.form['Cidade_encoded'])
        Bairro_encoded = int(request.form['Bairro_encoded'])
        Tipo_Imovel_encoded = int(request.form['Tipo_Imovel_encoded'])
        Andar_encoded = int(request.form['Andar_encoded'])
        Status_encoded = int(request.form['Status_encoded'])
        

      
        predicted_price = predict_price(Area, Beira_Mar, Valor_M, Closet, Qtde_Quartos, Qtde_Suites, WC, DCE,
                                        Vaga_Garagem, Elevador, Portaria_24h, Gerador, Central_Gas, Bicicletario,
                                        Cidade_encoded, Bairro_encoded, Tipo_Imovel_encoded, Andar_encoded,
                                        Status_encoded)
        
        formatted_price = format_currency(predicted_price, 'BRL', locale='pt_BR')
        

    return render_template('index.html', cidade_options=cidade_mapping, bairro_options=bairro_mapping, tipo_imovel_options=tipo_imovel_mapping, andar_options=andar_mapping, status_options=status_mapping, predicted_price=formatted_price)

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=36)
