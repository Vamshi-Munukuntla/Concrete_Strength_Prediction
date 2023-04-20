import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the pre-trained model
with open('preprocessed.pkl', 'rb') as preprocessed_file:
    preprocessed = pickle.load(preprocessed_file)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the features of the model
features = ['Cement', 'Blast_Furnace_Slag', 'Fly_Ash', 'Water', 'Superplasticizer',
            'Coarse_Aggregate', 'Fine_Aggregate', 'Age_in_days']


# Define the function to make a prediction
def predict_concrete_strength(Cement, Blast_Furnace_Slag, Fly_Ash, Water, Superplasticizer,
                              Coarse_Aggregate, Fine_Aggregate, Age_in_days):

    input_data = np.array([[Cement, Blast_Furnace_Slag, Fly_Ash, Water, Superplasticizer,
                            Coarse_Aggregate, Fine_Aggregate, Age_in_days]])

    data_preprocessing = preprocessed.transform(input_data)
    prediction = model.predict(data_preprocessing)[0]
    return prediction


# Define the Streamlit app
def app():
    st.set_page_config(page_title="Concrete Strength Prediction", page_icon=":hammer_and_wrench:")

    st.title("Concrete Strength Prediction")

    # Create input fields for user to input feature values
    Cement = st.number_input("Cement (kg/m3)", min_value=0, max_value=1000, value=250)
    Blast_Furnace_Slag = st.number_input("Blast_Furnace_Slag (kg/m3)", min_value=0, max_value=1000, value=0)
    Fly_Ash = st.number_input("Fly_Ash (kg/m3)", min_value=0, max_value=1000, value=0)
    Water = st.number_input("Water (kg/m3)", min_value=0, max_value=1000, value=185)
    Superplasticizer = st.number_input("Superplasticizer (kg/m3)", min_value=0, max_value=100, value=0)
    Coarse_Aggregate = st.number_input("Coarse_Aggregate (kg/m3)", min_value=0, max_value=2000, value=1115)
    Fine_Aggregate = st.number_input("Fine_Aggregate (kg/m3)", min_value=0, max_value=1000, value=670)
    Age_in_days = st.number_input("Age_in_days", min_value=1, max_value=365, value=28)

    # Make a prediction using the function defined earlier
    prediction = predict_concrete_strength(Cement, Blast_Furnace_Slag, Fly_Ash, Water, Superplasticizer,
                                           Coarse_Aggregate, Fine_Aggregate, Age_in_days)

    # Display the prediction
    st.write(f"The predicted concrete strength is {prediction:.2f} MPa.")


if __name__ == '__main__':
    app()
