import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Load dataset
apps_df = pd.read_csv('Play Store Data.csv')

# Get current IST time
try:
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist)
except:
    from zoneinfo import ZoneInfo
    ist_time = datetime.now(ZoneInfo('Asia/Kolkata'))

# Show chart only between 6 PM and 9 PM IST
if 18 <= ist_time.hour < 21:

    # Filter according to the conditions
    filtered_df = apps_df[
        (~apps_df['App'].str.lower().str.startswith(('x', 'y', 'z'))) &
        (apps_df['Category'].str.startswith(('E', 'C', 'B'))) &
        (apps_df['Reviews'] > 500) &
        (~apps_df['App'].str.contains('S', case=False, na=False))
    ].copy()

    # Translate categories
    filtered_df['Category'] = filtered_df['Category'].replace({
        'BEAUTY': 'सौंदर्य',        # Hindi
        'BUSINESS': 'வணிகம்',     # Tamil
        'DATING': 'Dating'         # German (same)
    })

    # Convert 'Last Updated' or 'Updated' column to datetime (if available)
    date_col = None
    for col in ['Last Updated', 'Updated', 'Release Date']:
        if col in filtered_df.columns:
            date_col = col
            filtered_df[col] = pd.to_datetime(filtered_df[col], errors='coerce')
            break

    if date_col:
        filtered_df['Month'] = filtered_df[date_col].dt.to_period('M')
    else:
        # If no date column, create a dummy month column
        filtered_df['Month'] = pd.date_range(start='2020-01-01', periods=len(filtered_df), freq='M').to_period('M')

    # Aggregate installs by month and category
    trend_df = filtered_df.groupby(['Month', 'Category'])['Installs'].sum().reset_index()
    trend_df['Month'] = trend_df['Month'].astype(str)

    # Calculate month-over-month percentage change
    trend_df['MoM_Growth'] = trend_df.groupby('Category')['Installs'].pct_change() * 100

    # Plot line chart
    fig = go.Figure()

    for category in trend_df['Category'].unique():
        cat_data = trend_df[trend_df['Category'] == category]
        fig.add_trace(go.Scatter(
            x=cat_data['Month'],
            y=cat_data['Installs'],
            mode='lines+markers',
            name=category
        ))

        # Shade regions with >20% MoM growth
        growth_periods = cat_data[cat_data['MoM_Growth'] > 20]
        if not growth_periods.empty:
            fig.add_trace(go.Scatter(
                x=growth_periods['Month'],
                y=growth_periods['Installs'],
                mode='lines',
                name=f"{category} - Growth>20%",
                fill='tozeroy',
                opacity=0.3,
                line=dict(width=0.5)
            ))

    fig.update_layout(
        title="📈 Total Installs Over Time by Category (with >20% Growth Highlighted)",
        xaxis_title="Month",
        yaxis_title="Total Installs",
        template="plotly_white",
        width=900,
        height=500
    )

    fig.show()
else:
    print("⏰ Task 4 chart visible only between 6 PM IST and 9 PM IST.")
