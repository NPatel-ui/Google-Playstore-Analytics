# Google-Playstore-Analytics
Tkinter | Pandas | Matplotlib | Plotly | Python

This project provides a series of data visualization dashboards for analyzing Google Play Store app data.
Each task demonstrates different visualization techniques, time-based restrictions, category filters, and translation logic using Python, Pandas, Matplotlib, and Plotly.

🧩 Task 1 — Grouped Bar Chart: Category Comparison
Objective:

Visualize and compare average rating and total review count for the top 10 app categories by installs.

Steps:

Filter data where:

Average Rating ≥ 4.0

Size ≥ 10 MB

Last Updated month = January

Group by app category and compute average rating and total reviews.

Plot a grouped bar chart comparing average ratings vs. total reviews.

Visualization is only displayed between 3 PM and 5 PM IST; otherwise, hidden from the dashboard.

Expected Output:

A dual-bar visualization showing how different app categories perform in ratings and review volume among the most-installed apps.

🌍 Task 2 — Interactive Choropleth Map
Objective:

Create an interactive global map showing installs per app category.

Steps:

Use Plotly Choropleth visualization.

Filters applied:

Only top 5 app categories by total installs.

Exclude categories starting with A, C, G, or S.

Highlight categories where installs > 1 million.

Display only between 6 PM and 8 PM IST.

Expected Output:

A colored world map where each country or region represents install distribution intensity. Categories with massive installs are distinctly highlighted.

💰 Task 3 — Dual-Axis Chart (Free vs Paid Apps)
Objective:

Compare average installs and average revenue for Free vs. Paid apps across top 3 categories.

Steps:

Apply filters:

Installs ≥ 10,000

Revenue ≥ $10,000

Android Version > 4.0

Size > 15 MB

Content Rating = Everyone

App Name ≤ 30 characters (including spaces/special symbols)

Create dual-axis line/bar combo chart using Matplotlib.

Display only between 1 PM and 2 PM IST.

Expected Output:

A clear visual of how Free vs Paid apps differ in installs and revenue, highlighting user behavior trends.

⏱️ Task 4 — Time Series Line Chart
Objective:

Show the trend of total installs over time, segmented by app category.

Steps:

Apply filters:

App Name not starting with x, y, z.

App Category starts with E, C, or B.

Reviews > 500.

App Name should not contain letter ‘S’.

Translate categories while plotting:

Beauty → सुंदरता (Hindi)

Business → வணிகம் (Tamil)

Dating → Dating (German)

Highlight growth periods (>20% month-over-month) with shaded areas.

Display only between 6 PM and 9 PM IST.

Expected Output:

An interactive time-series graph showing category-wise growth patterns with translated category names and shaded “growth surge” areas.

🔮 Task 5 — Bubble Chart: Size vs Rating vs Installs
Objective:

Analyze the relationship between app size (MB) and average rating, using bubble size for installs.

Steps:

Filters applied:

Rating > 3.5

Reviews > 500

Installs > 50K

Sentiment Subjectivity > 0.5

App Name not containing letter 'S'

Categories allowed: Game, Beauty, Business, Comics, Communication, Dating, Entertainment, Social, Event

Highlight Game category bubbles in pink.

Translate:

Beauty → सुंदरता (Hindi)

Business → வணிகம் (Tamil)

Dating → Dating (German)

Show only between 5 PM and 7 PM IST.

Expected Output:

A colorful bubble chart where each bubble’s position and size reflect app performance and popularity. The “Game” category appears distinctly in pink.

📈 Task 6 — Stacked Area Chart: Cumulative Installs
Objective:

Visualize cumulative installs over time for each app category using a stacked area chart.

Steps:

Apply filters:

Rating ≥ 4.2

Reviews > 1,000

App Name without numbers.

Category starts with “T” or “P”.

Size between 20 MB and 80 MB.

Translate categories:

Travel & Local → Voyage et Local (French)

Productivity → Productividad (Spanish)

Photography → 写真 (Japanese)

Highlight months where installs increased >25% MoM.

Display only between 4 PM and 6 PM IST.

Expected Output:

A smooth stacked area visualization where color intensity dynamically increases during high-growth months, with translated category legends.

🧠 Technologies Used

Python 3.11+

Pandas — Data processing

NumPy — Numerical calculations

Matplotlib / Seaborn — Static charts

Plotly — Interactive visualization

Tkinter — GUI dashboard

Datetime, ZoneInfo, Pytz — Time-based restrictions

NLTK / TextBlob — Sentiment analysis (for subjectivity filters)

🕐 Time-Based Graph Visibility

Each visualization only renders within its assigned IST time window:

Task	Time Window (IST)	Visualization Type
1	3 PM – 5 PM	Grouped Bar Chart
2	6 PM – 8 PM	Choropleth Map
3	1 PM – 2 PM	Dual-Axis Chart
4	6 PM – 9 PM	Time Series Line Chart
5	5 PM – 7 PM	Bubble Chart
6	4 PM – 6 PM	Stacked Area Chart

If the current time is outside the window, the respective visualization is not displayed on the dashboard.

📂 Project Structure
📁 App_Analysis_Dashboard
│
├── data/
│   └── googleplaystore.csv
│
├── task1_grouped_bar.py
├── task2_choropleth.py
├── task3_dual_axis.py
├── task4_timeseries.py
├── task5_bubble_chart.py
├── task6_stacked_area.py
│
├── dashboard.html
├── main_dashboard.py
└── README.md

🧾 Usage

Open VS Code or any IDE.

Run each task file separately using:

python task1_grouped_bar.py


Or launch the Tkinter dashboard:

python main_dashboard.py


Open dashboard.html in a browser (if applicable).
