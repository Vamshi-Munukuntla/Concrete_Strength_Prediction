import shutil

import streamlit as st
from concrete.exception import CustomException
from concrete.pipeline.Batch_Prediction import Batch_Prediction
import requests
from concrete.constant import *
import sys


def bulk_predict():
    try:
        file = st.file_uploader("Choose a file")
        folder = PREDICTION_DATA_SAVING_FOLDER_KEY

        if file is not None:
            st.success('File Uploaded Successfully.')

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
