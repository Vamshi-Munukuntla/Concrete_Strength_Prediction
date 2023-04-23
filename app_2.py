import streamlit as st

from Streamlit_app.EDA import EDA
from Streamlit_app.Problem_Statement import Problem_Statement
from Streamlit_app.output import app
from Streamlit_app.Preprocessing import Preprocessing
from Streamlit_app.Model_Building import model_building

st.set_page_config(page_title="Concrete Compressive Strength Prediction",
                   page_icon=":hammer_and_wrench:", layout="wide")
st.title("Concrete Compressive Strength Prediction")


def main():
    activities = ['Problem Statement', 'EDA', 'Feature Engineering', "Model Building", 'Prediction']
    option = st.sidebar.radio('Selection Option: ', activities)

    st.sidebar.markdown("[GitHub](https://github.com/Vamshi-Munukuntla/Concrete_Strength_Prediction)")

    # Problem Statement
    if option == 'Problem Statement':
        Problem_Statement()

    elif option == 'EDA':
        EDA()

    elif option == "Feature Engineering":
        Preprocessing()

    elif option == 'Model Building':
        model_building()

    elif option == 'Prediction':
        app()


if __name__ == "__main__":
    main()
