import streamlit as st
import pandas as pd
 
st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("carprices.csv")
st.area_chart(df)
st.line_chart(df)
