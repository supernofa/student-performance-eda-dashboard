import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Student Performance Dashboard', page_icon='📚', layout='wide')

# Calm sage-green and warm neutral colors
SAGE = '#78968A'
DARK_GREEN = '#3F6257'

st.markdown('''
<style>
.stApp { background-color: #F7F8F5; color: #293D35; }
[data-testid="stSidebar"] { background-color: #EDF2ED; }
h1, h2, h3 { color: #36574B !important; }
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E8E1;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="stMetricLabel"] { color: #60766A; }
[data-testid="stMetricValue"] { color: #36574B; }
.stButton > button { background-color: #78968A; color: white; border-radius: 9px; }
</style>
''', unsafe_allow_html=True)

st.title('Student Performance Dashboard')
st.write('Exploring academic, lifestyle, and background factors related to final Portuguese grades.')

@st.cache_data
def load_data():
    return pd.read_csv('student_performance_clean.csv')

df = load_data()

st.sidebar.header('About the Dataset')
st.sidebar.write('Portuguese language performance of students from two secondary schools in Portugal.')
st.sidebar.header('Filters')
schools = st.sidebar.multiselect('School', sorted(df['school'].unique()), default=sorted(df['school'].unique()))
sexes = st.sidebar.multiselect('Sex', sorted(df['sex'].unique()), default=sorted(df['sex'].unique()))
age_range = st.sidebar.slider('Age', int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))

filtered = df[df['school'].isin(schools) & df['sex'].isin(sexes) & df['age'].between(*age_range)]

st.subheader('Dataset Overview')
a, b, c = st.columns(3)
a.metric('Students', len(filtered))
b.metric('Average Final Grade', f"{filtered['G3'].mean():.2f} / 20" if len(filtered) else '—')
c.metric('Average Absences', f"{filtered['absences'].mean():.2f}" if len(filtered) else '—')

if filtered.empty:
    st.warning('No students match these filters. Change the sidebar selections.')
    st.stop()

with st.expander('Preview filtered data'):
    st.dataframe(filtered.head(20).rename(columns={'G3': 'Final Grade', 'G1': 'First Period Grade', 'G2': 'Second Period Grade'}), use_container_width=True)

st.subheader('Grade Distribution')
fig = px.histogram(filtered, x='G3', nbins=21, title='Final Grade Distribution',
                   labels={'G3': 'Final Grade', 'count': 'Number of Students'},
                   color_discrete_sequence=[SAGE])
fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color=DARK_GREEN,
                  yaxis_title='Number of Students')
st.plotly_chart(fig, use_container_width=True)

st.subheader('Explore Relationships')
st.write('Compare average final grades across academic, lifestyle, and background factors.')
category = st.selectbox('Factor group', ['Academic', 'Lifestyle and Social', 'Background', 'Previous Grades'])
options = {
    'Academic': {
        'Study Time': 'studytime',
        'Previous Failures': 'failures',
        'Absences': 'absences',
        'School Support': 'schoolsup',
        'Family Support': 'famsup',
        'Higher Education Plans': 'higher'
    },
    'Lifestyle and Social': {
        'Going Out with Friends': 'goout',
        'Free Time': 'freetime',
        'Family Relationships': 'famrel',
        'Romantic Relationship': 'romantic',
        'Extracurricular Activities': 'activities',
        'Health': 'health'
    },
    'Background': {
        'Age': 'age',
        'Sex': 'sex',
        "Mother's Education": 'Medu',
        "Father's Education": 'Fedu',
        'Home Address': 'address',
        'School': 'school'
    },
    'Previous Grades': {
        'First Period Grade': 'G1',
                'Second Period Grade': 'G2'
    }
}
label = st.selectbox('Choose a feature', list(options[category]))
feature = options[category][label]

# Treat the integer-coded groups as categories so the axis shows discrete values.
# Absences and previous grades have many values, so use a scatter plot of group averages.
means = filtered.groupby(feature, as_index=False).agg(
    average_grade=('G3', 'mean'),
    student_count=('G3', 'size')
).sort_values(feature)

if feature in ['absences', 'G1', 'G2']:
    fig = px.scatter(
        means, x=feature, y='average_grade', size='student_count',
        title=f'Average Final Grade by {label}',
        labels={feature: label, 'average_grade': 'Average Final Grade',
                'student_count': 'Number of Students'},
        color_discrete_sequence=[SAGE],
        hover_data={'student_count': True}
    )
    fig.update_traces(marker=dict(opacity=0.8))
    st.caption('Each dot represents a group of students with the same value; larger dots mean more students.')
else:
    means['group_label'] = means[feature].astype(str)
    fig = px.bar(
        means, x='group_label', y='average_grade',
        title=f'Average Final Grade by {label}',
        labels={'group_label': label, 'average_grade': 'Average Final Grade',
                'student_count': 'Number of Students'},
        color_discrete_sequence=[SAGE],
        hover_data={'student_count': True}
    )
    fig.update_xaxes(type='category')

fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color=DARK_GREEN,
                  yaxis_title='Average Final Grade', yaxis_range=[0, 20])
st.plotly_chart(fig, use_container_width=True)
st.caption('Group averages show associations, not cause and effect. Smaller groups may have less stable averages.')

st.subheader('Absences and Grades')
fig = px.scatter(filtered, x='absences', y='G3', hover_data=['studytime', 'failures'],
                 title='Absences vs Final Grade',
                 labels={'absences': 'Absences', 'G3': 'Final Grade',
                         'studytime': 'Study Time', 'failures': 'Previous Failures'},
                 color_discrete_sequence=[SAGE], opacity=0.7)
fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color=DARK_GREEN)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Key Findings')

st.markdown('**Previous failures and study time**')
st.write('Previous class failures had the strongest negative association with final grades among the selected academic and lifestyle factors (Spearman r = -0.448). Study time showed a positive association (r = 0.275).')

st.markdown('**Lifestyle and social habits**')
st.write('Going out with friends (r = -0.105), free time (r = -0.128), and family relationships (r = 0.048) showed weaker relationships with final grades.')

st.markdown('**Family educational background**')
st.write("Mother's education (r = 0.284) and father's education (r = 0.235) were positively associated with final grades.")

st.markdown('**Overall takeaway**')
st.write('The selected academic factors generally had stronger individual associations with final grades than the lifestyle factors examined.')