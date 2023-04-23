import streamlit as st


def Problem_Statement():
    st.subheader('Problem Statement:')
    st.write(
        "Concrete is the most important material in civil engineering. The concrete compressive strength is a "
        "highly nonlinear function of age and ingredients.")

    st.write(
        "Prediction results tells the optimal way to get the maximum compressive strength for a unit block of "
        "concrete using the ingredients.")

    st.write("The objective is to predict the concrete strength using the ingredients mentioned above.")

    st.write(
        "It's a Supervised - Regression Problem.")

    st.subheader('Data Collection')
    st.write("The dataset is collected from UCI REPOSITORY - [CLICK HERE]("
             "https://archive.ics.uci.edu/ml/datasets/concrete+compressive+strength).")
    st.write("Shape of the dataset (Rows, Columns): (1030, 9)")

    st.subheader('Input Features')
    st.write("**Cement** - It is the major factor that influences the strength and durability of concrete.")

    st.write("**Furnace Slag** - It is a supplementary material that enhances the strength and durability of "
             "concrete and improves its resistance to chemical attack.")

    st.write(" **Fly Ash** - It's a byproduct of coal combustion, used to reduce the carbon footprint.")
    st.write("**Water** - It is essential to initiate the chemical reaction between cement and other components, "
             "but it's excessive and inadequate amount can adversely affect the strength and durability of "
             "concrete.")
    st.write("**Superplaticizer** - Superplaticizers are chemical additives that can significantly improve the "
             "strength and workability of concrete by reducing its water-cement ratio without compromising its "
             "fluidity.")
    st.write("**Coarse Aggregate** - Coarse aggregates in concrete provide mechanical strength, increases the "
             "durability, and reduces the cost by reducing the cement content and also enhancing its resistance "
             "to compressive and tensile forces.")
    st.write("**Fine Aggregate** - Fine aggregate in concrete fills the voids between coarse aggregate particles "
             "and helps to produce a workable mix, resulting in a smoother surface finish and improved strength.")
    st.write("**Age** - Age is an important factor in determining the strength of concrete as it affects the "
             "chemical reaction between cement and water, resulting in gradual strength gain over time.")

    st.subheader('Target Feature')
    st.write("**Compressive strength** - Compressive strength of concrete refers to its ability to resist "
             "compression or withstand force applied to it in a perpendicular direction, and is an important "
             "factor in determining the durability and load-bearing capacity of concrete structures.")
