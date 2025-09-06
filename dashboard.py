import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# ===========================
# PAGE CONFIG
# ===========================
st.set_page_config(page_title="Fitness Dashboard", layout='wide')

st.title("🏋️ Lifestyle Fitness Dashboard")
st.markdown("Explore your health and fitness trends interactively.")

@st.cache_data
def load_data():
    df = pd.read_csv("fitness_dashboard_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["MonthPeriod"] = df["Date"].dt.to_period("M")   # month-year
    return df

# Load default data
df = load_data()

# If user uploaded a file, replace default
if "user_df" in st.session_state:
    df = st.session_state["user_df"]

# ===========================
# Sidebar Filters
# ===========================
st.sidebar.header("📌 Filters")

# Theme Toggle
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FAFAFA;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Month filter (only months in CSV)
unique_months = df["MonthPeriod"].unique().astype(str)
selected_month = st.sidebar.selectbox("📅 Select Month", options=unique_months, index=len(unique_months)-1)

df_month = df[df["MonthPeriod"] == selected_month]

all_metrics = ["Steps", "Calories", "WorkoutMinutes", "SleepHours", "WaterIntake(L)", "HeartRate"]
selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    options=all_metrics,
    default=all_metrics  
)

# ===========================
# KPI CARDS (Quick Stats)
# ===========================
st.subheader(f"📌 Quick Stats ({selected_month})")

col1, col2, col3 = st.columns(3)

with col1:
    total_steps = df_month["Steps"].sum()
    st.markdown(f"""
    <div style="background-color:#f9f9f9; padding:20px; border-radius:15px; text-align:center; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
         <p style="margin:0; font-size:16px; color:#333; font-weight:600;">Total Steps</p>
        <h2 style="color:#1f77b4; margin-top:0; font-size:32px;">{total_steps:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_sleep = df_month["SleepHours"].mean()
    st.markdown(f"""
    <div style="background-color:#f9f9f9; padding:20px; border-radius:15px; text-align:center; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
         <p style="margin:0; font-size:16px; color:#333; font-weight:600;">Average Sleep</p>
        <h2 style="color:#2ca02c; margin-top:0;">{avg_sleep:.1f} hrs</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_calories = df_month["Calories"].sum()
    st.markdown(f"""
    <div style="background-color:#f9f9f9; padding:20px; border-radius:15px; text-align:center; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
         <p style="margin:0; font-size:16px; color:#333; font-weight:600;">Total Calories</p>
        <h2 style="color:#ff7f0e; margin-top:0;">{total_calories:,}</h2>
    </div>
    """, unsafe_allow_html=True)

# ===========================
# TABS FOR SECTIONS
# ===========================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Graphs", "🤖 Insights", "📈 Trends","📥 Upload Data"])

# ------------------- Tab 1: Graphs -------------------
with tab1:
    st.subheader("Which factors are most connected in my life?")
    if selected_metrics:  
        corr = df[selected_metrics].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, square=True, fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap of Fitness Metrics", fontsize=14, pad=15)
        st.pyplot(fig)  
    else:
        st.info("👉 Please select at least one metric from the sidebar.")

    st.subheader("📈 How do activity patterns evolve across time?")
    if selected_metrics:
        weekly = df.set_index("Date").resample("W")[selected_metrics].sum().reset_index()
        fig = px.area(weekly, x="Date", y=selected_metrics,
                      title="Weekly Activity Breakdown",
                      labels={"value": "Total Activity", "Date": "Week"})
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    # 🔍 Raw Data Viewer
    with st.expander("📂 See Raw Data"):
        st.dataframe(df.head(50))

# ------------------- Tab 2: Insights -------------------
with tab2:
    st.subheader("🤖 AI-Powered Insights")

    def generate_dynamic_insights(df_filtered):
        insights = []
        if df_filtered.empty:
            return ["⚠️ No data available in the selected range."]

        half = len(df_filtered) // 2
        if half < 5:
            return ["ℹ️ Not enough data in this range to detect trends."]

        first_half, second_half = df_filtered.iloc[:half], df_filtered.iloc[half:]
        for col in df_filtered.select_dtypes(include=["float64", "int64"]).columns:
            mean_first, mean_second = first_half[col].mean(), second_half[col].mean()
            change = mean_second - mean_first
            if abs(change) > 0.1 * (mean_first + 1e-6):  
                direction = "increased 📈" if change > 0 else "decreased 📉"
                insights.append(f"Your **{col}** has {direction} in the second half of this period.")

        recent = df_filtered.tail(7)
        for col in recent.select_dtypes(include=["float64", "int64"]).columns:
            mean, std = df_filtered[col].mean(), df_filtered[col].std()
            for val in recent[col]:
                if abs(val - mean) > 2 * std:
                    insights.append(f"⚠️ Unusual values in **{col}** detected recently.")
                    break

        if not insights:
            insights.append("✅ No major changes detected. You're consistent!")

        return insights

    insights = generate_dynamic_insights(df_month)
    for insight in insights:
        st.markdown(f"- {insight}")

# ------------------- Tab 3: Trends -------------------
with tab3:
    st.subheader("📊 Calendar Heatmap of Activity")
    if selected_metrics:
        df["Month"] = df["Date"].dt.strftime("%b")
        df["Weekday"] = df["Date"].dt.day_name()
        heatmap_metric = selected_metrics[0]
        fig = px.density_heatmap(df, x="Weekday", y="Month", z=heatmap_metric,
                                 histfunc="avg", color_continuous_scale="YlGnBu",
                                 title=f"Average {heatmap_metric} by Weekday & Month")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 7-Day Rolling Average of Selected Metrics")
    if selected_metrics:
        df_roll = df.copy()
        for metric in selected_metrics:
            df_roll[f"{metric}_Roll"] = df_roll[metric].rolling(7).mean()
        df_long = df_roll.melt(id_vars="Date",
                               value_vars=[f"{m}_Roll" for m in selected_metrics],
                               var_name="Metric", value_name="Value")
        df_long["Metric"] = df_long["Metric"].str.replace("_Roll", "")
        fig = px.line(df_long, x="Date", y="Value", color="Metric",
                      title="7-Day Rolling Average of Selected Metrics")
        st.plotly_chart(fig, use_container_width=True)

# ------------------- Tab 4: Upload Data -------------------
with tab4:
    st.subheader("📥 Upload Your Data")
    
    uploaded_file = st.file_uploader("Upload your fitness CSV", type=["csv"])

    required_columns = ["Date", "Steps", "Calories", "WorkoutMinutes", "SleepHours", "WaterIntake(L)", "HeartRate"]

    if uploaded_file:
        try:
            df_user = pd.read_csv(uploaded_file)

            if not all(col in df_user.columns for col in required_columns):
                st.error(f"❌ Invalid CSV. Your file must contain these columns:\n\n{', '.join(required_columns)}")
            else:
                df_user["Date"] = pd.to_datetime(df_user["Date"], errors="coerce")
                df_user["MonthPeriod"] = df_user["Date"].dt.to_period("M")
                st.session_state["user_df"] = df_user

                st.success("✅ File uploaded successfully!")
                with st.expander("See raw data"):
                    st.dataframe(df_user.head())
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
