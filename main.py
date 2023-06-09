import streamlit as st

from Streamlit_app.EDA import EDA
from Streamlit_app.Problem_Statement import Problem_Statement
from Streamlit_app.output import app
from Streamlit_app.Preprocessing import Preprocessing
from Streamlit_app.Model_Building import model_building
from Streamlit_app.Batch_predict import batch_predict

st.set_page_config(page_title="Concrete Compressive Strength Prediction",
                   page_icon=":hammer_and_wrench:", layout="wide")
st.title("Concrete Compressive Strength Prediction")


def main():
    activities = ['Problem Statement', 'EDA', 'Feature Engineering',
                  "Model Building", 'Single Prediction', "Batch Prediction"]
    option = st.sidebar.radio('Selection Option: ', activities)

    st.sidebar.markdown("Github Repository: "
                        "[Click Here](https://github.com/Vamshi-Munukuntla/Concrete_Strength_Prediction)")

    # Problem Statement
    if option == 'Problem Statement':
        Problem_Statement()

    elif option == 'EDA':
        EDA()

    elif option == "Feature Engineering":
        Preprocessing()

    elif option == 'Model Building':
        model_building()

    elif option == 'Single Prediction':
        app()

    elif option == "Batch Prediction":
        batch_predict()

    # Display the PDF file

    # Add a download button for the PDF file
    with open("EDA_Files/Concrete.pdf", "rb") as f:
        pdf_bytes = f.read()
        st.sidebar.download_button("Download Presentation PDF", pdf_bytes,
                                   file_name="your_file_name.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
