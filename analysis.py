import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime
import pytz

nltk.download('vader_lexicon')

# Load Datasets
apps_df = pd.read_csv(r'C:\Users\Nitay\Desktop\Google Play Analytics\Play Store Data.csv')
reviews_df = pd.read_csv(r'C:\Users\Nitay\Desktop\Google Play Analytics\User Reviews.csv')

# Data Cleaning
apps_df = apps_df.dropna(subset=['Rating'])
for column in apps_df.columns:
    apps_df[column] = apps_df[column].fillna(apps_df[column].mode()[0])
apps_df.drop_duplicates(inplace=True)
apps_df = apps_df[apps_df['Rating'] <= 5]
reviews_df.dropna(subset=['Translated_Review'], inplace=True)

# Data Transformation
apps_df['Reviews'] = apps_df['Reviews'].astype(int)
apps_df['Installs'] = apps_df['Installs'].str.replace(',', '').str.replace('+', '').astype(int)
apps_df['Price'] = apps_df['Price'].str.replace('$', '').astype(float)

def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024
    else:
        return np.nan

apps_df['Size'] = apps_df['Size'].apply(convert_size)
apps_df['Log_Installs'] = np.log1p(apps_df['Installs'])
apps_df['Log_Reviews'] = np.log1p(apps_df['Reviews'])

def rating_group(rating):
    if rating >= 4:
        return 'Top rated'
    elif rating >= 3:
        return 'Above average'
    elif rating >= 2:
        return 'Average'
    else:
        return 'Below average'

apps_df['Rating_Group'] = apps_df['Rating'].apply(rating_group)
apps_df['Revenue'] = apps_df['Price'] * apps_df['Installs']

sia = SentimentIntensityAnalyzer()
reviews_df['Sentiment_Score'] = reviews_df['Translated_Review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
apps_df['Last Updated'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')
apps_df['Year'] = apps_df['Last Updated'].dt.year

# Tkinter Dashboard
class AppDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Google Play Store Analysis Dashboard")
        self.geometry("1400x900")
        self.configure(bg='lightgray')

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg='lightgray')
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # ---- Place frames for each visualization ----
        # Commenting out undefined methods for now
        # self.create_category_analysis(scrollable_frame, 0, 0)
        # self.create_type_analysis(scrollable_frame, 0, 1)
        # self.create_rating_sentiment_analysis(scrollable_frame, 0, 2)
        # self.create_installation_update_analysis(scrollable_frame, 0, 3)
        # self.create_additional_insights(scrollable_frame, 0, 4)
        # self.create_ml_model_evaluation(scrollable_frame, 0, 5)

        # Filtered grouped bar chart
        self.create_top_categories_grouped_bar(scrollable_frame, 1, 0)

    # ---- Filtered Grouped Bar Chart ----
    def create_top_categories_grouped_bar(self, parent, row, column):
        frame = ttk.Frame(parent, padding="5")
        frame.grid(row=row, column=column, sticky="nsew", pady=5)
        frame.columnconfigure(0, weight=1)

        # Current IST time
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)

        if 15 <= now.hour < 17:  # Only show between 3 PM and 5 PM IST
            filtered_df = apps_df[
                (apps_df['Rating'] >= 4.0) &
                (apps_df['Size'] >= 10) &
                (apps_df['Last Updated'].dt.month == 1)
            ]

            if filtered_df.empty:
                msg = tk.Label(frame, text="No data available for filtered criteria", bg="lightgray", fg="red")
                msg.pack(expand=True, fill="both")
                return

            top_categories = filtered_df.groupby('Category').agg(
                avg_rating=('Rating', 'mean'),
                total_reviews=('Reviews', 'sum')
            ).sort_values(by='total_reviews', ascending=False).head(10)

            fig, ax = plt.subplots(figsize=(7, 4))
            top_categories.plot(kind='bar', ax=ax, color=['skyblue', 'orange'])
            ax.set_title('Top 10 App Categories by Rating & Reviews (Filtered)')
            ax.set_ylabel('Value')
            ax.set_xlabel('Category')
            ax.set_xticklabels(top_categories.index, rotation=45, ha='right')
            ax.legend(["Average Rating", "Total Reviews"])
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            msg = tk.Label(frame, text="This chart is only visible between 3 PM and 5 PM IST", bg="lightgray", fg="red")
            msg.pack(expand=True, fill="both")


# ---- Run Dashboard ----
if __name__ == "__main__":
    app = AppDashboard()
    app.mainloop()

