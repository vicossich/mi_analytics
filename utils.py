from datetime import datetime
import pandas as pd


def cleanning_data(data):
    ##########################
    """
    Checking var names and adjust to the same pattern:

    Different version of the system demosntrates different var names this ensure 
    the df to have the same var names
    """

    data.columns = data.columns.str.strip()

    """
    Sorting Data:

    The data is organized by two key factors: the name of the skill 
    being performed and the name of the specific component related 
    to that skill. Sorting the data in this way helps to better 
    analyze and understand trends or patterns.
    """
    #--- Sort the data by 'SkillName' and 'Component Name' for better organization
    try:
        data.sort_values(by=['SkillName', 'Component Name'], inplace=True)
    except:
        data.sort_values(by=['Skill_Name', 'Question_Name'], inplace=True)

    """
    Cleaning the Data:

    Any row that contains a specific component called 
    "SummaryScore" is removed from the dataset. 
    This ensures that only relevant data is analyzed.
    """
    #--- Remove rows where 'Component Name' is 'SummaryScore' to clean the dataset
    try:
        data = data[data['Component Name'] != 'SummaryScore'].copy()
    except:
        data = data[data['Question_Name'] != 'SummaryScore'].copy()

    ##########################
    """
    Converting Text to Date/Time Format:

    The data contains times that are written as text. These
    text values are converted into actual time values so 
    that calculations can be made later. For example, 
    instead of having a time written as '5:57 PM,' it's 
    transformed into a format the computer can understand as 
    '5:57:35 PM' on a specific date.
    """
    #--- Convert 'Start Time' and 'End Time' from strings to datetime objects for further analysis

    # def str2datetime(date_string):
    #     """
    #     Converts a date-time string to a datetime object.
        
    #     The input date-time string should be in the format 'Friday, December 3, 2021 5:57:35 PM'.
        
    #     Args:
    #         date_string (str): The date-time string to be converted.
        
    #     Returns:
    #         datetime: A datetime object representing the parsed date and time.
        
    #     Raises:
    #         ValueError: If the date_string does not match the expected format.
        
    #     Example:
    #         >>> str2datetime('Friday, December 3, 2021 5:57:35 PM')
    #         datetime.datetime(2021, 12, 3, 17, 57, 35)
    #     """

    #     try:
    #         # Define the expected date-time format
    #         date_format = '%A, %B %d, %Y %I:%M:%S %p'

    #         # Convert the string to a datetime object
    #         parsed_date = datetime.strptime(date_string, date_format)

    #     except:
    #         date_format = "%Y-%m-%d-%H:%M:%S.%f" 
    #         # Convert the string to a datetime object
    #         parsed_date = datetime.strptime(date_string, date_format)


    #     return parsed_date
    def str2datetime(date_string):
        """
        Converts a date-time string to a datetime object, handling multiple formats 
        and ignoring missing values (e.g., 'na', 'N/A', or empty strings).
        
        Supported formats:
        1. 'Friday, December 3, 2021 5:57:35 PM'  (Long format with AM/PM)
        2. '2024-12-11-10:41:30'  (ISO-like without milliseconds)
        3. '2023-08-02-13:28:36.843'  (ISO-like with milliseconds)

        Args:
            date_string (str): The date-time string to be converted.
        
        Returns:
            datetime or None: A datetime object if successful, or None if the input is invalid.
        
        Example:
            >>> str2datetime('Friday, December 3, 2021 5:57:35 PM')
            datetime.datetime(2021, 12, 3, 17, 57, 35)

            >>> str2datetime('2024-12-11-10:41:30')
            datetime.datetime(2024, 12, 11, 10, 41, 30)

            >>> str2datetime('2023-08-02-13:28:36.843')
            datetime.datetime(2023, 8, 2, 13, 28, 36, 843000)

            >>> str2datetime('na')  # Returns None
            >>> str2datetime('N/A')  # Returns None
        """
        # Define a list of invalid values to treat as missing data
        invalid_values = {"na", "N/A", "null", "", None}

        if date_string in invalid_values:
            return None  # Return None for missing or invalid values

        date_formats = [
            "%A, %B %d, %Y %I:%M:%S %p",  # Long format with weekday and AM/PM
            "%Y-%m-%d-%H:%M:%S.%f",       # ISO-like format with milliseconds
            "%Y-%m-%d-%H:%M:%S"           # ISO-like format without milliseconds
        ]

        for date_format in date_formats:
            try:
                return datetime.strptime(date_string, date_format)
            except ValueError:
                continue  # Try the next format

        # If no format matches, return None instead of raising an error
        return None

    # Apply the string-to-datetime conversion to the 'Start Time' and 'End Time' columns
    data['Start Time'] = data['Start Time'].apply(str2datetime)
    data['End Time'] = data['End Time'].apply(str2datetime)

    ##########################
    """
    Splitting Team Information:

    Each row in the data contains a team name and an ID 
    combined into one field. The code separates these into 
    two parts: one for the team name and one for the team ID. 
    This makes it easier to identify and analyze the data for 
    each team separately.
    """
    #--- Split the 'Team Name-ID' column into separate 'Team Name' and 'Team ID' columns
    def split_teamname(item):
        """
        Splits a string containing a team name and team ID into separate components.
        
        The input string should be in the format 'TeamName, TeamID'.
        
        Args:
            item (str): The string containing the team name and team ID, separated by a comma and a space.
        
        Returns:
            tuple: A tuple containing the team name and team ID as separate elements.
        
        Example:
            >>> split_teamname('Warriors, 001')
            ('Warriors', '001')
        
        Usage:
            data[['TeamName', 'TeamID']] = data['Team Name-ID'].apply(lambda x: pd.Series(split_teamname(x)))
        """
        
        # Split the string at the last '-' to separate Team Name and Team ID
        split_string = item.rsplit('-', 5)

        # Assign Team Name and Team ID from the split components
        TeamName = split_string[0]
        TeamID = f'{split_string[1]}-{split_string[2]}-{split_string[3]}-{split_string[4]}-{split_string[5]}'

        return TeamName, TeamID 

    try:
        # Apply the split function to the 'Team Name-ID' column
        data[['TeamName', 'TeamID']] = data['Team Name-ID'].apply(lambda x: pd.Series(split_teamname(x)))
    except:
        data['TeamName'] = data["Class_Name"]
        data['TeamID'] = data["Class_ID"]


    """
    Calculating Duration:

    The code calculates the amount of time that passed 
    between two moments, called "Start Time" and "End Time." 
    This helps to understand how long a particular event or 
    action took. The result is shown in seconds.
    """
    #--- Calculate the duration in seconds between 'Start Time' and 'End Time'
    def calculate_duration(start_time, end_time):
        """
        Calculate the duration between two datetime objects in seconds.

        Args:
            start_time (datetime): The starting time.
            end_time (datetime): The ending time.

        Returns:
            float: The duration between start_time and end_time in seconds.

        Example:
            >>> from datetime import datetime
            >>> start_time = datetime(2024, 8, 28, 16, 3, 24)
            >>> end_time = datetime(2024, 8, 28, 16, 4, 24)
            >>> calculate_duration(start_time, end_time)
            60.0
        """
        
        # Calculate the total duration in seconds
        duration = (end_time - start_time).total_seconds()
        
        return duration 

    """
    Filtering Completed Events:

    Not all actions or attempts in the dataset were completed,
    so the code checks to see which ones have a valid "End Time." 
    It keeps only the rows where the action was completed, and 
    removes any incomplete attempts.
    """
    # Calculate the duration and create a new column 'Duration(seconds)'
    data['Duration(seconds)'] = data.apply(lambda row: calculate_duration(row['Start Time'], row['End Time']), axis=1)

    """
    Final Filtering:

    Finally, the code applies a filter to ensure the data is 
    clean and accurate, leaving only the rows where all necessary 
    information is available, especially focusing on completed attempts 
    with valid start and end times.
    """
    #--- Filter the data to include only completed attempts (those with a valid 'End Time')
    # Create a new column 'isFinished' to indicate whether an attempt has a valid 'End Time'
    data['isFinished'] = data['End Time'].notnull() & data['End Time'].apply(lambda x: pd.notna(x) and x != '')

    """
    Filtering just finished attempts
    """
    # Filter the DataFrame to include only rows where 'isFinished' is True
    data = data[data['isFinished'] == True].copy().reset_index(drop=True)


    ######################################################
    """
    Ajustanto a retrocompatibilidade com os dados do DF
    """

    # Dicionário de mapeamento: renomeia apenas as colunas necessárias
    column_mapping = {
        "Activity_Name": "ActivityName",
        "Skill_Name": "SkillName",
        "SkillID": "SkillID",
        "Question_Name": "Component Name",
        "QuestionID": "QuestionID",
        "Instructor_Name": "InstructorID",
        "InstructorID": "InstructorID",
        "Performer_Name": "PerformerName",
        "PerformerID": "PerformerID",
        "Evaluator_Name": "EvaluatorName",
        "EvaluatorID": "EvaluatorID",
        "Class_Name": "Team_Name_ID",
        "Class_ID": "Class_ID",
        "Assessment_Type": "Asmt Mode",
        "Attempts": "Attempt(s)",
        "Score": "Score",
        "Start_Time": "Start_Time",
        "End_Time": "End_Time",
        "Fair_job?": "FairJob?",
        "GoodAt?": "GoodAt?",
        "Like?": "Like?"
    }

    def standardize_columns(df):
        """
        Renomeia as colunas do DataFrame para o formato antigo sem remover colunas extras.
        
        Args:
            df (pd.DataFrame): DataFrame original carregado.
        
        Returns:
            pd.DataFrame: DataFrame com colunas renomeadas conforme a versão antiga.
        """
        df = df.rename(columns=column_mapping)  # Apenas renomeia colunas conhecidas
        return df


    data = standardize_columns(data)
    print('aqui')
    print(data.columns)
    ######################################################

    return data


