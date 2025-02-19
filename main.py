import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd 
from utils import cleanning_data, general_skill_performance, general_component_performance
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64
from PIL import Image
from io import BytesIO


st.set_page_config(page_title="MoveImprove - Analysis v.1",
	page_icon="",
	layout="wide")

# page setup
uploadfilepage = st.Page(page="views/uploadfile.py", title="Upload File", icon=":material/upload:", default=True,)
overview = st.Page(page="views/overview.py", title="Overview", icon=":material/dataset:")
reportpage = st.Page(page="views/report.py", title="Report", icon=":material/bar_chart:")

# image = Image.open('./static/images/MI_brand_Artboard 3_reverse-2spot.png'
st.markdown(
    """
    <style>

    	/* import font */
    	@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap');
    	
    	/* Apply Figtree font globally */
	    html, body, [class*="css"] {
	        font-family: 'Figtree', sans-serif !important;
	    }

	    /* hide decoration bar */
        #stDecoration {visibility: hidden;}

    	/* sidebar bg_color */
    	[data-testid="stSidebar"] {
	        background-color: #00AED5; /* Replace with your preferred color */
	    }

	    /* Ajustar a largura da sidebar para evitar corte dos filtros*/
        [data-testid="stSidebar"] {
            width: 350px !important;  /* Ajusta a largura sem impedir colapso */
            transition: width 0.5s ease-in-out;  /* Animação para suavizar a abertura e fechamento */
        }

	    /* sidebar logo */
        [data-testid="stSidebarNav"] {
            background-image: url('https://raw.githubusercontent.com/vicossich/MI/refs/heads/main/MI_brand_Artboard%203_reverse-2spot.png');
            background-repeat: no-repeat;
            width:70%;
            background-size: contain; /* Adjust size to fit the sidebar */
            padding-top: 100px; /* Space to push content below the image */
            background-position: top center; /* Position image at the top center */
            margin:5px;
            margin-left: 15px;
        }

        /* Target the entire sidebar navigation container */
        [data-testid="stSidebarNavItems"] {
            color: #fff !important; /* Force all text within the sidebar nav to white */
        }

        /* Style the links (default state) */
        [data-testid="stSidebarNavItems"] a {
            color: #fff !important; /* Text color white */
            text-decoration: none; /* Remove underline (optional) */
            background-color: transparent; /* Ensure no background */
            padding: 5px 10px; /* Add some padding for better hover effect */
            border-radius: 5px; /* Optional: Rounded edges */
            margin-left: 10px;
        }

        /* Hover effect for links */
        [data-testid="stSidebarNavItems"] a:hover {
            color: #04B6E2 !important; /* Text color blue on hover */
            background-color: #fff !important; /* White background on hover */
        }

        /* Style all span elements inside the sidebar nav */
        [data-testid="stSidebarNavItems"] span {
            color: #fff !important; /* Ensure all spans are white */
        }

        /* Optional: Hover effect for spans */
        [data-testid="stSidebarNavItems"] a:hover span {
            color: #04B6E2 !important; /* Text color blue for spans on hover */
        }

        [data-testid="stSidebarUserContent"]{
        	padding-top: 0px;
        }

	    div.st-dr,
	    div.st-dq,
	    div.st-ds,
	    div.st-bc.st-bd.st-be.st-bf.st-dr.st-dl.st-ae.st-dm.st-di  {
	    	background-color: #fff !important; /* Blue slider handle */
	    }



        /* change main area padding */
	    div.st-emotion-cache-1jicfl2 {
	    	padding: 40px;
	    }

	    /* managing button style */
	    button.st-emotion-cache-n5r31u.ef3psqc19,
	    button.st-emotion-cache-1igbibe.ef3psqc19 {
		    background-color: #FFFFFF !important; /* Default button color */
		    color: #1E3160 !important; /* Blue text color */
		    border: none !important;
		    padding: 10px 20px !important;
		    text-align: center !important;
		    text-decoration: none !important;
		    display: inline-block !important;
		    font-size: 16px !important;
		    margin: 4px 2px !important;
		    cursor: pointer !important;
		    border-radius: 8px !important; /* Rounded corners */
		    transition: background-color 0.3s !important; /* Smooth transition */
		}

		button.st-emotion-cache-n5r31u.ef3psqc19:hover,
		button.st-emotion-cache-1igbibe.ef3psqc19:hover {
		    background-color: #1E3160 !important; /* Dark blue on hover */
		    color: #FFFFFF !important; /* White text on hover */
		    border-color: #FFFFFF !important;
		}

		button.st-emotion-cache-n5r31u.ef3psqc19:active,
		button.st-emotion-cache-1igbibe.ef3psqc19:active {
		    background-color: #1E3160 !important; /* Dark blue background when clicked */
		    color: #FFFFFF !important; /* White text when clicked */
		    border-color: #FFFFFF !important;
		}

		button.st-emotion-cache-n5r31u.ef3psqc19:active,
		button.st-emotion-cache-1igbibe.ef3psqc19:focus {
		    background-color: #1E3160 !important; /* Ensure focus uses the same color */
		    color: #FFFFFF !important; /* White text on focus */
		    border-color: #FFFFFF !important;
		    outline: none !important; /* Remove default focus outline */
		}
    </style>
    """,
    unsafe_allow_html=True,
)


# # Inject CSS into the Streamlit app
# # st.markdown(sidebar_bg_color, unsafe_allow_html=True)
# # Open image with PIL and resize it
# # image = Image.open(BytesIO(image_bytes))
# image = Image.open('./static/images/MI_brand_Artboard 3_reverse-2spot.png')
# # image = Image.open('logo.png')
# # resized_image = image.resize((200, 200))  # Adjust width and height as needed
# resized_image = image
# # Display the image in the sidebar
# st.sidebar.image(resized_image, use_container_width=False)
pg = st.navigation(pages=[uploadfilepage,overview,reportpage])


# # Inject CSS into the Streamlit app
# st.markdown(sidebar_bg_color, unsafe_allow_html=True)
# # Open image with PIL and resize it
# # image = Image.open(BytesIO(image_bytes))
# image = Image.open('./static/images/MI_brand_Artboard 3_reverse-2spot.png')
# # image = Image.open('logo.png')
# # resized_image = image.resize((200, 200))  # Adjust width and height as needed
# resized_image = image
# # Display the image in the sidebar
# st.sidebar.image(resized_image, use_container_width=False)


pg.run()


