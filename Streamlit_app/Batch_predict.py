import shutil

import streamlit as st
from concrete.exception import CustomException
from concrete.pipeline.Batch_Prediction import Batch_Prediction
import requests
from concrete.constant import *
import sys


import streamlit as st
import os
import shutil

# Create a function to handle the file upload
# def upload_csv():
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="csv_upload")
#
#     if uploaded_file is not None:
#         # Save the uploaded file to a temporary location
#         with open(os.path.join("temp", uploaded_file.name), "wb") as f:
#             f.write(uploaded_file.getbuffer())
#
#         # Move the uploaded file to the desired location
#         shutil.move(os.path.join("temp", uploaded_file.name), os.path.join("uploads", uploaded_file.name))


def batch_predict():
    try:
        file = st.file_uploader("Choose a file")
        folder = PREDICTION_DATA_SAVING_FOLDER_KEY

        if file is not None:
            st.success('File Uploaded Successfully.')

            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)

            with open(os.path.join(folder, file.name), 'wb') as f:
                f.write(file.getbuffer())

            pred = Batch_Prediction()
            output_file = pred.initiate_bulk_prediction()
            st.markdown('First five rows of predicted data')
            st.write(output_file.head())
            st.success("Prediction file generated.")

            @st.cache_data
            def convert_df(data):
                return data.to_csv(index=False)

            csv_file = convert_df(output_file)

            # Download the data
            st.download_button(
                label="Download Concrete Batch Predicted File",
                data=csv_file,
                file_name='Concrete_batch_predicted.csv',
                mime='text/csv',
            )

    except Exception as e:
        raise CustomException(e, sys) from e
