import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config(page_title = 'Survey Results')
st.header('Survey Results 2021')
st.subheader('Was the tutorial helpful?')

#load dataFrame
excel= '../excelwebapp/Survey_Results.xlsx'
sheet = 'DATA'
df = pd.read_excel(excel,sheet_name=sheet, usecols='B:D',header =3 )
df_participants = pd.read_excel(excel,sheet_name=sheet, usecols='F:G', header=3)

df_participants.dropna(inplace=True)

st.dataframe(df)
pie_chart = px.pie(df_participants,title='Total No. of paricipants',
                   values='Participants', names='Departments' )
st.plotly_chart(pie_chart)

#--streamlit Selection

department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))
department_selection = st.multiselect('Department:',department,
                                      default=department)

## FIlTER DATAFRAME
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
# mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]

st.markdown(f'*Available Results: {number_of_result}*')

#group DataFrame
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()


# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('../excelwebapp/survey.jpg')
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Departments')

st.plotly_chart(pie_chart)