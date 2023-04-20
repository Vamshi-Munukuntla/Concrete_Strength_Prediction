import pickle

import pandas as pd
import streamlit as st

model = pickle.load(open('saved_models/20230420035450/model.pkl', 'rb'))

st.title('Concrete Compressive Strength Prediction')

Cement = st.number_input('Please enter Cement value: ')

Blast_Furnace_Slag = st.number_input('Please enter Blast_Furnace_Slag value: ')

Fly_Ash = st.number_input('Please enter Fly_Ash value: ')

Water = st.number_input('Please enter Water value: ')

Superplasticizer = st.number_input('Please enter Superplasticizer value: ')

Coarse_Aggregate = st.number_input('Please enter Coarse_Aggregate value: ')

Fine_Aggregate = st.number_input('Please enter Fine_Aggregate value: ')

Age_in_days = st.number_input('Please enter Age_in_days value: ')


inputs = {'cement': Cement,
          'Blast_Furnace_Slag': Blast_Furnace_Slag,
          'Fly_Ash': Fly_Ash, 'Water': Water,
          'Superplasticizer': Superplasticizer,
          'Coarse_Aggregate': Coarse_Aggregate,
          'Fine_Aggregate': Fine_Aggregate,
          'Age_in_days': Age_in_days}

df = pd.DataFrame(inputs, index=[0])

y_pred = model.predict(df)
st.write(y_pred)
if st.button("Show Results"):
    st.header(f"{round(y_pred, 2)}")
