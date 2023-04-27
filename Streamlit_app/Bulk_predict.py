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

            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)

            with open(os.path.join(folder, file.name), 'wb') as f:
                f.write(file.getbuffer())
            st.success('File Saved Successfully.')

            pred = Batch_Prediction()
            output_file = pred.initiate_bulk_prediction()
            path = os.path.basename(output_file)

            st.success("Prediction file generated.")

            if st.button("Open File Location Path"):
                if os.path.isdir(os.path.dirname(output_file)):
                    os.system(f"open '{os.path.dirname(output_file)}'")
                else:
                    st.error(f"'{os.path.dirname(output_file)}' is not a valid directory")
                return st.write(os.path.dirname(output_file))

    except Exception as e:
        raise CustomException(e, sys) from e
