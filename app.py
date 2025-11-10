
"""
Sleep Pattern Visualization Dashboard
Deploy to: Streamlit Cloud (free hosting)
"""

import streamlit as st
st.set_page_config(
    page_title="Sleep Analytics Dashboard",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
    }
    .stMetric {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        background: linear-gradient(90deg, #a78bfa 0%, #f9a8d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Generate sample sleep data
@st.cache_data
def generate_sleep_data(days):
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    np.random.seed(42)
    
    data = {
        'date': dates,
        'day': [d.strftime('%a') for d in dates],
        'duration': np.random.uniform(6, 9, days),
        'deep_sleep': np.random.uniform(1, 2.5, days),
        'rem_sleep': np.random.uniform(1.5, 2.5, days),
        'light_sleep': np.random.uniform(3, 5, days),
        'awake': np.random.uniform(0.2, 0.7, days),
        'quality': np.random.uniform(60, 95, days),
        'heart_rate': np.random.uniform(55, 70, days),
        'bed_time': np.random.uniform(22, 24, days),
        'wake_time': np.random.uniform(6, 8, days)
    }
    return pd.DataFrame(data)

# Title
st.markdown("# 🌙 Sleep Analytics Dashboard")
st.markdown("### Track and optimize your sleep patterns for better health")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙ Settings")
    time_range = st.selectbox(
        "Select Time Range",
        ["Week", "Month", "Quarter"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 💤 Problem Statement")
    st.markdown("""
    In the modern world, irregular lifestyles, stress, and excessive screen time have 
    significantly affected people's sleep quality. Although various devices and apps 
    collect sleep data, users often find it difficult to interpret and utilize this 
    information effectively.
    
    *This dashboard aims to:*
    - Visualize sleep patterns clearly
    - Provide meaningful insights
    - Help users improve their sleep habits
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Objectives")
    st.markdown("""
    1. *Track Key Metrics*: Duration, quality, stages
    2. *Identify Trends*: Weekly and monthly patterns
    3. *Generate Insights*: AI-powered recommendations
    4. *Optimize Sleep*: Data-driven improvements
    """)
    
    st.markdown("---")
    st.markdown("### 📋 Scope")
    st.markdown("""
    *In Scope:*
    ✅ Data visualization  
    ✅ Statistical analysis  
    ✅ Pattern recognition  
    ✅ Personalized insights  
    
    *Future Enhancements:*
    🔄 Device integration  
    🔄 ML predictions  
    🔄 Social features  
    """)

# Get data
days_map = {"Week": 7, "Month": 30, "Quarter": 90}
days = days_map[time_range]
df = generate_sleep_data(days)

# Calculate statistics
avg_duration = df['duration'].mean()
avg_quality = df['quality'].mean()
avg_deep_sleep = df['deep_sleep'].mean()
avg_heart_rate = df['heart_rate'].mean()

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⏰ Avg Sleep Duration",
        value=f"{avg_duration:.1f}h",
        delta="+0.3h"
    )

with col2:
    st.metric(
        label="⭐ Sleep Quality",
        value=f"{avg_quality:.0f}%",
        delta="+5%"
    )

with col3:
    st.metric(
        label="🧠 Deep Sleep",
        value=f"{avg_deep_sleep:.1f}h",
        delta="+0.2h"
    )

with col4:
    st.metric(
        label="❤ Resting Heart Rate",
        value=f"{avg_heart_rate:.0f} bpm",
        delta="-2 bpm"
    )

st.markdown("---")

# Main charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌙 Sleep Duration Trend")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df['date'],
        y=df['duration'],
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.3)',
        line=dict(color='rgb(139, 92, 246)', width=2),
        name='Duration',
        mode='lines'
    ))
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, title='Date'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Hours'),
        height=350,
        hovermode='x unified'
    )
    st.plotly_chart(fig1, width="stretch")

with col2:
    st.markdown("### 📊 Sleep Quality Score")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['date'],
        y=df['quality'],
        mode='lines+markers',
        line=dict(color='rgb(236, 72, 153)', width=2),
        marker=dict(size=6, color='rgb(236, 72, 153)'),
        name='Quality'
    ))
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, title='Date'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Quality %', range=[0, 100]),
        height=350,
        hovermode='x unified'
    )
    st.plotly_chart(fig2, width="stretch")

st.markdown("---")

# Bottom charts
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧠 Sleep Stages")
    stages_df = pd.DataFrame({
        'Stage': ['Deep', 'REM', 'Light', 'Awake'],
        'Hours': [
            df['deep_sleep'].mean(),
            df['rem_sleep'].mean(),
            df['light_sleep'].mean(),
            df['awake'].mean()
        ]
    })
    
    fig3 = px.bar(
        stages_df,
        y='Stage',
        x='Hours',
        orientation='h',
        color='Stage',
        color_discrete_map={
            'Deep': '#4F46E5',
            'REM': '#7C3AED',
            'Light': '#8B5CF6',
            'Awake': '#C4B5FD'
        }
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        height=300
    )
    st.plotly_chart(fig3, width="stretch")

with col2:
    st.markdown("### 📅 Weekly Pattern")
    weekly_df = df.groupby('day').agg({'duration': 'mean'}).reindex(
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    )
    
    fig4 = go.Figure()
    fig4.add_trace(go.Scatterpolar(
        r=weekly_df['duration'].values,
        theta=weekly_df.index,
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.3)',
        line=dict(color='rgb(139, 92, 246)', width=2),
        name='Duration'
    ))
    fig4.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
            angularaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig4, width="stretch")

with col3:
    st.markdown("### ☀ Sleep Schedule")
    last_week_df = df.tail(7)
    
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=last_week_df['day'],
        y=last_week_df['bed_time'],
        mode='lines+markers',
        line=dict(color='rgb(245, 158, 11)', width=2),
        marker=dict(size=8),
        name='Bed Time'
    ))
    fig5.add_trace(go.Scatter(
        x=last_week_df['day'],
        y=last_week_df['wake_time'],
        mode='lines+markers',
        line=dict(color='rgb(16, 185, 129)', width=2),
        marker=dict(size=8),
        name='Wake Time'
    ))
    fig5.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, title='Day'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Hour', range=[0, 24]),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig5, width="stretch")

st.markdown("---")

# Insights
st.markdown("### 💡 AI Insights & Recommendations")
col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    *✨ Sleep Consistency*
    
    Your sleep schedule varies by 2.3 hours across the {time_range.lower()}. 
    Try maintaining consistent bed and wake times for better quality sleep and 
    improved circadian rhythm regulation.
    """)

with col2:
    st.success(f"""
    *🎯 Deep Sleep Optimization*
    
    You're averaging {avg_deep_sleep:.1f}h of deep sleep per night. The optimal 
    range is 1.5-2h. Consider reducing screen time before bed and maintaining 
    a cool room temperature (65-68°F) to enhance deep sleep stages.
    """)

# Data table
with st.expander("📊 View Raw Data"):
    st.dataframe(
        df.style.background_gradient(cmap='viridis', subset=['quality']),
        width="stretch
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9CA3AF; padding: 20px;'>
    <p><strong>Sleep Analytics Dashboard</strong> | Track, Analyze, and Optimize Your Sleep Patterns</p>
    <p style='font-size: 0.85rem;'>💤 Better Sleep = Better Life | Data is simulated for demonstration</p>
</div>
""", unsafe_allow_html=True)
