import streamlit as st
import pandas as pd
import plotly.express as px

# Set wide layout
st.set_page_config(layout="wide")
st.title("📈 Congressional Topic Trends Over Time")

# ✅ Load local Excel file
file_path = r"C:\Users\jmathiss\Desktop\Jemaira FNA\Congressional Reports\Congressional Reports xslx basic\Subtopic_to_MainTopic_Mapping_with_summaries.xlsx"
df = pd.read_excel(file_path)

# ✅ Clean topic labels
df['main_topic_summary'] = df['main_topic_summary'].str.replace(r'[.,"]+$', '', regex=True).str.strip()

# ✅ Extract year
df['year'] = df['file_name'].str.extract(r'(\d{4})')
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)

# ✅ Count mentions per year and topic
topic_counts = df.groupby(['year', 'main_topic_summary']).size().reset_index(name='count')

# 📆 Year range slider
min_year = int(topic_counts['year'].min())
max_year = int(topic_counts['year'].max())
selected_years = st.slider("📆 Select Year Range", min_year, max_year, (min_year, max_year))

# 🔘 Topic toggles (as switches)
st.markdown("### 🔧 Show/Hide Topics")
st.markdown("Use the switches below to select which topics to display:")

toggled_topics = []
all_topics = sorted(topic_counts['main_topic_summary'].unique().tolist())
cols = st.columns(3)  # Show toggles in 3 columns

for i, topic in enumerate(all_topics):
    col = cols[i % 3]
    if col.toggle(topic, value=True):
        toggled_topics.append(topic)

# ✂️ Filter by year and toggled topics
filtered_data = topic_counts[
    (topic_counts['main_topic_summary'].isin(toggled_topics)) &
    (topic_counts['year'] >= selected_years[0]) &
    (topic_counts['year'] <= selected_years[1])
]

# 📈 Plot
fig = px.line(
    filtered_data,
    x='year',
    y='count',
    color='main_topic_summary',
    markers=True,
    title="📈 Main Topic Trends Over Time",
    labels={
        'count': 'Number of Mentions',
        'year': 'Year',
        'main_topic_summary': 'Main Topic Summary'
    },
    hover_name='main_topic_summary',
    hover_data={'year': True, 'count': True}
)

fig.update_layout(
    legend_title_text='Main Topic Summary',
    title_x=0.05,
    margin=dict(l=40, r=40, t=80, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# ⬇️ Download filtered data
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_topic_trends.csv",
    mime="text/csv"
)
