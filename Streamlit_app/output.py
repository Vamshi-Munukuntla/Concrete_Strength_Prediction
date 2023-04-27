import pickle

import numpy as np
import pandas as pd
import streamlit as st


def app():
    df = pd.read_csv('EDA_Files/Data/Concrete_without_Outliers.csv')

    with open('concrete_pickle/model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    # Create input fields for user to input feature values
    Cement = st.slider("Cement (kg/m3)", min_value=float(df['Cement'].min()), max_value=df['Cement'].max(),
                       value=320.00)

    Blast_Furnace_Slag = st.slider("Blast_Furnace_Slag (kg/m3)", min_value=float(df['Furnace_Slag'].min()),
                                   max_value=df['Furnace_Slag'].max(), value=160.0)

    Fly_Ash = st.slider("Fly_Ash (kg/m3)", min_value=float(df['Fly_Ash'].min()),
                        max_value=df['Fly_Ash'].max(), value=10.0)

    Water = st.slider("Water (kg/m3)", min_value=float(df['Water'].min()), max_value=df['Water'].max(), value=165.35)
    Superplasticizer = st.slider("Superplasticizer (kg/m3)", min_value=float(df['Superplasticizer'].min()),
                                 max_value=df['Superplasticizer'].max(), value=3.0)
    Coarse_Aggregate = st.slider("Coarse_Aggregate (kg/m3)", min_value=float(df['Coarse_Aggregate'].min()),
                                 max_value=df['Coarse_Aggregate'].max(), value=976.0)
    Fine_Aggregate = st.slider("Fine_Aggregate (kg/m3)", min_value=float(df['Fine_Aggregate'].min()),
                               max_value=df['Fine_Aggregate'].max(), value=720.00)
    Age_in_days = st.slider("Age (days)", min_value=0, max_value=180, step=1, value=90)

    input_data = {'Cement': Cement,
                  'Blast_Furnace_Slag': Blast_Furnace_Slag,
                  'Fly_Ash': Fly_Ash,
                  'Water': Water,
                  'Superplasticizer': Superplasticizer,
                  'Coarse_Aggregate': Coarse_Aggregate,
                  'Fine_Aggregate': Fine_Aggregate,
                  'Age_in_days': Age_in_days}

    # st.subheader('Reference Data: ')
    # st.dataframe(df.sample(5, random_state=0))

    df = pd.DataFrame([input_data])
    cols = df.columns
    st.dataframe(df)

    # Predicting the Compressive Strength of Concrete.
    y_pred = model.predict(df)

    if st.button('Show Results'):
        st.header(f'Compressive Strength: {round(y_pred[0], 2)} MPa')
