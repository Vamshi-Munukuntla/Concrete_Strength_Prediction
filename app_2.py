import pickle

import pandas as pd
import streamlit as st

# preprocessor = pickle.load(open('preprocessed.pkl', 'rb'))
# model = pickle.load(open('model.pkl', 'rb'))

with open('preprocessed.pkl', 'rb') as preprocessed_file:
    preprocessed = pickle.load(preprocessed_file)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.set_page_config(page_title="Concrete Strength Prediction", page_icon=":hammer_and_wrench:")
st.title("Concrete Strength Prediction")

# Create input fields for user to input feature values
Cement = st.number_input("Cement (kg/m3)", min_value=0, max_value=1000, value=198)
Blast_Furnace_Slag = st.number_input("Blast_Furnace_Slag (kg/m3)", min_value=0, max_value=1000, value=132)
Fly_Ash = st.number_input("Fly_Ash (kg/m3)", min_value=0, max_value=1000, value=0)
Water = st.number_input("Water (kg/m3)", min_value=0, max_value=1000, value=192)
Superplasticizer = st.number_input("Superplasticizer (kg/m3)", min_value=0, max_value=100, value=0)
Coarse_Aggregate = st.number_input("Coarse_Aggregate (kg/m3)", min_value=0, max_value=2000, value=978)
Fine_Aggregate = st.number_input("Fine_Aggregate (kg/m3)", min_value=0, max_value=1000, value=825)
Age_in_days = st.number_input("Age_in_days", min_value=1, max_value=365, value=90)

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
st.write("data: ")
st.dataframe(df)

preprocessed_data = pd.DataFrame(preprocessed.transform(df), columns=cols)

y_pred = model.predict(preprocessed_data)
print(y_pred[0])
st.write(y_pred[0])
