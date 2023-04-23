import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def EDA():
    df = pd.read_csv('Concrete_Data.csv')

    st.subheader('Shape of the dataset:')
    st.write(f' - Number of Rows in the dataset: {df.shape[0]}')
    st.write(f' - Number of Columns in the dataset: {df.shape[1]}')

    # First 5 rows
    st.subheader('Top 5 Rows')
    st.dataframe(df.head())

    # dtypes
    st.subheader('Data Type of each column')
    st.write(df.dtypes)

    # Descriptive analysis
    st.subheader('Descriptive Analysis')
    st.write(df.describe())

    # Are mean median values similar?
    st.subheader('Are mean and median values similar?')
    image = Image.open('Streamlit_app/Images/EDA_1.png')
    st.image(image, use_column_width=False)
    st.write('**Few Insights:**')
    st.write("1. Furnace_Slag, Fly_Ash and Age has high difference in mean and median, which means these three "
             "columns may have outliers. Box plot would reveal more details about it.")

    st.write("2. Water and Superplasticizer has negligible difference in mean and median, so, mean and median can be "
             "used interchangeably for these features.")

    st.write("3. Remaining features have slight difference, further analysis will provide more information about these "
             "features.")

    # Uni variate Analysis
    st.subheader('Uni-Variate Analysis')
    image = Image.open('Streamlit_app/Images/EDA_2.png')
    st.image(image, use_column_width=True)
    st.write('**Few Insights:**')
    st.write("1. Furnace Slag, Fly Ash, Superplaticizer and Age are highly skewed.")
    st.write("2. All the features  are at different scales.")

    # Boxen plot
    st.subheader('Boxen Plot')
    image = Image.open('Streamlit_app/Images/EDA_3.png')
    st.image(image, use_column_width=True)
    st.write('**Few Insights:**')
    st.write("1. It shows how the data is distributed.")
    st.write("2. Cement mostly lie between 180 to 350")
    st.write("3. Fly Ash mostly between 0 to 120")
    st.write("4. Superplaticizer mostly between 0 to 10")
    st.write("5. Age contains quite a lot outliers, it's highly right skewed.")

    # Hex Bin plot
    st.subheader('HexBin Plot')
    image = Image.open('Streamlit_app/Images/EDA_4.png')
    st.image(image, use_column_width=True)
    st.write('**Few Insights:**')
    st.write("1. It shows the density of the input and target columns.")

    # CDF (Cumulative Distribution Function)
    st.subheader('Cumulative Distribution Function (CDF)')
    image = Image.open('Streamlit_app/Images/EDA_5.png')
    st.image(image, use_column_width=True)
    st.write('**Few Insights:**')
    st.write("1. There are lot of zeros in Furnace Slag, Fly Ash and superplaticizer.")

    # Heatmap
    st.subheader('Heatmap')
    image = Image.open('Streamlit_app/Images/EDA_6.png')
    st.image(image, use_column_width=True)
    st.write('**Few Insights:**')
    st.write('There is no collinearity between features.')
