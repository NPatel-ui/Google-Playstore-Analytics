import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import webbrowser

# Load dataset
apps_df = pd.read_csv('Play Store Data.csv')

# 🧹 Clean and convert columns safely
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')
apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')

# Clean Installs — remove non-numeric junk
apps_df['Installs'] = (
    apps_df['Installs']
    .astype(str)
    .str.replace('+', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.extract('(\d+)')  # extract only digits
    .astype(float)
)

# Drop rows with missing key values
apps_df.dropna(subset=['Category', 'Installs', 'Rating', 'Reviews'], inplace=True)

# 🕐 Show only between 12 PM – 1 PM IST
ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
if 12 <= ist_time.hour < 13:

    # ✅ Apply filters
    filtered_df = apps_df[
        (apps_df['Installs'] >= 10000) &
        (apps_df['Rating'] > 4.0)
    ]

    # ✅ Calculate category-wise averages
    category_stats = filtered_df.groupby('Category').agg(
        Avg_Rating=('Rating', 'mean'),
        Avg_Reviews=('Reviews', 'mean')
    ).reset_index()

    # ✅ Identify top & bottom 3 categories
    sorted_df = category_stats.sort_values('Avg_Rating', ascending=False)
    top3 = sorted_df.head(3)['Category']
    bottom3 = sorted_df.tail(3)['Category']

    # Assign colors
    colors = [
        'green' if cat in top3.values else 'red' if cat in bottom3.values else 'blue'
        for cat in category_stats['Category']
    ]

    # ✅ Create bar chart
    fig = go.Figure([
        go.Bar(
            x=category_stats['Category'],
            y=category_stats['Avg_Rating'],
            marker_color=colors,
            text=category_stats['Avg_Reviews'].round(0),
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<br>Avg Reviews: %{text}"
        )
    ])

    # ✅ Layout
    fig.update_layout(
        title='Average Rating & Reviews by App Category (Filtered)',
        xaxis_title='App Category',
        yaxis_title='Average Rating',
        width=1000,
        height=600,
        template='plotly_white'
    )

    # ✅ Save and open
    chart_path = "./avg_rating_reviews_by_category.html"
    fig.write_html(chart_path, full_html=True)
    webbrowser.open('file://' + os.path.realpath(chart_path))

else:
    print("⏰ Chart will only be displayed between 12 PM and 1 PM IST.")
