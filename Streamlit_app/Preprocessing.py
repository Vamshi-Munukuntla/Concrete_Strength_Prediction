import streamlit as st
from PIL import Image


def Preprocessing():
    st.subheader('Preprocessing Steps:')
    image = Image.open('Streamlit_app/Images/Preprocessing_Steps_1.png')
    st.image(image, use_column_width=True)

    # Outlier Detection
    st.subheader('Outlier Detection:')
    st.write("1. Check the distribution of the data and the outliers in the feature.")
    image = Image.open('Streamlit_app/Images/Outlier_Detection_1.png')
    st.image(image, use_column_width=True, caption='Checking the distribution for Water Feature.')

    st.write("2. Depending on the distribution, we choose limits either by Gaussian, IQR or Winsorization method.")
    image = Image.open('Streamlit_app/Images/Outlier_Detection_3.png')
    st.image(image, use_column_width=False, caption='Checking the distribution for Water Feature.')

    st.write("3. Then we cap the outliers by upper and lower limits.")
    image = Image.open('Streamlit_app/Images/Outlier_Detection_2.png')
    st.image(image, use_column_width=True, caption='Distribution of Water, before and after capping the outliers.')

    st.write("4. Same process is followed for all the features.")

    st.markdown("###### Note: For detailed analysis, custom defined functions to detect and cap the outliers, "
                "please check the Jupyter Notebook here: [00_Concrete.ipynb]("
                "https://github.com/Vamshi-Munukuntla/Concrete_Strength_Prediction/blob/main/EDA_Files/00_Concrete"
                ".ipynb)")
    st.write('')
    st.write('')

    # Variable Transformation
    st.subheader('Variable Transformation:')
    st.write("Nearly all the features are skewed, Some ML models assume features to follow normal distribution. "
             "Feature Transformation is must.")
    st.write("1. Check the distribution of the data using Q-Q plots or histograms.")
    image = Image.open('Streamlit_app/Images/variable_transformation_1.png')
    st.image(image, use_column_width=True, caption='Checking the distribution for Age Feature.')

    st.write("2. Perform the transformation and check the distribution and skewness of the feature.")
    image = Image.open('Streamlit_app/Images/variable_transformation_2.png')
    st.image(image, use_column_width=False, caption='Checking the Skewness for every transformation.')

    st.write("3. Distribution of data, after transformation.")
    image = Image.open('Streamlit_app/Images/variable_transformation_3.png')
    st.image(image, use_column_width=True, caption='Distribution of Age, after applying Yeo-Johnson transformation.')

    st.markdown("###### Note: For detailed analysis, custom defined functions for all the transformations "
                "and for all the features, please check the Jupyter Notebook here: [01_Concrete.ipynb]("
                "https://github.com/Vamshi-Munukuntla/Concrete_Strength_Prediction/blob/main/EDA_Files"
                "/01_Concrete_Variable_transformation.ipynb)")

    # Scaling
    st.subheader('Scaling')
    st.write('Some Machine Learning models are sensitive to scale of the features. ')
    st.write('Larger magnitude features dominate over the smaller magnitude features. '
             'So, Scaling the features provides better results for some models.')
    st.write('**MinMaxScaler()** is applied for all the features.')



