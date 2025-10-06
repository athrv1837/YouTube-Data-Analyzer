# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.graph_objects as go
# import warnings
# import io

# warnings.filterwarnings("ignore")

# def load_and_clean_data(uploaded_file):
#     try:
#         # Read CSV
#         df = pd.read_csv(uploaded_file)

#         # Check for required columns
#         required_cols = ['Video title', 'Views', 'Watch time (hours)', 'Subscribers', 'Duration', 
#                          'Impressions', 'Impressions click-through rate (%)', 'Average view duration', 'Video publish time']
#         missing_cols = [col for col in required_cols if col not in df.columns]
#         if missing_cols:
#             return None, f"Missing required columns: {', '.join(missing_cols)}"

#         # Automated cleaning: Remove 'Total' row
#         if df.iloc[0].astype(str).str.contains('Total').any():
#             df = df.iloc[1:].reset_index(drop=True)
        
#         # Drop rows with missing Video title
#         df = df.dropna(subset=['Video title'])
        
#         # Fill missing numeric values with 0
#         numeric_cols = ['Views', 'Watch time (hours)', 'Subscribers', 'Duration', 
#                         'Impressions', 'Impressions click-through rate (%)']
#         df[numeric_cols] = df[numeric_cols].fillna(0)

#         # Convert data types
#         df['Average view duration'] = pd.to_timedelta(df['Average view duration']).dt.total_seconds()
#         df['Video publish time'] = pd.to_datetime(df['Video publish time'], errors='coerce')
#         df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce').fillna(0)

#         # Calculate retention rate
#         df['Retention Rate (%)'] = (df['Average view duration'] / df['Duration']) * 100
#         df['Retention Rate (%)'] = df['Retention Rate (%)'].clip(0, 100)

#         return df, None
#     except Exception as e:
#         return None, f"Error loading data: {str(e)}"

# # Save graph as image 
# def get_image_download_button(fig, filename="plot"):
#     try:
#         buf = io.BytesIO()
#         fig.write_image(buf, format="png")
#         buf.seek(0)
#         return st.download_button(
#             label=f"Download {filename} as PNG",
#             data=buf,
#             file_name=f"{filename}.png",
#             mime="image/png"
#         )
#     except ValueError as e:
#         st.warning("PNG export requires the 'kaleido' package. Please install it with 'pip install --upgrade kaleido' to enable downloads.")
#         return None

# st.title("YouTube Analytics Dashboard")
# st.write("Upload your YouTube Studio 'Table data.csv' file to analyze your channel's performance.")

# # File uploader
# uploaded_file = st.file_uploader("Choose Table data.csv", type=["csv"])

# if uploaded_file is not None:
#     # Load and clean data
#     df, error = load_and_clean_data(uploaded_file)
    
#     if error:
#         st.error(error)
#     else:
#         st.success(f"Data loaded successfully! Found {df.shape[0]} videos.")
        
#         # Display cleaned data
#         with st.expander("View Cleaned Data"):
#             st.dataframe(df[['Video title', 'Duration', 'Views', 'Watch time (hours)', 
#                             'Subscribers', 'Average view duration', 'Impressions', 
#                             'Impressions click-through rate (%)']])
        
#         # Download cleaned data as CSV
#         csv = df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Download Cleaned Data as CSV",
#             data=csv,
#             file_name="cleaned_youtube_data.csv",
#             mime="text/csv"
#         )
        
#         # Correlation Analysis
#         st.header("Correlation Analysis")
#         correlation_data = df[['Views', 'Watch time (hours)', 'Subscribers', 
#                              'Average view duration', 'Impressions', 
#                              'Impressions click-through rate (%)']]
#         corr_matrix = correlation_data.corr()
        
#         # Plot correlation heatmap with Plotly
#         fig1 = go.Figure(data=go.Heatmap(
#             z=corr_matrix.values,
#             x=corr_matrix.columns,
#             y=corr_matrix.columns,
#             text=corr_matrix.values,
#             texttemplate="%{text:.2f}",
#             colorscale='RdBu',
#             zmin=-1, zmax=1
#         ))
#         fig1.update_layout(
#             title="YouTube Analytics Correlation Heatmap",
#             width=600, height=500
#         )
#         st.plotly_chart(fig1)
#         get_image_download_button(fig1, "correlation_heatmap")
        
#         # Display key correlation insights
#         st.subheader("Key Correlation Insights")
#         insights = []
#         for col1 in corr_matrix.columns:
#             for col2 in corr_matrix.columns:
#                 if col1 != col2 and corr_matrix.loc[col1, col2] > 0.7:
#                     insights.append(f"- Strong positive correlation between {col1} and {col2} ({corr_matrix.loc[col1, col2]:.2f})")
#         if insights:
#             for insight in insights:
#                 st.write(insight)
#         else:
#             st.write("No strong correlations (above 0.7) found.")
        
#         # Audience Retention Analysis
#         st.header("Audience Retention Analysis")
        
