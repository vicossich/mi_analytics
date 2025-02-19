import streamlit as st
import pandas as pd
from utils import cleanning_data

####
@st.cache_data
def load_data(file):
	# Determine the file type and process accordingly
	if file.name.endswith(".csv"):
		return pd.read_csv(file)
	elif file.name.endswith(".xlsx"):
	    return pd.read_excel(file)
	else:
	    st.error("Unsupported file type!")
	    return None
####

def show_datapreview():
	st.write("#### Data Preview")
	st.dataframe(data_uploaded,height=1000)




uploaded_data = pd.DataFrame()
# check if a df existis in cache
if 'uploaded_data' not in st.session_state:
	st.write("#### File Uploader")
	data_uploaded = st.file_uploader("Upload Move Improve CSV file", type="csv")


	# check if the data is empty
	if data_uploaded is not None:
		# Use the cached function to load data
		data_uploaded = load_data(data_uploaded)
		data_uploaded = cleanning_data(data_uploaded)

		# Armazenar no `session_state`
		st.session_state['uploaded_data'] = data_uploaded
		show_datapreview()

		
else:
	data_uploaded = st.session_state['uploaded_data']
	show_datapreview()



