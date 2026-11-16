import streamlit as st
import pandas as pd
 
st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("carprices.csv")
st.area_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, stack=None, width="stretch", height="content", use_container_width=None, alt=None)
