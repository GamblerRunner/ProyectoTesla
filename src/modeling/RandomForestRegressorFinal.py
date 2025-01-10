import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

hiperparametros = {
    'profundidad': 10,
    'criterio': 'poisson',
    'estimator': 50
}

def obtener_df():
    df = pd.read_csv('./data/full_cleaned_data.csv')
    df.drop(columns=["Unnamed: 0"], inplace=True)
    df.drop_duplicates(inplace=True)
    return df


def modelo_rfr(hiperparametros):
    rfr = RandomForestRegressor(n_estimators=hiperparametros['estimator'], criterion=hiperparametros['criterio'], max_depth=hiperparametros['profundidad'], random_state=1337)
    rfr.fit(X_train, y_train)
    return rfr


df = obtener_df()

X = df.drop(columns=['price'])  # Elimina la columna objetivo del conjunto de características
y = df['price']  # Define la variable objetivo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1337)


rfr = modelo_rfr(hiperparametros=hiperparametros)
predicciones = rfr.predict(X_test)

X_test['predicted_price'] = predicciones
X_test['real_price'] = df.loc[X_test.index, 'price']

X_test.to_csv('./src/modeling/modeling_results.csv')