#         # Top 10 videos by retention
#         st.subheader("Top 10 Videos by Retention Rate")
#         df_sorted = df.sort_values(by='Retention Rate (%)', ascending=False)
#         st.dataframe(df_sorted[['Video title', 'Duration', 'Average view duration', 
#                               'Retention Rate (%)']].head(10))
        
#         # Bottom 10 videos by retention
#         st.subheader("Bottom 10 Videos by Retention Rate")
#         st.dataframe(df_sorted[['Video title', 'Duration', 'Average view duration', 
#                               'Retention Rate (%)']].tail(10))
        
#         # Scatter plot: Retention vs. Duration with Plotly
#         st.subheader("Retention Rate vs. Video Duration")
#         fig2 = px.scatter(
#             df, 
#             x='Duration', 
#             y='Retention Rate (%)', 
#             size='Views', 
#             color='Views', 
#             hover_name='Video title',
#             color_continuous_scale='RdBu',
#             size_max=30
#         )
#         fig2.update_layout(
#             title="Audience Retention vs. Video Duration",
#             xaxis_title="Video Duration (seconds)",
#             yaxis_title="Retention Rate (%)",
#             width=800, height=500
#         )
#         st.plotly_chart(fig2)
#         get_image_download_button(fig2, "retention_scatter")
        
#         # Time-Series Analysis
#         st.header("Views Over Time")
#         df['Publish Month'] = df['Video publish time'].dt.to_period('M').astype(str)
#         monthly_views = df.groupby('Publish Month')['Views'].sum().reset_index()
        
#         # Plot time-series with Plotly
#         fig3 = px.line(
#             monthly_views,
#             x='Publish Month',
#             y='Views',
#             title="Total Views by Publish Month",
#             markers=True
#         )
#         fig3.update_layout(
#             xaxis_title="Publish Month",
#             yaxis_title="Total Views",
#             xaxis_tickangle=45,
#             width=800, height=500
#         )
#         st.plotly_chart(fig3)
#         get_image_download_button(fig3, "views_timeseries")
        
#         # Custom Metrics: Retention by Duration Bucket
#         st.header("Retention by Duration Bucket")
#         show_buckets = st.checkbox("Show Average Retention by Duration Bucket", value=False)
#         if show_buckets:
#             df['Duration Bucket'] = pd.cut(
#                 df['Duration'],
#                 bins=[0, 300, 600, 1200, float('inf')],
#                 labels=['<5min', '5-10min', '10-20min', '>20min']
#             )
#             bucket_retention = df.groupby('Duration Bucket')['Retention Rate (%)'].mean().reset_index()
#             st.dataframe(bucket_retention)
            
#             # Plot retention by duration bucket
#             fig4 = px.bar(
#                 bucket_retention,
#                 x='Duration Bucket',
#                 y='Retention Rate (%)',
#                 title="Average Retention Rate by Duration Bucket"
#             )
#             fig4.update_layout(
#                 xaxis_title="Duration Bucket",
#                 yaxis_title="Average Retention Rate (%)",
#                 width=600, height=400
#             )
#             st.plotly_chart(fig4)
#             get_image_download_button(fig4, "retention_bucket")
# else:
#     st.info("Please upload a CSV file to begin analysis.")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
import io

warnings.filterwarnings("ignore")

def load_and_clean_data(uploaded_file):
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Check for required columns
        required_cols = ['Video title', 'Views', 'Watch time (hours)', 'Subscribers', 'Duration', 
                         'Impressions', 'Impressions click-through rate (%)', 'Average view duration', 'Video publish time']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return None, f"Missing required columns: {', '.join(missing_cols)}"

        # Automated cleaning: Remove 'Total' row
        if df.iloc[0].astype(str).str.contains('Total').any():
            df = df.iloc[1:].reset_index(drop=True)
        
        # Drop rows with missing Video title
        df = df.dropna(subset=['Video title'])
        
        # Fill missing numeric values with 0
        numeric_cols = ['Views', 'Watch time (hours)', 'Subscribers', 'Duration', 
                        'Impressions', 'Impressions click-through rate (%)']
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Convert data types
        df['Average view duration'] = pd.to_timedelta(df['Average view duration']).dt.total_seconds()
        df['Video publish time'] = pd.to_datetime(df['Video publish time'], errors='coerce')
        df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce').fillna(0)

        # Calculate retention rate
        df['Retention Rate (%)'] = (df['Average view duration'] / df['Duration']) * 100
        df['Retention Rate (%)'] = df['Retention Rate (%)'].clip(0, 100)

        return df, None
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

# Save graph as image 
def get_image_download_button(fig, filename="plot"):
    try:
        buf = io.BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)
        return st.download_button(
            label=f"Download {filename} as PNG",
            data=buf,
            file_name=f"{filename}.png",
            mime="image/png"
        )
    except ValueError as e:
        st.warning("PNG export requires the 'kaleido' package. Please install it with 'pip install --upgrade kaleido' to enable downloads.")
        return None

st.title("YouTube Analytics Dashboard")
st.write("Upload your YouTube Studio 'Table data.csv' file to analyze your channel's performance. This dashboard simplifies complex YouTube analytics into actionable insights.")

