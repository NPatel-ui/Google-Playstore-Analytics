import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz
import os
import webbrowser

# Load dataset
apps_df = pd.read_csv('Play Store Data.csv')

# Clean and preprocess numeric columns safely
def clean_numeric(x):
    if pd.isna(x):
        return np.nan
    x = str(x).replace(',', '').replace('+', '').replace('M', '').replace('k', '').strip()
    if x.lower() == 'varies with device' or x == '':
        return np.nan
    try:
        return float(x)
    except:
        return np.nan

apps_df['Installs'] = apps_df['Installs'].apply(clean_numeric)
apps_df['Size'] = apps_df['Size'].apply(clean_numeric)
apps_df['Revenue'] = apps_df['Revenue'].apply(clean_numeric) if 'Revenue' in apps_df.columns else apps_df['Installs'] * 0.05

# Clean Android Version
apps_df['Android Ver'] = apps_df['Android Ver'].astype(str).replace('Varies with device', '0')
apps_df['Android Ver'] = pd.to_numeric(apps_df['Android Ver'], errors='coerce')

# Drop rows with missing important data
apps_df.dropna(subset=['Installs', 'Size', 'Android Ver'], inplace=True)

# Check IST time
ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
if 13 <= ist_time.hour < 14:  # 1 PM to 2 PM IST

    # Apply filters
    filtered_df = apps_df[
        (apps_df['Installs'] >= 10000) &
        (apps_df['Revenue'] >= 10000) &
        (apps_df['Android Ver'] > 4.0) &
        (apps_df['Size'] > 15) &
        (apps_df['Content Rating'] == 'Everyone') &
        (apps_df['App'].str.len() <= 30)
    ]

    # Get top 3 categories by installs
    top_categories = filtered_df.groupby('Category')['Installs'].sum().nlargest(3).index
    filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

    # Calculate average installs and revenue per Type (Free/Paid) for each category
    summary_df = filtered_df.groupby(['Category', 'Type']).agg(
        Avg_Installs=('Installs', 'mean'),
        Avg_Revenue=('Revenue', 'mean')
    ).reset_index()

    # Plot dual-axis chart
    fig = go.Figure()

    for cat in top_categories:
        cat_data = summary_df[summary_df['Category'] == cat]
        fig.add_trace(
            go.Bar(
                x=cat_data['Type'],
                y=cat_data['Avg_Installs'],
                name=f'{cat} - Avg Installs',
                yaxis='y1'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=cat_data['Type'],
                y=cat_data['Avg_Revenue'],
                name=f'{cat} - Avg Revenue',
                yaxis='y2',
                mode='lines+markers'
            )
        )

    # Layout
    fig.update_layout(
        title='Average Installs vs Revenue for Free vs Paid Apps (Top 3 Categories)',
        xaxis=dict(title='App Type'),
        yaxis=dict(title='Average Installs', side='left'),
        yaxis2=dict(title='Average Revenue ($)', overlaying='y', side='right'),
        width=800,
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Save and open HTML
    chart_path = "./dual_axis_installs_revenue.html"
    fig.write_html(chart_path, full_html=True)
    webbrowser.open('file://' + os.path.realpath(chart_path))

else:
    print("⏰ Chart visible only between 1 PM and 2 PM IST.")