######
# vd = 'Duration(seconds)'
# vd = 'Score'
# vd = 'Attempt(s)'

def general_skill_performance(df, vd, option='SkillName'):
    """
    Computes descriptive statistics for the specified skill or option in the dataset.

    This function groups the dataset by a specified option and calculates the count,
    mean, minimum, and maximum values for a given variable. The results are rounded
    to one decimal place and returned in a new DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be analyzed.
        vd (str): The name of the variable/column in the DataFrame for which the statistics will be calculated.
        option (str, optional): The column name by which to group the data. Defaults to 'SkillName'.

    Returns:
        pandas.DataFrame: A DataFrame containing the grouped statistics, including the count, mean, min, and max values.
    """
    aux = df[[option,vd]].groupby(by=option).describe().round(1).reset_index().copy()

    columns_to_keep = [
        (option, ''),
        (vd, 'count'),
        (vd, 'mean'),
        (vd, 'min'),
        (vd, 'max')
    ]

    # Select only the desired columns using .loc
    aux = aux.loc[:, columns_to_keep]

    aux.columns = [option,'count','mean','min','max']
    
    return aux


def general_component_performance(df, vd):
    """
    Computes descriptive statistics for components of each skill in the dataset.

    This function groups the dataset by both 'SkillName' and 'Component Name' to calculate 
    the count, mean, minimum, and maximum values for a given variable. The results are 
    rounded to one decimal place and returned in a dictionary, where each skill has 
    its own DataFrame summarizing the performance of its components.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be analyzed.
        vd (str): The name of the variable/column in the DataFrame for which the statistics will be calculated.

    Returns:
        list: A list of unique skill names present in the dataset.
        dict: A dictionary where each key is a skill name, and the value is a DataFrame containing 
              the grouped statistics (count, mean, min, max) for each component of that skill.
    """
    
    try:
        aux = df[['SkillName','Component Name',vd]].groupby(by=['SkillName','Component Name']).describe().round(1).reset_index().copy()
        columns_to_keep = [
            ('SkillName', ''),
            ('Component Name', ''),
            (vd, 'count'),
            (vd, 'mean'),
            (vd, 'min'),
            (vd, 'max')
        ]

    except:
        aux = df[['Skill_Name','Question_Name',vd]].groupby(by=['Skill_Name','Question_Name']).describe().round(1).reset_index().copy()
        columns_to_keep = [
            ('Skill_Name', ''),
            ('Question_Name', ''),
            (vd, 'count'),
            (vd, 'mean'),
            (vd, 'min'),
            (vd, 'max')
        ]

    
    # Select only the desired columns using .loc
    aux = aux.loc[:, columns_to_keep]

    aux.columns = ['SkillName','Component Name','count','mean','min','max']
    
    # list with skills
    try:
        skillNamesList = aux['SkillName'].unique()
    except:
        skillNamesList = aux['Skill_Name'].unique()

    output = {}
    # create subsets to sumarize the components results by skill
    for name in skillNamesList:
        try:
            t = aux[aux['SkillName']==name]
        except:
            t = aux[aux['Skill_Name']==name]
        
        output[name] = t
    
    
    return skillNamesList, output
