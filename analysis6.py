import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytz

# Load dataset
apps_df = pd.read_csv('Play Store Data.csv')

# ✅ Handle IST time
try:
    ist_time = datetime.now(pytz.timezone('Asia/Kolkata'))
except:
    from zoneinfo import ZoneInfo
    ist_time = datetime.now(ZoneInfo('Asia/Kolkata'))

# ✅ Display chart only between 4 PM and 6 PM IST
if 16 <= ist_time.hour < 18:

    # Convert 'Size' to MB numeric
    def convert_size(size):
        if isinstance(size, str):
            size = size.strip().upper()
            if 'M' in size:
                return float(size.replace('M', ''))
            elif 'K' in size:
                return float(size.replace('K', '')) / 1024
            elif 'G' in size:
                return float(size.replace('G', '')) * 1024
        return np.nan

    apps_df['Size_MB'] = apps_df['Size'].apply(convert_size)

    # ✅ Clean Reviews and Installs columns
    apps_df['Reviews'] = apps_df['Reviews'].astype(str).str.replace(',', '').str.replace('+', '')
    apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')

    apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace('[+,]', '', regex=True)
    apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')

    # ✅ Apply filters
    filtered_df = apps_df[
        (apps_df['Rating'] >= 4.2) &
        (apps_df['Reviews'] > 1000) &
        (apps_df['Size_MB'].between(20, 80)) &
        (~apps_df['App'].str.contains(r'\d', na=False)) &
        (apps_df['Category'].str.startswith(('T', 'P')))
    ].copy()

    # ✅ Parse Last Updated column to datetime
    filtered_df['Last Updated'] = pd.to_datetime(filtered_df['Last Updated'], errors='coerce')
    filtered_df.dropna(subset=['Last Updated'], inplace=True)

    # Extract month-year
    filtered_df['Month'] = filtered_df['Last Updated'].dt.to_period('M').astype(str)

    # ✅ Aggregate installs by category and month
    installs_over_time = filtered_df.groupby(['Category', 'Month'])['Installs'].sum().reset_index()

    # ✅ Translate categories
    installs_over_time['Category'] = installs_over_time['Category'].replace({
        'Travel & Local': 'Voyage et Local',     # French
        'Productivity': 'Productividad',         # Spanish
        'Photography': '写真'                     # Japanese
    })

    # ✅ Pivot to wide format
    pivot_df = installs_over_time.pivot(index='Month', columns='Category', values='Installs').fillna(0)
    pivot_df = pivot_df.sort_index()

    # ✅ Calculate cumulative installs
    cumulative_df = pivot_df.cumsum()

    # ✅ Convert installs to millions to reduce load
    cumulative_df = cumulative_df / 1_000_000

    # ✅ Calculate month-over-month growth
    growth_df = cumulative_df.pct_change().fillna(0)

    # ✅ Define colors for categories
    colors = px.colors.qualitative.Pastel + px.colors.qualitative.Bold

    # ✅ Create stacked area chart
    fig = go.Figure()

    for i, category in enumerate(cumulative_df.columns):
        fig.add_trace(go.Scatter(
            x=cumulative_df.index,
            y=cumulative_df[category],
            mode='lines',
            name=category,
            stackgroup='one',
            line=dict(width=0.5, color=colors[i % len(colors)]),
            fill='tonexty',
            opacity=0.8  # fixed opacity for faster rendering
        ))

    # ✅ Layout settings
    fig.update_layout(
        title="📈 Cumulative Installs Over Time by Category (in Millions)",
        xaxis_title="Month",
        yaxis_title="Cumulative Installs (Millions)",
        legend_title="App Category",
        template="plotly_white",
        width=950,
        height=550
    )

    # ✅ Save chart as HTML instead of opening localhost
    output_file = "cumulative_installs_chart.html"
    fig.write_html(output_file)
    print(f"✅ Chart saved as '{output_file}'. Open this file in any browser to view.")

else:
    print("⏰ Task 6 chart visible only between 4 PM IST and 6 PM IST.")
