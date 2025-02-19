import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd 
from utils import general_skill_performance, general_component_performance
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64
from PIL import Image
from io import BytesIO


# st.set_page_config(page_title="MoveImprove - Analysis v.1",
# 	page_icon="",
# 	layout="wide")

# # Base64 image data (truncated here for readability)
# img_data = "data:image/png;base64,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"

# # Decode the base64 image
# image_bytes = base64.b64decode(img_data.split(",")[1])

# # Custom CSS to change the sidebar background color
# sidebar_bg_color = """
# <style>
#     [data-testid="stSidebar"] {
#         background-color: #00AED5; /* Replace with your preferred color */
#     }
# </style>
# """

# # # Inject CSS into the Streamlit app
# st.markdown(sidebar_bg_color, unsafe_allow_html=True)
# # Open image with PIL and resize it
# # image = Image.open(BytesIO(image_bytes))
# image = Image.open('./static/images/MI_brand_Artboard 3_reverse-2spot.png')
# # image = Image.open('logo.png')
# # resized_image = image.resize((200, 200))  # Adjust width and height as needed
# resized_image = image
# # Display the image in the sidebar
# st.sidebar.image(resized_image, use_container_width=False)


try:
	data = st.session_state['uploaded_data']

	# ################################	
	# st.sidebar.header("Filters")

	# # Initialize session state for filters
	# if "skill" not in st.session_state:
	# 	st.session_state.skill = "All"
	# if "performer" not in st.session_state:
	# 	st.session_state.performer = "All"
	# if "asmt_type" not in st.session_state:
	# 	st.session_state.asmt_type = "All"
	# if "evaluator" not in st.session_state:
	# 	st.session_state.evaluator = "All"

	# # Reset Filters Button
	# if st.sidebar.button("Reset Filters"):
	# 	st.session_state.skill = "All"
	# 	st.session_state.performer = "All"
	# 	st.session_state.asmt_type = "All"
	# 	st.session_state.evaluator = "All"

	# skill = st.sidebar.selectbox(
	# 	"Select Skill", 
	# 	["All"] + list(data['SkillName'].unique()), 
	# 	key="skill"
	# )


	# performer = st.sidebar.selectbox(
	# 	"Select Performer", 
	# 	["All"] + list(data['PerformerName'].unique()), 
	# 	key="performer"
	# )

	# asmt_type = st.sidebar.selectbox(
	# 	"Select Assessment Type", 
	# 	["All"] + list(data['Asmt Mode'].unique()), 
	# 	key="asmt_type"
	# )

	# # Dynamically update evaluator options based on asmt_type
	# if asmt_type == 'peer':
	# 	evaluator = st.sidebar.selectbox(
	# 		"Select Evaluator", 
	# 		["All"] + list(data['EvaluatorName'].unique()), 
	# 		key="evaluator"
	# 	)
	# else:
	# 	evaluator = "All"

	# # Filter data based on selections
	# filtered_data = data[
	# 	((data['PerformerName'] == performer) | (performer == "All")) &
	# 	((data['SkillName'] == skill) | (skill == "All")) &
	# 	((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
	# 	((data['EvaluatorName'] == evaluator) | (evaluator == "All"))
	# ]
	# ################################

	################################	
	st.sidebar.header("Filters")

	# Inicializa os filtros no session state
	if "skill" not in st.session_state:
	    st.session_state.skill = "All"
	if "performer" not in st.session_state:
	    st.session_state.performer = "All"
	if "asmt_type" not in st.session_state:
	    st.session_state.asmt_type = "All"
	if "evaluator" not in st.session_state:
	    st.session_state.evaluator = "All"
	if "start_date" not in st.session_state:
	    st.session_state.start_date = data["Start Time"].min().date()
	if "end_date" not in st.session_state:
	    st.session_state.end_date = data["Start Time"].max().date()

	# Botão para resetar os filtros
	if st.sidebar.button("Reset Filters"):
	    st.session_state.skill = "All"
	    st.session_state.performer = "All"
	    st.session_state.asmt_type = "All"
	    st.session_state.evaluator = "All"
	    st.session_state.start_date = data["Start Time"].min().date()
	    st.session_state.end_date = data["Start Time"].max().date()

	# 🔹 Seleção de Filtros
	skill = st.sidebar.selectbox("Select Skill", ["All"] + list(data['SkillName'].unique()), key="skill")
	performer = st.sidebar.selectbox("Select Performer", ["All"] + list(data['PerformerName'].unique()), key="performer")
	asmt_type = st.sidebar.selectbox("Select Assessment Type", ["All"] + list(data['Asmt Mode'].unique()), key="asmt_type")

	# 🔹 Select Evaluator (caso o tipo de avaliação seja 'peer')
	if asmt_type == 'peer':
	    evaluator = st.sidebar.selectbox("Select Evaluator", ["All"] + list(data['EvaluatorName'].unique()), key="evaluator")
	else:
	    evaluator = "All"

	start_date = st.sidebar.date_input(
	    "Start Date",
	    value=st.session_state.start_date,
	    min_value=data["Start Time"].min().date(),
	    max_value=data["Start Time"].max().date()
	)

	end_date = st.sidebar.date_input(
	    "End Date",
	    value=st.session_state.end_date,
	    min_value=data["Start Time"].min().date(),
	    max_value=data["Start Time"].max().date()
	)

	# Garantir que a data final não seja menor que a inicial
	if start_date > end_date:
	    st.sidebar.error("⚠️ End Date must be after Start Date!")
	else:
	    st.session_state.start_date = start_date
	    st.session_state.end_date = end_date

	# Filtragem dos dados
	filtered_data = data[
	    ((data['PerformerName'] == performer) | (performer == "All")) &
	    ((data['SkillName'] == skill) | (skill == "All")) &
	    ((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
	    ((data['EvaluatorName'] == evaluator) | (evaluator == "All")) &
	    ((data["Start Time"].dt.date >= st.session_state.start_date) & (data["Start Time"].dt.date <= st.session_state.end_date))
	]
	################################

	st.write("### Overview")
	try:
		if filtered_data.empty:
			st.warning("No data matches the selected filters. Please adjust your filters and try again.")
		else:
			# Display the dataframe in Streamlit
			st.write("### Data Preview")

			# Custom gray message box using Markdown
			st.markdown(
				"""
				<div style="
					padding: 10px;
					background-color: #f7f7f7;
					border-radius: 5px;
					color: #333;margin-bottom:20px">
					<ul style="margin-bottom:0px">
						<li>The dataset changes according to the filters applied on the left-hand side.</li>
						<li>You can also download the filtered table data.</li>
					</ul>
				</div>
				""",
				unsafe_allow_html=True
			)

			st.dataframe(filtered_data)

			st.markdown("<hr>", unsafe_allow_html=True)
			###################
			import io

			# Criar checkboxes abaixo do DataFrame com texto menor
			st.markdown('<p style="font-size:20px; font-weight:bold;">Select Columns to Include in CSV</p>', unsafe_allow_html=True)


			# # Custom gray message box using Markdown
			# st.markdown(
			# 	"""
			# 	<div style="
			# 		padding: 10px;
			# 		background-color: #f7f7f7;
			# 		border-radius: 5px;
			# 		color: #333;margin-bottom:20px">
			# 		<ul style="margin-bottom:0px;font-size:5px;">
			# 			<li>You can download the dataset while keeping the applied filters. Additionally, you can select which columns (variables) you want to include in the final file.</li>
			# 		</ul>
			# 	</div>
			# 	""",
			# 	unsafe_allow_html=True
			# )

			st.warning("You can download the dataset while keeping the applied filters. Additionally, you can select which columns (variables) you want to include in the final file.")
			
			# Criar 5 colunas para distribuir os checkboxes
			columns = st.columns(5)  

			# Dicionário para armazenar seleção das colunas
			selected_columns = {}

			# Criar checkboxes organizados em 5 colunas
			cols_list = list(filtered_data.columns)

			###########################
			# to adjust the checkbox style
			st.markdown(
			    """
			    <style>
			        /* Reduce font size inside checkboxes */
			        div[data-testid="stHorizontalBlock"] label span {
			            font-size: 8px !important;  /* Reduce font size */
			            line-height: 1 !important; /* Adjust spacing */
			        }

			        /* Alternative: Shrink entire checkbox element */
			        div[data-testid="stCheckbox"] {
			            transform: scale(0.8); /* Scale down checkbox */
			            transform-origin: left; /* Keep alignment */
			        }
			    </style>
			    """,
			    unsafe_allow_html=True
			)

			# Criar checkboxes organizados em 5 colunas
			for i, col in enumerate(cols_list):
			    with columns[i % 5]:  # Distribui os checkboxes nas 5 colunas
			        selected_columns[col] = st.checkbox(col, value=True)
			###########################

			# Filtrar colunas selecionadas
			columns_to_include = [col for col, selected in selected_columns.items() if selected]

			# Exibir um aviso se nenhuma coluna for selecionada
			if not columns_to_include:
			    st.warning("⚠️ Select at least one column to download.")

			# 📌 **Garantir que o formato das datas seja mantido**
			def format_datetime_column(df, column_name):
			    if column_name in df.columns:
			        df[column_name] = pd.to_datetime(df[column_name], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

			# Aplicar a formatação apenas se as colunas estiverem no dataset
			if "Start Time" in columns_to_include:
			    format_datetime_column(filtered_data, "Start Time")

			if "End Time" in columns_to_include:
			    format_datetime_column(filtered_data, "End Time")

			# Criar um arquivo CSV com as colunas selecionadas
			output = io.StringIO()
			filtered_data[columns_to_include].to_csv(output, index=False)
			data_bytes = output.getvalue().encode("utf-8")

			# Botão de download abaixo das checkboxes
			st.download_button(
			    label="Download Filtered data",
			    data=data_bytes,
			    file_name="filtered_data.csv",
			    mime="text/csv",
			    disabled=not columns_to_include  # Desativa o botão se nenhuma coluna for selecionada
			)

			st.markdown("<hr>", unsafe_allow_html=True)
			###################

			# Add a horizontal line
			# st.markdown("<hr>", unsafe_allow_html=True)

			# Filter widgets
			st.write("### Quick Look")
			
			columns = list(filtered_data.columns)  # Get column names for filtering

			# Select a column to filter
			# filter_column = st.selectbox("Select column to filter", options=columns)


			col1,col2,col3,col4,col5 = st.columns(5)
			
			with col1:
				st.write("#### Activity")
				####
				# assuming that all the rows have the same value
				st.write(f"{filtered_data['ActivityName'].values[0]}")

			with col2:
				st.write("#### Skills")

				skills=sorted(filtered_data['SkillName'].unique())

				html_list = """
				<ul style="list-style-type: square; margin-left: 0px; font-size: 16px;">
					{}
				</ul>
				""".format("".join(f"<li>{skill}</li>" for skill in skills))

				st.markdown(html_list, unsafe_allow_html=True)

				# for skill in skills:
				# 	st.write(skill)

			with col3:
				st.write("#### Performers")

				performers=sorted(filtered_data['PerformerName'].unique())

				# total_performers 
				st.write(f"##### Total: {len(performers)}")

				html_list = """
				<ul style="list-style-type: square; margin-left: 0px; font-size: 16px;">
					{}
				</ul>
				""".format("".join(f"<li>{performer}</li>" for performer in performers))

				st.markdown(html_list, unsafe_allow_html=True)

				# for performer in performers:
				# 	st.write(performer)

			with col4:
				st.write("#### Evaluators")

				evaluators=sorted(filtered_data['EvaluatorName'].unique())

				# total_performers 
				st.write(f"##### Total: {len(evaluators)}")

				html_list = """
				<ul style="list-style-type: square; margin-left: 0px; font-size: 16px;">
					{}
				</ul>
				""".format("".join(f"<li>{evaluator}</li>" for evaluator in evaluators))

				st.markdown(html_list, unsafe_allow_html=True)

			with col5:
				st.write("#### Assessment Mode")

				# Calculate the frequency of each assessment mode
				asmt_mode = filtered_data['Asmt Mode'].value_counts()

				# Generate an unordered HTML list dynamically for asmt_mode
				html_list = """
				<ul style="list-style-type: square; margin-left: 0px; font-size: 16px;">
					{}
				</ul>
				""".format("".join(f"<li><strong>{mode}</strong>: {count}</li>" for mode, count in asmt_mode.items()))

				# Display the unordered list
				st.markdown(html_list, unsafe_allow_html=True)

			# Add a horizontal line
			st.markdown("<hr>", unsafe_allow_html=True)

			st.write("### Skills Overview")
			
			col1,col2,col3 = st.columns(3)
			
			with col1:
				st.write("#### Duration")

				##### --- General by Skills
				# duration 
				general_skill_duration_self = general_skill_performance(df=filtered_data,
																		vd='Duration(seconds)',
																		option='SkillName')


				# st.dataframe(general_skill_duration_self)
				# st.table(general_skill_duration_self)
				# Convert the DataFrame to an HTML table
				html_table = general_skill_duration_self.to_html(
					index=False,
					border=0,
					justify="center",
					classes="styled-table"
				)

				# Add optional CSS for styling
				st.markdown(
					"""
					<style>
					.styled-table {
						border-collapse: collapse;
						margin: 0px 0;
						font-size: 0.5em;
						font-family: sans-serif;
						min-width: 350px;
						border-radius: 5px 5px 0 0;
						overflow: hidden;
						box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
					}
					.styled-table thead tr {
						background-color: #04B6E2;
						color: #ffffff;
						text-align: left;
					}
					.styled-table th, .styled-table td {
						padding: 10px 10px;
						font-size: 13px;
					}
					.styled-table tbody tr {
						border-bottom: 1px solid #dddddd;
					}
					.styled-table tbody tr:nth-of-type(even) {
						background-color: #f3f3f3;
					}
					.styled-table tbody tr:last-of-type {
						border-bottom: 2px solid #04B6E2;
					}
					</style>
					""",
					unsafe_allow_html=True
				)

				# Render the table
				st.markdown(html_table, unsafe_allow_html=True)

				footer = "<p style='color:#ccc; font-size: 15px'>in seconds</p>"
				st.markdown(footer, unsafe_allow_html=True)


			with col2:
				st.write("#### Score")

				##### --- General by Skills
				# score 
				general_skill_score_self = general_skill_performance(df=filtered_data,
																	vd='Score',
																	option='SkillName')


				# st.dataframe(general_skill_duration_self)
				# st.table(general_skill_duration_self)
				# Convert the DataFrame to an HTML table
				html_table = general_skill_score_self.to_html(
					index=False,
					border=0,
					justify="center",
					classes="styled-table"
				)

				# Add optional CSS for styling
				st.markdown(
					"""
					<style>
					.styled-table {
						border-collapse: collapse;
						margin: 0px 0;
						font-size: 0.5em;
						font-family: sans-serif;
						min-width: 350px;
						border-radius: 5px 5px 0 0;
						overflow: hidden;
						box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
					}
					.styled-table thead tr {
						background-color: #04B6E2;
						color: #ffffff;
						text-align: left;
					}
					.styled-table th, .styled-table td {
						padding: 10px 10px;
						font-size: 13px;
					}
					.styled-table tbody tr {
						border-bottom: 1px solid #dddddd;
					}
					.styled-table tbody tr:nth-of-type(even) {
						background-color: #f3f3f3;
					}
					.styled-table tbody tr:last-of-type {
						border-bottom: 2px solid #04B6E2;
					}
					</style>
					""",
					unsafe_allow_html=True
				)

				# Render the table
				st.markdown(html_table, unsafe_allow_html=True)
				footer = "<p style='color:#ccc; font-size: 15px'>points</p>"
				st.markdown(footer, unsafe_allow_html=True)


			with col3:
				st.write("#### Attempts")

				##### --- General by Skills
				# score 
				general_skill_score_self = general_skill_performance(df=filtered_data,
																	vd='Attempt(s)',
																	option='SkillName')


				# st.dataframe(general_skill_duration_self)
				# st.table(general_skill_duration_self)
				# Convert the DataFrame to an HTML table
				html_table = general_skill_score_self.to_html(
					index=False,
					border=0,
					justify="center",
					classes="styled-table"
				)

				# Add optional CSS for styling
				st.markdown(
					"""
					<style>
					.styled-table {
						border-collapse: collapse;
						margin: 0px 0;
						font-size: 0.5em;
						font-family: sans-serif;
						min-width: 400px;
						border-radius: 5px 5px 0 0;
						overflow: hidden;
						box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
					}
					.styled-table thead tr {
						background-color: #04B6E2;
						color: #ffffff;
						text-align: left;
					}
					.styled-table th, .styled-table td {
						padding: 10px 10px;
						font-size: 13px;
					}
					.styled-table tbody tr {
						border-bottom: 1px solid #dddddd;
					}
					.styled-table tbody tr:nth-of-type(even) {
						background-color: #f3f3f3;
					}
					.styled-table tbody tr:last-of-type {
						border-bottom: 2px solid #04B6E2;
					}
					</style>
					""",
					unsafe_allow_html=True
				)

				# Render the table
				st.markdown(html_table, unsafe_allow_html=True)
				footer = "<p style='color:#ccc; font-size: 15px'>count</p>"
				st.markdown(footer, unsafe_allow_html=True)


			# Add a horizontal line
			st.markdown("<hr>", unsafe_allow_html=True)

			st.write("### Components Overview")

			##### --- General by Components
			# duration 
			skillNamesList, output_component_duration = general_component_performance(df=filtered_data, 
																					vd='Duration(seconds)')

			# score 
			skillNamesList, output_component_score = general_component_performance(df=filtered_data,
																				vd='Score')

			# attempts
			skillNamesList, output_component_attemt = general_component_performance(df=filtered_data,
																				vd='Attempt(s)')



			attemps_list = {'skill':[],'value':[]}	
			
			for skill in skills:
				attemps_list['skill'].append(skill)
				attemps_list['value'].append(round(output_component_attemt[skill]['count'].values[0]))

			
			# Create the bar chart
			fig = go.Figure(
				data=[go.Bar(x=attemps_list['skill'],
							y=attemps_list['value'],
							text=attemps_list['value'],  # Add text on bars
							textposition='outside',  # Always display numbers on top of bars
							textfont=dict(size=18, color="#000"),
							marker=dict(
						color='#04B6E2',  # Custom bar colors
					))]
			)

			# Define o limite superior do eixo Y (2 unidades acima do valor máximo)
			y_max = max(fig.data[0].y) + 2

			# Customize the layout
			fig.update_layout(
				title="Attempts General",
				xaxis_title="",
				yaxis_title="Count",
				template="plotly_white",
				height=600,
				plot_bgcolor="rgba(0,0,0,0)",  # Make plot background transparent
				# paper_bgcolor="rgba(0,0,0,0)",  # Make outside background transparent
				xaxis=dict(showgrid=False),  # Remove x-axis grid lines
				yaxis=dict(showgrid=False, range=[0, y_max]),  # Remove y-axis grid lines
			)

			# Show the figure
			# Add the Plotly chart to Streamlit
			st.plotly_chart(fig)


			for skill in skills:
				st.write(f"### {skill}")


				col1, col2, col3 = st.columns(3)

				with col1:
					st.write("#### Duration")
					##### --- General by Components
					html_table = output_component_duration[skill][output_component_duration[skill].columns[1:]].to_html(
						index=False,
						border=0,
						justify="center",
						classes="styled-table"
					)

					# Add optional CSS for styling
					st.markdown(
						"""
						<style>
						.styled-table {
							border-collapse: collapse;
							margin: 0px 0;
							font-size: 0.9em;
							font-family: sans-serif;
							min-width: 400px;
							border-radius: 5px 5px 0 0;
							overflow: hidden;
							box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
						}
						.styled-table thead tr {
							background-color: #04B6E2;
							color: #ffffff;
							text-align: left;
						}
						.styled-table th, .styled-table td {
							padding: 10px 10px;
						}
						.styled-table tbody tr {
							border-bottom: 1px solid #dddddd;
						}
						.styled-table tbody tr:nth-of-type(even) {
							background-color: #f3f3f3;
						}
						.styled-table tbody tr:last-of-type {
							border-bottom: 2px solid #04B6E2;
						}
						</style>
						""",
						unsafe_allow_html=True
					)

					# Render the table
					st.markdown(html_table, unsafe_allow_html=True)
			
				with col2:
					st.write("#### Score")
					##### --- General by Components
					html_table = output_component_score[skill][output_component_score[skill].columns[1:]].to_html(
						index=False,
						border=0,
						justify="center",
						classes="styled-table"
					)

					# Add optional CSS for styling
					st.markdown(
						"""
						<style>
						.styled-table {
							border-collapse: collapse;
							margin: 0px 0;
							font-size: 0.9em;
							font-family: sans-serif;
							min-width: 400px;
							border-radius: 5px 5px 0 0;
							overflow: hidden;
							box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
						}
						.styled-table thead tr {
							background-color: #04B6E2;
							color: #ffffff;
							text-align: left;
						}
						.styled-table th, .styled-table td {
							padding: 10px 10px;
						}
						.styled-table tbody tr {
							border-bottom: 1px solid #dddddd;
						}
						.styled-table tbody tr:nth-of-type(even) {
							background-color: #f3f3f3;
						}
						.styled-table tbody tr:last-of-type {
							border-bottom: 2px solid #04B6E2;
						}
						</style>
						""",
						unsafe_allow_html=True
					)

					# Render the table
					st.markdown(html_table, unsafe_allow_html=True)

				with col3:
					st.write("#### Attempts")
					##### --- General by Components
					html_table = output_component_attemt[skill][output_component_attemt[skill].columns[1:]].to_html(
						index=False,
						border=0,
						justify="center",
						classes="styled-table"
					)

					# Add optional CSS for styling
					st.markdown(
						"""
						<style>
						.styled-table {
							border-collapse: collapse;
							margin: 0px 0;
							font-size: 0.9em;
							font-family: sans-serif;
							min-width: 400px;
							border-radius: 5px 5px 0 0;
							overflow: hidden;
							box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
						}
						.styled-table thead tr {
							background-color: #04B6E2;
							color: #ffffff;
							text-align: left;
						}
						.styled-table th, .styled-table td {
							padding: 10px 10px;
						}
						.styled-table tbody tr {
							border-bottom: 1px solid #dddddd;
						}
						.styled-table tbody tr:nth-of-type(even) {
							background-color: #f3f3f3;
						}
						.styled-table tbody tr:last-of-type {
							border-bottom: 2px solid #04B6E2;
						}
						</style>
						""",
						unsafe_allow_html=True
					)

					# Render the table
					st.markdown(html_table, unsafe_allow_html=True)

				df = filtered_data[(filtered_data['SkillName']==skill)].copy()

				# Pivot the data to create a matrix for the heatmap
				heatmap_data = df.pivot_table(
					index="Component Name", columns="PerformerName", values="Score"
				).round(1)

				# Create the heatmap with a custom color scale and show values
				fig = px.imshow(
					heatmap_data,
					labels={"x": "Performer", "y": "Component", "color": "Score"},
					title="Scores by Components and Performers",
					color_continuous_scale=[
						(0, "#ccc"),
						(0.3, "#EF3E5E"), # red
						(0.5, "#F7E244"), # yellow 
						(1., "#ACD14B")  # green
					],
					zmin=0,  # Min score
					zmax=3,  # Max score
					text_auto=True  # Automatically display the values
				)

				fig.update_layout(
					xaxis=dict(
						tickangle=90  # Rotate x-axis labels by 90 degrees
					),
					autosize=True,
					width=1000,     # Set a custom width
					height=1000,     # Set a custom height
				)

				# Remove the color scale
				fig.update_coloraxes(showscale=True)
				
				# Show the heatmap
				st.plotly_chart(fig,use_container_width=True,key=f"heat-{skill}")


				#####################################################
				# Create the pivot table
				jitter_data = df.pivot_table(
					index="Component Name", 
					columns="PerformerName", 
					values="Attempt(s)", 
					aggfunc="count"
				)

				# Reset index for plotting
				plot_data = jitter_data.reset_index().melt(id_vars="Component Name", var_name="PerformerName", value_name="Count")

				# Add jitter to the Count values
				np.random.seed(42)  # Set seed for reproducibility
				plot_data["Jittered Count"] = plot_data["Count"] + (np.random.rand(len(plot_data)) - 0.5) * 0.3  # Add small random noise

				# Generate the scatter plot with jitter
				fig = px.scatter(
					plot_data,
					x="Jittered Count",  # Use jittered values for x-axis
					y="Component Name",
					color="PerformerName",
					title="Attempts by Component and Performer",
					labels={"Component Name": "Components", "Jittered Count": "Number of Attempts"}
				)

				# Customize layout
				fig.update_traces(marker=dict(size=15, opacity=0.7))  # Adjust marker size and opacity

				# Set x-axis to display 0-10 with all integer ticks
				fig.update_layout(
					xaxis=dict(
						tickangle=0,  # Rotate x-axis labels
						range=[0, 10],  # Set x-axis range from 0 to 10
						tickmode="array",  # Use explicit tick values
						tickvals=list(range(0, 11)),  # Set tick values to integers [0, 1, 2, ..., 10]
						title="Attempts"
					),
					yaxis=dict(
						autorange="reversed",  # Invert the y-axis
						tickfont=dict(size=12)  # Reduce y-label font size
					),
					template="plotly_white",
					height=600,
					width=800,
					plot_bgcolor="rgba(0,0,0,0)"  # Make plot background transparent
				)
				
				# Show the jitter
				st.plotly_chart(fig,use_container_width=True,key=f"jitter-{skill}")


				#####################################################
				# Create the pivot table
				jitter_data = df.pivot_table(
					index="Component Name", 
					columns="PerformerName", 
					values="Duration(seconds)", 
					aggfunc="mean"
				)

				# Reset index for plotting
				plot_data = jitter_data.reset_index().melt(id_vars="Component Name", var_name="PerformerName", value_name="Count")

				# Add jitter to the Count values
				np.random.seed(42)  # Set seed for reproducibility
				plot_data["Jittered Count"] = plot_data["Count"] + (np.random.rand(len(plot_data)) - 0.5) * 0.3  # Add small random noise

				# Generate the scatter plot with jitter
				fig = px.scatter(
					plot_data,
					x="Jittered Count",  # Use jittered values for x-axis
					y="Component Name",
					color="PerformerName",
					title="Duration by Component and Performer",
					labels={"Component Name": "Components", "Jittered Count": "Duration"}
				)

				# Customize layout
				fig.update_traces(marker=dict(size=15, opacity=0.7))  # Adjust marker size and opacity

				# Set x-axis to display 0-10 with all integer ticks
				fig.update_layout(
					xaxis=dict(
						tickangle=0,  # Rotate x-axis labels
						# range=[0, 10],  # Set x-axis range from 0 to 10
						tickmode="array",  # Use explicit tick values
						# tickvals=list(range(0, 11)),  # Set tick values to integers [0, 1, 2, ..., 10]
						title="Duration"
					),
					yaxis=dict(
						autorange="reversed",  # Invert the y-axis
						tickfont=dict(size=12)  # Reduce y-label font size
					),
					template="plotly_white",
					height=600,
					width=800,
					plot_bgcolor="rgba(0,0,0,0)"  # Make plot background transparent
				)
				
				# Show the jitter
				st.plotly_chart(fig,use_container_width=True,key=f"time-{skill}")


				###################################################################			    
	except:
		pass
except:
	st.warning('No data loaded', icon="⚠️")


# it's expected that all the columns have the same name
# - ActivityName
# - SkillName
# - PerformerName
# - PerformerID
# - EvaluatorName
# - EvaluatorID
# - InstructorID
# - Team Name-ID
# - Component Name
# - Attempt(s)
# - Score
# - Start Time
# - End Time
# - Duration(seconds)
# - Asmt Mode
# - FairJob?
# - GoodAt?
# - Like?


# try:
#     data = st.session_state.get('uploaded_data')

#     if data is None:
#         st.warning('No data loaded', icon="⚠️")
#     else:
#         try:
#             ################################
#             st.sidebar.header("Filters")

#             # Initialize session state for filters
#             if "skill" not in st.session_state:
#                 st.session_state.skill = "All"
#             if "performer" not in st.session_state:
#                 st.session_state.performer = "All"
#             if "asmt_type" not in st.session_state:
#                 st.session_state.asmt_type = "All"
#             if "evaluator" not in st.session_state:
#                 st.session_state.evaluator = "All"

#             # Reset Filters Button
#             if st.sidebar.button("Reset Filters"):
#                 st.session_state.skill = "All"
#                 st.session_state.performer = "All"
#                 st.session_state.asmt_type = "All"
#                 st.session_state.evaluator = "All"

#             # Check if required columns exist in the DataFrame before filtering
#             required_columns = ["SkillName", "PerformerName", "Asmt Mode", "EvaluatorName"]
#             missing_columns = [col for col in required_columns if col not in data.columns]

#             if missing_columns:
#                 raise KeyError(f"Missing required columns in the dataset: {missing_columns}")

#             # Apply filters
#             skill = st.sidebar.selectbox("Select Skill", ["All"] + list(data['SkillName'].unique()), key="skill")
#             performer = st.sidebar.selectbox("Select Performer", ["All"] + list(data['PerformerName'].unique()), key="performer")
#             asmt_type = st.sidebar.selectbox("Select Assessment Type", ["All"] + list(data['Asmt Mode'].unique()), key="asmt_type")

#             if asmt_type == 'peer':
#                 evaluator = st.sidebar.selectbox("Select Evaluator", ["All"] + list(data['EvaluatorName'].unique()), key="evaluator")
#             else:
#                 evaluator = "All"

#             # Filter data
#             filtered_data = data[
#                 ((data['PerformerName'] == performer) | (performer == "All")) &
#                 ((data['SkillName'] == skill) | (skill == "All")) &
#                 ((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
#                 ((data['EvaluatorName'] == evaluator) | (evaluator == "All"))
#             ]

#             # Display overview
#             st.write("### Overview")

#             if filtered_data.empty:
#                 st.warning("No data matches the selected filters. Please adjust your filters and try again.")
#             else:
#                 st.write("### Data Preview")
#                 st.dataframe(filtered_data)

#         except KeyError as e:
#             st.error(f"Column Error: {str(e)}")
#             st.text("Check if the dataset has all required columns.")
#         except Exception as e:
#             st.error(f"An unexpected error occurred: {str(e)}")
#             st.text(traceback.format_exc())  # Display detailed error message

# except Exception as e:
#     st.error(f"Critical Error: {str(e)}")
#     st.text(traceback.format_exc())


