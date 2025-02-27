import streamlit as st
import plotly.express as px
import pandas as pd

def graph_duration_score(df_graph_duration_score, performer):
    ##########################################
    # Ensure Start Time is converted to datetime
    df_graph_duration_score["Start Time"] = pd.to_datetime(df_graph_duration_score["Start Time"])

    # Extract the date part for unique X-axis values
    df_graph_duration_score["Date"] = df_graph_duration_score["Start Time"].dt.date

    # Ensure Score column is numeric
    df_graph_duration_score["Score"] = pd.to_numeric(df_graph_duration_score["Score"], errors="coerce").fillna(0)

    # Calculate padding for the X-axis range
    x_min = df_graph_duration_score["Start Time"].min()
    x_max = df_graph_duration_score["Start Time"].max()
    padding = pd.Timedelta(days=1.5)  # Add padding for X-axis

    # Enforce color scale normalization for 0–3 range
    df_graph_duration_score["Normalized Score"] = df_graph_duration_score["Score"].clip(lower=0, upper=3)

    # Timeline for attempt times
    fig = px.scatter(
        df_graph_duration_score,
        x="Start Time",
        y="Component Name",
        color="Score",  # Use normalized column for fixed range
        size="Duration(seconds)",
        title=f"Attempt | Duration | Score - {performer}",
        labels={"Start Time": "Attempt Time", "Component Name": "Component"},
        color_continuous_scale=[
            (0, "#ccc"),         # Grey for low scores
            (0.3, "#EF3E5E"),    # Red
            (0.5, "#F7E244"),    # Yellow
            (1.0, "#ACD14B")     # Green
        ],
        range_color=[0, 3],  # Force the color range to be 0–3
        hover_data=["Duration(seconds)"]
    )

    # Update layout for gridlines, padding, and background
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",  # Invert the Y-axis
            title="Component",
            showgrid=True,  # Add gridlines
            gridcolor="lightgray",  # Light gray grid
            gridwidth=1
        ),
        xaxis=dict(
            range=[x_min - padding, x_max + padding],  # Add padding to X-axis range
            tickmode="array",  # Show only specific ticks
            tickvals=df_graph_duration_score["Date"].unique(),  # Unique dates on the X-axis
            tickformat="%Y-%m-%d",  # Format as YYYY-MM-DD
            automargin=True,  # Automatically adjust margins for better appearance
            tickangle=0,

        ),
        title=dict(
            x=0.5  # Center the title
        ),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot background
        height=600,
        width=800,
        autosize=True
    )

    # Adjust marker transparency
    fig.update_traces(marker=dict(opacity=0.7))

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True, key=f"time-score-{performer}")
    ##########################################



# Streamlit Interface
st.write("#### Report")

