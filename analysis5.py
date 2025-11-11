import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Load dataset
apps_df = pd.read_csv('Play Store Data.csv')

# ✅ Ensure important columns exist (avoid KeyErrors)
for col in ['Rating', 'Reviews', 'Installs', 'App', 'Category', 'Size', 'Sentiment_Subjectivity']:
    if col not in apps_df.columns:
        apps_df[col] = None

# ✅ Get current IST time safely
try:
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(ist)
except:
    from zoneinfo import ZoneInfo
    ist_time = datetime.now(ZoneInfo('Asia/Kolkata'))

# ✅ Show chart only between 5 PM and 7 PM IST
if 16 <= ist_time.hour < 19:
    print(f"✅ Current IST Time: {ist_time.strftime('%I:%M %p')}")
    print("📊 Generating chart...")

    # ✅ Convert numeric columns safely
    apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')
    apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')
    apps_df['Installs'] = apps_df['Installs'].replace('[+,]', '', regex=True).astype(float)

    # ✅ Convert Size column to MB
    def convert_size(size):
        if isinstance(size, str):
            size = size.strip().upper()
            if 'M' in size:
                return float(size.replace('M', ''))
            elif 'K' in size:
                return float(size.replace('K', '')) / 1024
            elif 'G' in size:
                return float(size.replace('G', '')) * 1024
        return None

    apps_df['Size_MB'] = apps_df['Size'].apply(convert_size)

    # ✅ Simplified filters (not too strict)
    filtered_df = apps_df[
        (apps_df['Rating'] > 3.5) &
        (apps_df['Reviews'] > 100) &
        (apps_df['Installs'] > 10000) &
        (apps_df['Size_MB'].notna())
    ].copy()

    # ✅ Translate a few categories if available
    filtered_df['Category'] = filtered_df['Category'].replace({
        'BEAUTY': 'सौंदर्य',        # Hindi
        'BUSINESS': 'வணிகம்',     # Tamil
        'DATING': 'Dating'         # German (same)
    })

    # ✅ If too few rows remain, show fallback sample
    if filtered_df.empty:
        print("⚠️ No data after filtering. Showing sample of original data.")
        filtered_df = apps_df.sample(n=min(50, len(apps_df)), random_state=42)

    # ✅ Custom colors
    color_map = {
        'GAME': 'pink',
        'सौंदर्य': '#8ECFC9',
        'வணிகம்': '#FFB6C1',
        'COMICS': '#A8E6CF',
        'COMMUNICATION': '#FFD3B6',
        'Dating': '#FFAAA5',
        'ENTERTAINMENT': '#D9E4DD',
        'SOCIAL': '#99C1DE',
        'EVENT': '#C3AED6'
    }

    # ✅ Create bubble chart
    fig = px.scatter(
        filtered_df,
        x='Size_MB',
        y='Rating',
        size='Installs',
        color='Category',
        color_discrete_map=color_map,
        hover_name='App',
        title='📱 App Size vs Average Rating (Bubble size = Installs)',
        size_max=60
    )

    fig.update_layout(
        xaxis_title="App Size (MB)",
        yaxis_title="Average Rating",
        template="plotly_white",
        width=900,
        height=500,
        legend_title_text="App Category"
    )

    fig.show()

else:
    print("⏰ Task 5 chart visible only between 5 PM IST and 7 PM IST.")
