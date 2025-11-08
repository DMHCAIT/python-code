import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Duty Schedule Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the duty schedule data"""
    try:
        # Load the original CSV file - use relative path
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(current_dir, 'Untitled spreadsheet - Sheet3.csv')
        df = pd.read_csv(csv_file, names=['ID', 'Name', 'Status', 'DateTime'])
        
        # Convert DateTime to datetime object
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Date'] = df['DateTime'].dt.date
        df['Time'] = df['DateTime'].dt.time
        df['Hour'] = df['DateTime'].dt.hour
        df['DayOfWeek'] = df['DateTime'].dt.day_name()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_work_hours():
    """Load the work hours data"""
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        work_hours_file = os.path.join(current_dir, 'employee_work_hours.csv')
        return pd.read_csv(work_hours_file)
    except Exception as e:
        st.error(f"Error loading work hours data: {e}")
        return None

def main():
    st.title("📊 Duty Schedule Dashboard")
    st.markdown("---")
    
    # Load data
    df = load_data()
    work_hours_df = load_work_hours()
    
    if df is None:
        st.error("Failed to load data. Please check if the CSV file exists.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Employee filter
    all_employees = ['All'] + sorted(df['Name'].unique().tolist())
    selected_employees = st.sidebar.multiselect(
        "Select Employees",
        options=all_employees,
        default=['All']
    )
    
    # Status filter
    status_filter = st.sidebar.selectbox(
        "Filter by Status",
        options=['All', 'DutyOn', 'DutyOff']
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'] >= start_date) & 
            (filtered_df['Date'] <= end_date)
        ]
    
    # Employee filter
    if 'All' not in selected_employees and selected_employees:
        filtered_df = filtered_df[filtered_df['Name'].isin(selected_employees)]
    
    # Status filter
    if status_filter != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    # Key Metrics Row
    st.header("📈 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_records = len(filtered_df)
        st.metric("Total Records", f"{total_records:,}")
    
    with col2:
        unique_employees = filtered_df['Name'].nunique()
        st.metric("Unique Employees", unique_employees)
    
    with col3:
        duty_on_count = len(filtered_df[filtered_df['Status'] == 'DutyOn'])
        st.metric("Duty On Records", f"{duty_on_count:,}")
    
    with col4:
        duty_off_count = len(filtered_df[filtered_df['Status'] == 'DutyOff'])
        st.metric("Duty Off Records", f"{duty_off_count:,}")
    
    with col5:
        date_range_days = (filtered_df['Date'].max() - filtered_df['Date'].min()).days + 1
        st.metric("Date Range (Days)", date_range_days)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Daily Duty Activity")
        daily_stats = filtered_df.groupby(['Date', 'Status']).size().reset_index(name='Count')
        
        fig = px.bar(daily_stats, 
                    x='Date', 
                    y='Count', 
                    color='Status',
                    title="Daily Duty On/Off Activity",
                    color_discrete_map={'DutyOn': '#2E8B57', 'DutyOff': '#DC143C'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.subheader("👥 Employee Activity Distribution")
        employee_stats = filtered_df['Name'].value_counts().head(15)
        
        fig = px.bar(x=employee_stats.values, 
                    y=employee_stats.index,
                    orientation='h',
                    title="Top 15 Most Active Employees",
                    labels={'x': 'Total Records', 'y': 'Employee'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🕐 Hourly Activity Pattern")
        hourly_stats = filtered_df.groupby(['Hour', 'Status']).size().reset_index(name='Count')
        
        fig = px.line(hourly_stats, 
                     x='Hour', 
                     y='Count', 
                     color='Status',
                     title="Hourly Activity Pattern",
                     markers=True,
                     color_discrete_map={'DutyOn': '#2E8B57', 'DutyOff': '#DC143C'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.subheader("📆 Day of Week Analysis")
        dow_stats = filtered_df.groupby(['DayOfWeek', 'Status']).size().reset_index(name='Count')
        
        # Order days properly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_stats['DayOfWeek'] = pd.Categorical(dow_stats['DayOfWeek'], categories=day_order, ordered=True)
        dow_stats = dow_stats.sort_values('DayOfWeek')
        
        fig = px.bar(dow_stats, 
                    x='DayOfWeek', 
                    y='Count', 
                    color='Status',
                    title="Activity by Day of Week",
                    color_discrete_map={'DutyOn': '#2E8B57', 'DutyOff': '#DC143C'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    # Work Hours Analysis (if available)
    if work_hours_df is not None:
        st.markdown("---")
        st.header("⏰ Work Hours Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Average Work Hours by Employee")
            avg_hours = work_hours_df.groupby('Name')['Work_Hours'].mean().sort_values(ascending=False).head(15)
            
            fig = px.bar(x=avg_hours.values,
                        y=avg_hours.index,
                        orientation='h',
                        title="Top 15 Employees by Average Work Hours",
                        labels={'x': 'Average Hours', 'y': 'Employee'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            st.subheader("📈 Work Hours Distribution")
            
            fig = px.histogram(work_hours_df, 
                             x='Work_Hours',
                             nbins=20,
                             title="Distribution of Daily Work Hours")
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        # Work hours statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_work_hours = work_hours_df['Work_Hours'].mean()
            st.metric("Average Work Hours", f"{avg_work_hours:.2f}")
        
        with col2:
            min_work_hours = work_hours_df['Work_Hours'].min()
            st.metric("Minimum Work Hours", f"{min_work_hours:.2f}")
        
        with col3:
            max_work_hours = work_hours_df['Work_Hours'].max()
            st.metric("Maximum Work Hours", f"{max_work_hours:.2f}")
        
        with col4:
            std_work_hours = work_hours_df['Work_Hours'].std()
            st.metric("Std Deviation", f"{std_work_hours:.2f}")
    
    # Individual Employee Analysis
    st.markdown("---")
    st.header("👤 Individual Employee Analysis")
    
    # Employee selector
    selected_employee = st.selectbox(
        "🔍 Select an Employee to View Detailed Schedule:",
        options=['Select an employee...'] + sorted(filtered_df['Name'].unique().tolist()),
        key="employee_selector"
    )
    
    if selected_employee != 'Select an employee...':
        employee_data = filtered_df[filtered_df['Name'] == selected_employee].copy()
        
        if not employee_data.empty:
            # Employee metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_records = len(employee_data)
                st.metric("Total Records", total_records)
            
            with col2:
                unique_days = employee_data['Date'].nunique()
                st.metric("Days Worked", unique_days)
            
            with col3:
                duty_on_count = len(employee_data[employee_data['Status'] == 'DutyOn'])
                st.metric("Duty On Records", duty_on_count)
            
            with col4:
                duty_off_count = len(employee_data[employee_data['Status'] == 'DutyOff'])
                st.metric("Duty Off Records", duty_off_count)
            
            # Create detailed schedule table
            st.subheader(f"📅 Detailed Schedule for {selected_employee}")
            
            # Group by date and create a comprehensive view
            schedule_data = []
            for date in sorted(employee_data['Date'].unique()):
                date_records = employee_data[employee_data['Date'] == date].sort_values('DateTime')
                
                duty_on_records = date_records[date_records['Status'] == 'DutyOn']
                duty_off_records = date_records[date_records['Status'] == 'DutyOff']
                
                # Get duty on times
                duty_on_times = duty_on_records['Time'].tolist() if not duty_on_records.empty else ['N/A']
                duty_off_times = duty_off_records['Time'].tolist() if not duty_off_records.empty else ['N/A']
                
                # Calculate work duration if both exist
                work_duration = "N/A"
                if not duty_on_records.empty and not duty_off_records.empty:
                    first_on = duty_on_records.iloc[0]['DateTime']
                    last_off = duty_off_records.iloc[-1]['DateTime']
                    duration = last_off - first_on
                    hours = duration.total_seconds() / 3600
                    work_duration = f"{hours:.2f} hours"
                
                schedule_data.append({
                    'Date': date,
                    'Name': selected_employee,
                    'Duty On': ', '.join([str(t) for t in duty_on_times]),
                    'Duty Off': ', '.join([str(t) for t in duty_off_times]),
                    'Work Duration': work_duration,
                    'Total Records': len(date_records)
                })
            
            # Display as DataFrame
            schedule_df = pd.DataFrame(schedule_data)
            st.dataframe(schedule_df, width='stretch')
            
            # Download button for individual employee data
            csv = schedule_df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {selected_employee}'s Schedule",
                data=csv,
                file_name=f"{selected_employee}_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Employee-specific charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Daily Activity Pattern")
                daily_activity = employee_data.groupby(['Date', 'Status']).size().reset_index(name='Count')
                
                fig = px.bar(daily_activity, 
                            x='Date', 
                            y='Count', 
                            color='Status',
                            title=f"Daily Activity for {selected_employee}",
                            color_discrete_map={'DutyOn': '#2E8B57', 'DutyOff': '#DC143C'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                st.subheader("🕐 Hourly Activity Pattern")
                hourly_activity = employee_data.groupby(['Hour', 'Status']).size().reset_index(name='Count')
                
                fig = px.line(hourly_activity, 
                             x='Hour', 
                             y='Count', 
                             color='Status',
                             title=f"Hourly Pattern for {selected_employee}",
                             markers=True,
                             color_discrete_map={'DutyOn': '#2E8B57', 'DutyOff': '#DC143C'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, width='stretch')
            
            # Work hours trend (if work hours data available)
            if work_hours_df is not None:
                employee_work_hours = work_hours_df[work_hours_df['Name'] == selected_employee]
                if not employee_work_hours.empty:
                    st.subheader("⏰ Work Hours Trend")
                    
                    fig = px.line(employee_work_hours, 
                                 x='Date', 
                                 y='Work_Hours',
                                 title=f"Work Hours Trend for {selected_employee}",
                                 markers=True)
                    fig.add_hline(y=employee_work_hours['Work_Hours'].mean(), 
                                 line_dash="dash", 
                                 line_color="red",
                                 annotation_text=f"Average: {employee_work_hours['Work_Hours'].mean():.2f} hours")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, width="stretch")
        else:
            st.warning(f"No data found for {selected_employee} in the selected date range.")
    
    # Detailed Data Tables
    st.markdown("---")
    st.header("📋 Detailed Data")
    
    tab1, tab2, tab3 = st.tabs(["Raw Data", "Daily Summary", "Employee Summary"])
    
    with tab1:
        st.subheader("Filtered Raw Data")
        st.dataframe(filtered_df, width="stretch")
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"duty_schedule_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Daily Summary")
        daily_summary = filtered_df.groupby('Date').agg({
            'Name': 'nunique',
            'Status': ['count']
        }).round(2)
        daily_summary.columns = ['Unique_Employees', 'Total_Records']
        daily_summary = daily_summary.reset_index()
        
        # Add duty on/off counts
        duty_on_daily = filtered_df[filtered_df['Status'] == 'DutyOn'].groupby('Date').size()
        duty_off_daily = filtered_df[filtered_df['Status'] == 'DutyOff'].groupby('Date').size()
        
        daily_summary['Duty_On_Count'] = daily_summary['Date'].map(duty_on_daily).fillna(0).astype(int)
        daily_summary['Duty_Off_Count'] = daily_summary['Date'].map(duty_off_daily).fillna(0).astype(int)
        
        st.dataframe(daily_summary, width="stretch")
    
    with tab3:
        st.subheader("Employee Summary")
        employee_summary = filtered_df.groupby('Name').agg({
            'Date': 'nunique',
            'Status': 'count',
            'DateTime': ['min', 'max']
        }).round(2)
        employee_summary.columns = ['Unique_Days', 'Total_Records', 'First_Activity', 'Last_Activity']
        employee_summary = employee_summary.reset_index()
        
        # Add duty on/off counts
        duty_on_emp = filtered_df[filtered_df['Status'] == 'DutyOn'].groupby('Name').size()
        duty_off_emp = filtered_df[filtered_df['Status'] == 'DutyOff'].groupby('Name').size()
        
        employee_summary['Duty_On_Count'] = employee_summary['Name'].map(duty_on_emp).fillna(0).astype(int)
        employee_summary['Duty_Off_Count'] = employee_summary['Name'].map(duty_off_emp).fillna(0).astype(int)
        
        st.dataframe(employee_summary, width="stretch")

if __name__ == "__main__":
    main()