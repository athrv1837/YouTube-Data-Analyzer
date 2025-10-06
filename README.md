# 📊 YouTube Data Analyzer

A Streamlit dashboard to analyze your YouTube Studio CSV exports and gain actionable insights into your channel's performance.

---

## 🚀 Features

- 📥 **Upload CSV**: Easily upload your YouTube Studio `Table data.csv` file.
- 🧹 **Automatic Data Cleaning**: Handles missing values, removes summary rows, and ensures correct data types.
- 📈 **Correlation Analysis**: Interactive heatmap to explore relationships between key metrics.
- 👁️‍🗨️ **Audience Retention**: See top and bottom videos by retention, and visualize retention vs. duration.
- 📅 **Time-Series Analysis**: Track total views by publish month.
- 🪣 **Custom Metrics**: Analyze retention by video duration buckets.
- 📤 **Download**: Export cleaned data and plots as CSV or PNG.

---

## 🛠️ Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/Youtube-Data-Analyzer.git
   cd Youtube-Data-Analyzer
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

   > ℹ️ For image downloads, you may also need:
   > ```sh
   > pip install kaleido
   > ```

---

## ▶️ Usage

1. **Run the Streamlit app**
   ```sh
   streamlit run app.py
   ```

2. **In your browser:**
   - Upload your `Table data.csv` from YouTube Studio.
   - Explore the dashboard and download insights.

---

## 📂 File Structure

```
.
├── app.py              # Main Streamlit dashboard
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 📊 Dashboard Sections

- **View Cleaned Data**: Preview your uploaded and cleaned dataset.
- **Download Cleaned Data**: Export the processed CSV.
- **Correlation Analysis**: Interactive heatmap and key insights.
- **Audience Retention Analysis**: Top/bottom videos and scatter plot.
- **Views Over Time**: Line chart of monthly views.
- **Retention by Duration Bucket**: Optional bar chart for retention by video length.

---

## 📝 Notes

- The app expects the following columns in your CSV:
  - `Video title`, `Views`, `Watch time (hours)`, `Subscribers`, `Duration`, `Impressions`, `Impressions click-through rate (%)`, `Average view duration`, `Video publish time`
- If you see a warning about `kaleido`, install it to enable PNG downloads.

---

## 🙋 FAQ

- **Q:** _Where do I get the CSV?_
  - **A:** In YouTube Studio, go to Analytics → Advanced Mode → Export current view.

- **Q:** _Can I use this for other CSVs?_
  - **A:** The app is tailored for YouTube Studio's "Table data.csv" format.

---


