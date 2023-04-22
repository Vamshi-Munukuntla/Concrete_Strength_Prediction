import pickle

import pandas as pd
import streamlit as st

df = pd.read_csv('EDA_Files/Concrete_without_Outliers.csv')

# preprocessor = pickle.load(open('preprocessed.pkl', 'rb'))
# model = pickle.load(open('model.pkl', 'rb'))

with open('preprocessed.pkl', 'rb') as preprocessed_file:
    preprocessed = pickle.load(preprocessed_file)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.set_page_config(page_title="Concrete Compressive Strength Prediction", page_icon=":hammer_and_wrench:")
st.title("Concrete Compressive Strength Prediction")

# Create input fields for user to input feature values
Cement = st.slider("Cement (kg/m3)", min_value=float(df['Cement'].min()), max_value=df['Cement'].max())
Blast_Furnace_Slag = st.slider("Blast_Furnace_Slag (kg/m3)", min_value=float(df['Furnace_Slag'].min()),
                               max_value=df['Furnace_Slag'].max())
Fly_Ash = st.slider("Fly_Ash (kg/m3)", min_value=float(df['Fly_Ash'].min()), max_value=df['Fly_Ash'].max())
Water = st.slider("Water (kg/m3)", min_value=float(df['Water'].min()), max_value=df['Water'].max())
Superplasticizer = st.slider("Superplasticizer (kg/m3)", min_value=float(df['Superplasticizer'].min()),
                             max_value=df['Superplasticizer'].max())
Coarse_Aggregate = st.slider("Coarse_Aggregate (kg/m3)", min_value=float(df['Coarse_Aggregate'].min()),
                             max_value=df['Coarse_Aggregate'].max())
Fine_Aggregate = st.slider("Fine_Aggregate (kg/m3)", min_value=float(df['Fine_Aggregate'].min()),
                           max_value=df['Fine_Aggregate'].max())
Age_in_days = st.slider("Age (days)", min_value=0, max_value=180, step=1)

input_data = {'Cement': Cement,
              'Blast_Furnace_Slag': Blast_Furnace_Slag,
              'Fly_Ash': Fly_Ash,
              'Water': Water,
              'Superplasticizer': Superplasticizer,
              'Coarse_Aggregate': Coarse_Aggregate,
              'Fine_Aggregate': Fine_Aggregate,
              'Age_in_days': Age_in_days}


df = pd.DataFrame([input_data])
cols = df.columns
st.dataframe(df)

# # Performing preprocessing steps on the new data.
# preprocessed_data = pd.DataFrame(preprocessed.transform(df), columns=cols)

# Predicting the Compressive Strength of Concrete.
y_pred = model.predict(df)


if st.button('Show Results'):
    st.header(f'{round(y_pred[0], 2)} MPa')
