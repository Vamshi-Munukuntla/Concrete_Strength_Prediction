import streamlit as st
from PIL import Image


def model_building():

    st.subheader('Machine Learning')
    image = Image.open('Streamlit_app/Images/ML_Process.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader('Model Building')
    st.write('Model Building is performed using 7 Algorithms.')
    image = Image.open('Streamlit_app/Images/ML_models.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader('Regression Metrics')
    st.write('R2_Score and Root Mean Squared Error (RMSE) as used as model evaluation metrics.')
    st.write()

    st.subheader("Results")
    st.write('Model Building is performed using 7 Algorithms.')
    image = Image.open('Streamlit_app/Images/Model_output_2.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader("Hyperparameter Tuning")
    st.write("From above results, we can conclude Random Forest and XGBoost performs better than other models.")
    st.write("So, hyperparameter tuning is performed on these two algorithms to get the best possible estimators.")
    st.write()

    # Random Forest

    st.markdown('##### Random Forest:')
    st.write('Hyperparameter Tuning parameters: ')
    image = Image.open('Streamlit_app/Images/random_forest_hp_params.png')
    st.image(image, use_column_width=False)
    st.write()

    st.write('Best Parameters: ')
    image = Image.open('Streamlit_app/Images/Random_Forest_best_params.png')
    st.image(image, use_column_width=False)
    st.write()

    # XGBoost

    st.markdown('##### XGBoost:')
    st.write('Hyperparameter Tuning parameters: ')
    image = Image.open('Streamlit_app/Images/XGBoost_hp_params.png')
    st.image(image, use_column_width=False)
    st.write()

    st.write('Best Parameters: ')
    image = Image.open('Streamlit_app/Images/XGBoost_best_params.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader('Final Results:')
    image = Image.open('Streamlit_app/Images/Model_output_3.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader('R2 Score')
    image = Image.open('Streamlit_app/Images/r2_score_plot.png')
    st.image(image, use_column_width=False)
    st.write()

    st.subheader('RMSE:')
    image = Image.open('Streamlit_app/Images/rmse_plot.png')
    st.image(image, use_column_width=False)
    st.write()