# File uploader
uploaded_file = st.file_uploader("Choose Table data.csv", type=["csv"])

if uploaded_file is not None:
    # Load and clean data
    df, error = load_and_clean_data(uploaded_file)
    
    if error:
        st.error(error)
    else:
        st.success(f"Data loaded successfully! Found {df.shape[0]} videos.")
        
        # Display cleaned data
        with st.expander("View Cleaned Data"):
            st.dataframe(df[['Video title', 'Duration', 'Views', 'Watch time (hours)', 
                            'Subscribers', 'Average view duration', 'Impressions', 
                            'Impressions click-through rate (%)']])
        
        # Download cleaned data as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=csv,
            file_name="cleaned_youtube_data.csv",
            mime="text/csv"
        )
        
        # Correlation Analysis
        st.header("Correlation Analysis")
        correlation_data = df[['Views', 'Watch time (hours)', 'Subscribers', 
                             'Average view duration', 'Impressions', 
                             'Impressions click-through rate (%)']]
        corr_matrix = correlation_data.corr()
        
        # Plot correlation heatmap with Plotly
        fig1 = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            text=corr_matrix.values,
            texttemplate="%{text:.2f}",
            colorscale='RdBu',
            zmin=-1, zmax=1
        ))
        fig1.update_layout(
            title="YouTube Analytics Correlation Heatmap",
            width=600, height=500
        )
        st.plotly_chart(fig1)
        get_image_download_button(fig1, "correlation_heatmap")
        
        # Display key correlation insights
        st.subheader("Key Correlation Insights")
        insights = []
        for col1 in corr_matrix.columns:
            for col2 in corr_matrix.columns:
                if col1 != col2 and corr_matrix.loc[col1, col2] > 0.7:
                    insights.append(f"- Strong positive correlation between {col1} and {col2} ({corr_matrix.loc[col1, col2]:.2f})")
        if insights:
            for insight in insights:
                st.write(insight)
        # Audience Retention Analysis
        st.header("Audience Retention Analysis")
        
        # Top 10 videos by retention
        st.subheader("Top 10 Videos by Retention Rate")
        df_sorted = df.sort_values(by='Retention Rate (%)', ascending=False)
        st.dataframe(df_sorted[['Video title', 'Duration', 'Average view duration', 
                              'Retention Rate (%)']].head(10))
        
        # Bottom 10 videos by retention
        st.subheader("Bottom 10 Videos by Retention Rate")
        st.dataframe(df_sorted[['Video title', 'Duration', 'Average view duration', 
                              'Retention Rate (%)']].tail(10))
        
        
        # Scatter plot: Retention vs. Duration with Plotly
        st.subheader("Retention Rate vs. Video Duration")
        fig2 = px.scatter(
            df, 
            x='Duration', 
            y='Retention Rate (%)', 
            size='Views', 
            color='Views', 
            hover_name='Video title',
            color_continuous_scale='RdBu',
            size_max=30
        )
        fig2.update_layout(
            title="Audience Retention vs. Video Duration",
            xaxis_title="Video Duration (seconds)",
            yaxis_title="Retention Rate (%)",
            width=800, height=500
        )
        st.plotly_chart(fig2)
        get_image_download_button(fig2, "retention_scatter")
        
        # Time-Series Analysis
        st.header("Views Over Time")
        df['Publish Month'] = df['Video publish time'].dt.to_period('M').astype(str)
        monthly_views = df.groupby('Publish Month')['Views'].sum().reset_index()
        
        # Plot time-series with Plotly
        fig3 = px.line(
            monthly_views,
            x='Publish Month',
            y='Views',
            title="Total Views by Publish Month",
            markers=True
        )
        fig3.update_layout(
            xaxis_title="Publish Month",
            yaxis_title="Total Views",
            xaxis_tickangle=45,
            width=800, height=500
        )
        st.plotly_chart(fig3)
        get_image_download_button(fig3, "views_timeseries")
        
        
        # Custom Metrics: Retention by Duration Bucket
        st.header("Retention by Duration Bucket")
        show_buckets = st.checkbox("Show Average Retention by Duration Bucket", value=False)
        if show_buckets:
            df['Duration Bucket'] = pd.cut(
                df['Duration'],
                bins=[0, 300, 600, 1200, float('inf')],
                labels=['<5min', '5-10min', '10-20min', '>20min']
            )
            bucket_retention = df.groupby('Duration Bucket')['Retention Rate (%)'].mean().reset_index()
            st.dataframe(bucket_retention)
            
            # Plot retention by duration bucket
            fig4 = px.bar(
                bucket_retention,
                x='Duration Bucket',
                y='Retention Rate (%)',
                title="Average Retention Rate by Duration Bucket"
            )
            fig4.update_layout(
                xaxis_title="Duration Bucket",
                yaxis_title="Average Retention Rate (%)",
                width=600, height=400
            )
            st.plotly_chart(fig4)
            get_image_download_button(fig4, "retention_bucket")
        
else:
    st.info("Please upload a CSV file to begin analysis.")