try:
	data = st.session_state['uploaded_data']
	# ################################	
	# st.sidebar.header("Filters")

	# # Initialize session state for filters
	# if "skill" not in st.session_state:
	#     st.session_state.skill = "All"
	# if "performer" not in st.session_state:
	#     st.session_state.performer = "All"
	# if "asmt_type" not in st.session_state:
	#     st.session_state.asmt_type = "All"
	# if "evaluator" not in st.session_state:
	#     st.session_state.evaluator = "All"

	# # Reset Filters Button
	# if st.sidebar.button("Reset Filters"):
	#     st.session_state.skill = "All"
	#     st.session_state.performer = "All"
	#     st.session_state.asmt_type = "All"
	#     st.session_state.evaluator = "All"


	# if len(list(data['ActivityName'].unique())) > 1:
	# 	activity = st.sidebar.selectbox(
	# 	    "Select Activity", 
	# 	    ["All"] + list(data['ActivityName'].unique()), 
	# 	    key="activity"
	# 	)
	# else:
	# 	activity = list(data['ActivityName'].unique())[0]

	# skill = st.sidebar.selectbox(
	#     "Select Skill", 
	#     ["All"] + list(data['SkillName'].unique()), 
	#     key="skill"
	# )

	# performer = st.sidebar.selectbox(
	#     "Select Performer", 
	#     ["All"] + list(data['PerformerName'].unique()), 
	#     key="performer"
	# )

	# # Sidebar numeric inputs for range selection
	# min_score = st.sidebar.number_input(
	#     "Minimum Score",
	#     min_value=0,  # Minimum value allowed
	#     max_value=3,  # Maximum value allowed
	#     value=0,      # Default value
	#     step=1,       # Increment step
	#     key="min_score"
	# )

	# max_score = st.sidebar.number_input(
	#     "Maximum Score",
	#     min_value=min_score,  # Ensure it's not less than the minimum
	#     max_value=3,          # Maximum value allowed
	#     value=3,              # Default value
	#     step=1,               # Increment step
	#     key="max_score"
	# )

	# asmt_type = st.sidebar.selectbox(
	#     "Select Assessment Type", 
	#     ["All"] + list(data['Asmt Mode'].unique()), 
	#     key="asmt_type"
	# )


	# # Dynamically update evaluator options based on asmt_type
	# if asmt_type == 'peer':
	#     evaluator = st.sidebar.selectbox(
	#         "Select Evaluator", 
	#         ["All"] + list(data['EvaluatorName'].unique()), 
	#         key="evaluator"
	#     )
	# else:
	#     evaluator = "All"

	# # Filter data based on selections
	# filtered_data = data[
	#     ((data['PerformerName'] == performer) | (performer == "All")) &
	#     ((data['SkillName'] == skill) | (skill == "All")) &
	#     ((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
	#     ((data['EvaluatorName'] == evaluator) | (evaluator == "All"))
	# ]
	# ################################

	# ################################	
	# st.sidebar.header("Filters")

	# # Initialize session state for filters
	# if "skill" not in st.session_state:
	#     st.session_state.skill = "All"
	# if "performer" not in st.session_state:
	#     st.session_state.performer = "All"
	# if "asmt_type" not in st.session_state:
	#     st.session_state.asmt_type = "All"
	# if "evaluator" not in st.session_state:
	#     st.session_state.evaluator = "All"
	# if "start_date" not in st.session_state:
	#     st.session_state.start_date = data["Start Time"].min().date()
	# if "end_date" not in st.session_state:
	#     st.session_state.end_date = data["Start Time"].max().date()

	# # Reset Filters Button
	# if st.sidebar.button("Reset Filters"):
	#     st.session_state.skill = "All"
	#     st.session_state.performer = "All"
	#     st.session_state.asmt_type = "All"
	#     st.session_state.evaluator = "All"
	#     st.session_state.start_date = data["Start Time"].min().date()
	#     st.session_state.end_date = data["Start Time"].max().date()

	# # Select Activity (if multiple activities exist)
	# if len(list(data['ActivityName'].unique())) > 1:
	#     activity = st.sidebar.selectbox(
	#         "Select Activity", 
	#         ["All"] + list(data['ActivityName'].unique()), 
	#         key="activity"
	#     )
	# else:
	#     activity = list(data['ActivityName'].unique())[0]

	# # Select Skill
	# skill = st.sidebar.selectbox("Select Skill", ["All"] + list(data['SkillName'].unique()), key="skill")

	# # Select Performer
	# performer = st.sidebar.selectbox("Select Performer", ["All"] + list(data['PerformerName'].unique()), key="performer")

	# # Sidebar numeric inputs for range selection
	# min_score = st.sidebar.number_input(
	#     "Minimum Score",
	#     min_value=0,  # Minimum value allowed
	#     max_value=3,  # Maximum value allowed
	#     value=0,      # Default value
	#     step=1,       
	#     key="min_score"
	# )

	# max_score = st.sidebar.number_input(
	#     "Maximum Score",
	#     min_value=min_score,  
	#     max_value=3,          
	#     value=3,              
	#     step=1,               
	#     key="max_score"
	# )

	# # Select Assessment Type
	# asmt_type = st.sidebar.selectbox("Select Assessment Type", ["All"] + list(data['Asmt Mode'].unique()), key="asmt_type")

	# # Select Evaluator (if assessment type is 'peer')
	# if asmt_type == 'peer':
	#     evaluator = st.sidebar.selectbox("Select Evaluator", ["All"] + list(data['EvaluatorName'].unique()), key="evaluator")
	# else:
	#     evaluator = "All"

	# # 📅 Add Date Range Filter
	# st.sidebar.subheader("Select Date Range")

	# start_date = st.sidebar.date_input(
	#     "Start Date",
	#     value=st.session_state.start_date,
	#     min_value=data["Start Time"].min().date(),
	#     max_value=data["Start Time"].max().date()
	# )

	# end_date = st.sidebar.date_input(
	#     "End Date",
	#     value=st.session_state.end_date,
	#     min_value=data["Start Time"].min().date(),
	#     max_value=data["Start Time"].max().date()
	# )

	# # Ensure End Date is after Start Date
	# if start_date > end_date:
	#     st.sidebar.error("⚠️ End Date must be after Start Date!")
	# else:
	#     st.session_state.start_date = start_date
	#     st.session_state.end_date = end_date

	# # 🔹 Apply Filters to Data
	# filtered_data = data[
	#     ((data['PerformerName'] == performer) | (performer == "All")) &
	#     ((data['SkillName'] == skill) | (skill == "All")) &
	#     ((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
	#     ((data['EvaluatorName'] == evaluator) | (evaluator == "All")) &
	#     ((data["Start Time"].dt.date >= st.session_state.start_date) & (data["Start Time"].dt.date <= st.session_state.end_date))
	# ]
	# ################################

	################################	
	st.sidebar.header("Filters")

	# Initialize session state for filters
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

	# Reset Filters Button
	if st.sidebar.button("Reset Filters"):
	    st.session_state.skill = "All"
	    st.session_state.performer = "All"
	    st.session_state.asmt_type = "All"
	    st.session_state.evaluator = "All"
	    st.session_state.start_date = data["Start Time"].min().date()
	    st.session_state.end_date = data["Start Time"].max().date()

	# Select Activity (if multiple activities exist)
	if len(list(data['ActivityName'].unique())) > 1:
	    activity = st.sidebar.selectbox(
	        "Select Activity", 
	        ["All"] + list(data['ActivityName'].unique()), 
	        key="activity"
	    )
	else:
	    activity = list(data['ActivityName'].unique())[0]

	# Select Skill
	skill = st.sidebar.selectbox("Select Skill", ["All"] + list(data['SkillName'].unique()), key="skill")

	# Sidebar numeric inputs for range selection
	min_score = st.sidebar.number_input(
	    "Minimum Score",
	    min_value=0,  
	    max_value=3,  
	    value=0,      
	    step=1,       
	    key="min_score"
	)

	max_score = st.sidebar.number_input(
	    "Maximum Score",
	    min_value=min_score,  
	    max_value=3,          
	    value=3,              
	    step=1,               
	    key="max_score"
	)

	# Select Assessment Type
	asmt_type = st.sidebar.selectbox("Select Assessment Type", ["All"] + list(data['Asmt Mode'].unique()), key="asmt_type")

	# Select Evaluator (if assessment type is 'peer')
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

	st.markdown(
	    """
	    <div style="
	        padding: 10px;
	        background-color: #f7f7f7;
	        border-radius: 5px;
	        color: #333;margin-bottom:20px">
	        <ul style="margin-bottom:0px">
	            <li>This section provides a detailed breakdown of the selected skill's performance.</li>
	            <li>Each component is displayed with its attempt count, score, execution time, and timestamp.</li>
	            <li>The list on the left shows detailed records of each attempt, including the exact time and duration.</li>
	            <li>Filters applied on the left-hand side will dynamically update the displayed data.</li>
	        </ul>
	    </div>
	    """,
	    unsafe_allow_html=True
	)

	# Ensure End Date is after Start Date
	if start_date > end_date:
	    st.sidebar.error("⚠️ End Date must be after Start Date!")
	else:
	    st.session_state.start_date = start_date
	    st.session_state.end_date = end_date

	# 🔹 Apply Filters to Data (Antes de definir o filtro de Performer)
	filtered_data = data[
	    ((data['SkillName'] == skill) | (skill == "All")) &
	    ((data['Asmt Mode'] == asmt_type) | (asmt_type == "All")) &
	    ((data['EvaluatorName'] == evaluator) | (evaluator == "All")) &
	    ((data["Start Time"].dt.date >= st.session_state.start_date) & (data["Start Time"].dt.date <= st.session_state.end_date))
	]

	# 🔹 Atualizar dinamicamente a lista de performers com base nos filtros aplicados
	performer_options = ["All"] + list(filtered_data['PerformerName'].unique())

	performer = st.sidebar.selectbox(
	    "Select Performer", 
	    performer_options, 
	    key="performer"
	)

	# 🔹 Filtragem final dos dados considerando o performer também
	filtered_data = filtered_data[
	    (filtered_data['PerformerName'] == performer) | (performer == "All")
	]
	################################


	# st.dataframe(df)

	
	# Filter data by activity and score
	score_activity = (filtered_data['ActivityName'] == activity)
	score_filter = (filtered_data['Score'] >= min_score) & (filtered_data['Score'] <= max_score)

	filt1 = filtered_data[ score_activity & score_filter]
	# st.dataframe(filt1)

	# st.divider()



	### # filter skill
	if skill == 'All':
		st.warning("Select a skill for individual analysis.")
	else:
		filt2 = filt1[(filt1['SkillName'] == skill)]
		st.write(f"##### Skill: {skill}")

		st.markdown(
		    """
		    <div style="
		        padding: 10px;
		        background-color: #f7f7f7;
		        border-radius: 5px;
		        color: #333;margin-bottom:20px">
		        <ul style="margin-bottom:0px">
		            <li>The list on the left shows detailed records of each attempt, including the exact time and duration.</li>
		            <li>The chart on the right visualizes attempt scores using a color scale:
		                <ul style="margin-top:5px; margin-bottom:5px; padding-left: 20px;">
		                    <li><span style="color:#008000;"><b>Green:</b></span> Higher scores (better execution).</li>
		                    <li><span style="color:#FFD700;"><b>Yellow:</b></span> Moderate scores (room for improvement).</li>
		                    <li><span style="color:#FF0000;"><b>Red:</b></span> Lower scores (areas that need attention).</li>
		                </ul>
		            </li>
		            <li>The x-axis represents the attempt time, helping to analyze consistency over time.</li>
		            <li>Use this section to assess performance trends and identify components that may need additional practice.</li>
		            <li>The marker size ("circle") represents the attempt duration.</li>
		            <li>Filters applied on the left-hand side will dynamically update the displayed data.</li>
		        </ul>
		    </div>
		    """,
		    unsafe_allow_html=True
		)

	# Check if the filtered data is empty
	if filt2.empty:
	    st.warning("No registry found for the selected filters.")
	else:
	    # Process and display performers
		for performer in filt2['PerformerName'].unique():

			col1, col2 = st.columns([1,2])
			st.divider()
			with col1:
				st.write(f"###### Performer: {performer}")
				
				df_graph_duration_score = filt2[(filt2['PerformerName'] == performer)]
				# st.dataframe(df_graph_duration_score)

				for component_text in filt2['Component Name'].unique():
					st.write(f"###### Component: {component_text}")

					filt3 = filt2[(filt2['PerformerName'] == performer) & (filt2['Component Name'] == component_text)]

					# st.dataframe(filt3)

					# Sort and format the data
					filt4 = (
					    filt3[['PerformerName', 'EvaluatorName', 'Attempt(s)', 'Score', 'Start Time', 'Duration(seconds)']]
					    .sort_values(by=['Start Time', 'Score'], ascending=False)
					    .reset_index(drop=True)
					)
			        
					# Generate text output
					# st.write("#### Detailed Attempts")
					for i in filt4.index:
					    aux_txt = (
					        f"- Attempt: {filt4.iloc[i]['Attempt(s)']} - "
					        f"Score: {filt4.iloc[i]['Score']} - "
					        f"Time: {filt4.iloc[i]['Start Time']} - "
					        f"Duration: {filt4.iloc[i]['Duration(seconds)']} seconds"
					    )
					    st.caption(aux_txt)

			with col2:
				graph_duration_score(df_graph_duration_score,performer)

			

					    
				### 

except:
	st.warning('No data loaded', icon="⚠️")



