import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Cookie Cats A/B Test Dashboard", layout="wide")

# Connect to database and load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('cookie_cats.db')
    
    # Aggregated metrics query
    query_agg = """
    SELECT 
        version,
        COUNT(userid) AS total_users,
        SUM(sum_gamerounds) AS total_gamerounds,
        ROUND(AVG(sum_gamerounds), 2) AS avg_gamerounds,
        SUM(CASE WHEN retention_1 = 1 THEN 1 ELSE 0 END) AS retained_day_1,
        SUM(CASE WHEN retention_7 = 1 THEN 1 ELSE 0 END) AS retained_day_7,
        ROUND(CAST(SUM(CASE WHEN retention_1 = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(userid) * 100, 2) AS day_1_retention_pct,
        ROUND(CAST(SUM(CASE WHEN retention_7 = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(userid) * 100, 2) AS day_7_retention_pct
    FROM user_data
    GROUP BY version;
    """
    df_agg = pd.read_sql(query_agg, conn)
    
    # Raw data for distribution (filtering extreme outliers)
    query_raw = """
    SELECT * 
    FROM user_data 
    WHERE sum_gamerounds <= 200;
    """
    df_raw = pd.read_sql(query_raw, conn)
    
    conn.close()
    return df_agg, df_raw

try:
    df_agg, df_raw = load_data()
except Exception as e:
    st.error("Could not load data. Please ensure you have run the Jupyter notebook first to create the cookie_cats.db file.")
    st.stop()

# Title
st.title("🐱 Cookie Cats A/B Test Results")
st.markdown("### Analyzing the impact of moving the first gate from level 30 to level 40.")
st.markdown("---")

# Metrics row
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

gate_30_data = df_agg[df_agg['version'] == 'gate_30'].iloc[0]
gate_40_data = df_agg[df_agg['version'] == 'gate_40'].iloc[0]

with col1:
    st.metric("Total Players (Gate 30)", f"{gate_30_data['total_users']:,}")
    st.metric("Total Players (Gate 40)", f"{gate_40_data['total_users']:,}")

with col2:
    st.metric("Avg Game Rounds (Gate 30)", f"{gate_30_data['avg_gamerounds']}")
    delta_rounds = round(gate_40_data['avg_gamerounds'] - gate_30_data['avg_gamerounds'], 2)
    st.metric("Avg Game Rounds (Gate 40)", f"{gate_40_data['avg_gamerounds']}", f"{delta_rounds} rounds")

with col3:
    st.metric("Day 1 Retention (Gate 30)", f"{gate_30_data['day_1_retention_pct']}%")
    delta_d1 = round(gate_40_data['day_1_retention_pct'] - gate_30_data['day_1_retention_pct'], 2)
    st.metric("Day 1 Retention (Gate 40)", f"{gate_40_data['day_1_retention_pct']}%", f"{delta_d1}%")

with col4:
    st.metric("Day 7 Retention (Gate 30)", f"{gate_30_data['day_7_retention_pct']}%")
    delta_d7 = round(gate_40_data['day_7_retention_pct'] - gate_30_data['day_7_retention_pct'], 2)
    st.metric("Day 7 Retention (Gate 40)", f"{gate_40_data['day_7_retention_pct']}%", f"{delta_d7}%")

st.markdown("---")

# Visualizations
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Retention Rate Comparison")
    # Melt dataframe for easy plotting
    df_melt = pd.melt(df_agg, id_vars=['version'], value_vars=['day_1_retention_pct', 'day_7_retention_pct'], 
                      var_name='Retention_Type', value_name='Percentage')
    df_melt['Retention_Type'] = df_melt['Retention_Type'].map({'day_1_retention_pct': 'Day 1', 'day_7_retention_pct': 'Day 7'})
    
    fig_retention = px.bar(df_melt, x='Retention_Type', y='Percentage', color='version', barmode='group',
                           text='Percentage', title='Day 1 vs Day 7 Retention',
                           labels={'Percentage': 'Retention Rate (%)', 'Retention_Type': 'Metric'})
    fig_retention.update_traces(textposition='outside')
    st.plotly_chart(fig_retention, use_container_width=True)

with col_chart2:
    st.subheader("User Engagement: Game Rounds Played")
    st.markdown("*(Showing players with ≤ 200 rounds to improve readability)*")
    
    fig_dist = px.histogram(df_raw, x='sum_gamerounds', color='version', barmode='overlay', 
                            nbins=40, opacity=0.7, title='Distribution of Game Rounds Played',
                            labels={'sum_gamerounds': 'Total Game Rounds Played'})
    st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("---")
st.subheader("💡 Product Recommendation")
st.info("""
**Do NOT move the gate to level 40.**

Although players in the `gate_40` group initially play slightly more rounds, we observe a **statistically significant drop in Day-7 retention**. 
Forcing players to take a break at level 30 acts as 'delayed gratification', which increases the likelihood of them returning to the game long-term.
""")
