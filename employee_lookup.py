import pandas as pd
import streamlit as st
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Employee Duty Lookup",
    page_icon="👤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .employee-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .duty-on {
        color: #28a745;
        font-weight: bold;
    }
    .duty-off {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the duty schedule data"""
    try:
        import os, glob
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pattern = os.path.join(current_dir, 'Untitled spreadsheet - Sheet*.csv')
        files = sorted(glob.glob(pattern))
        if not files:
            raise FileNotFoundError(f"No CSV files found matching: {pattern}")

        parts = []
        for csv_file in files:
            parts.append(pd.read_csv(csv_file, names=['ID', 'Name', 'Status', 'DateTime']))
        df = pd.concat(parts, ignore_index=True)
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df['Date'] = df['DateTime'].dt.date
        df['Time'] = df['DateTime'].dt.time

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def format_time_list(times):
    """Format a list of times for display"""
    if not times:
        return "No records"
    return ", ".join([str(t) for t in times])

def main():
    st.title("👤 Employee Duty Schedule Lookup")
    st.markdown("Select an employee to view their complete duty schedule")
    st.markdown("---")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Employee selection
    employees = sorted(df['Name'].unique().tolist())
    selected_employee = st.selectbox(
        "🔍 Select Employee Name:",
        options=[''] + employees,
        index=0,
        placeholder="Choose an employee..."
    )
    
    if selected_employee:
        # Filter data for selected employee
        employee_data = df[df['Name'] == selected_employee].sort_values(['Date', 'DateTime'])
        
        if not employee_data.empty:
            # Employee summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👤 Employee", selected_employee)
            with col2:
                st.metric("📅 Total Days", employee_data['Date'].nunique())
            with col3:
                st.metric("✅ Duty On", len(employee_data[employee_data['Status'] == 'DutyOn']))
            with col4:
                st.metric("❌ Duty Off", len(employee_data[employee_data['Status'] == 'DutyOff']))
            
            st.markdown("---")
            
            # Create detailed schedule
            st.subheader(f"📋 Complete Duty Schedule for **{selected_employee}**")
            
            # Group by date
            schedule_records = []
            
            for date in sorted(employee_data['Date'].unique()):
                date_data = employee_data[employee_data['Date'] == date].sort_values('DateTime')
                
                # Separate duty on and off records
                duty_on_records = date_data[date_data['Status'] == 'DutyOn']
                duty_off_records = date_data[date_data['Status'] == 'DutyOff']
                
                # Get times
                duty_on_times = duty_on_records['Time'].tolist()
                duty_off_times = duty_off_records['Time'].tolist()
                
                # Calculate work duration
                work_duration = ""
                if duty_on_times and duty_off_times:
                    first_on = duty_on_records.iloc[0]['DateTime']
                    last_off = duty_off_records.iloc[-1]['DateTime']
                    duration = last_off - first_on
                    hours = duration.total_seconds() / 3600
                    work_duration = f"{hours:.2f} hours"
                
                schedule_records.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Day': date.strftime('%A'),
                    'Name': selected_employee,
                    'Duty On': format_time_list(duty_on_times),
                    'Duty Off': format_time_list(duty_off_times),
                    'Work Duration': work_duration,
                    'Total Records': len(date_data)
                })
            
            # Display as table
            schedule_df = pd.DataFrame(schedule_records)
            
            # Style the dataframe
            def highlight_duty(val):
                if 'No records' in str(val):
                    return 'color: #6c757d; font-style: italic;'
                elif ':' in str(val):  # Time format
                    return 'font-weight: bold;'
                return ''
            
            styled_df = schedule_df.style.map(highlight_duty, subset=['Duty On', 'Duty Off'])
            
            st.dataframe(styled_df, width='stretch', hide_index=True)
            
            # Download button
            csv = schedule_df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {selected_employee}'s Complete Schedule",
                data=csv,
                file_name=f"{selected_employee}_duty_schedule_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Additional insights
            st.markdown("---")
            st.subheader("📊 Quick Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Statistics")
                total_days = employee_data['Date'].nunique()
                total_duty_on = len(employee_data[employee_data['Status'] == 'DutyOn'])
                total_duty_off = len(employee_data[employee_data['Status'] == 'DutyOff'])
                
                st.write(f"• **Total Working Days:** {total_days}")
                st.write(f"• **Total Duty On Records:** {total_duty_on}")
                st.write(f"• **Total Duty Off Records:** {total_duty_off}")
                st.write(f"• **Average Records per Day:** {(total_duty_on + total_duty_off) / total_days:.1f}")
            
            with col2:
                st.markdown("### 📅 Date Range")
                first_date = employee_data['Date'].min()
                last_date = employee_data['Date'].max()
                date_range = (last_date - first_date).days
                
                st.write(f"• **First Record:** {first_date}")
                st.write(f"• **Last Record:** {last_date}")
                st.write(f"• **Date Range:** {date_range} days")
                
                # Most common duty on hour
                if not employee_data[employee_data['Status'] == 'DutyOn'].empty:
                    common_hour = employee_data[employee_data['Status'] == 'DutyOn']['DateTime'].dt.hour.mode()
                    if len(common_hour) > 0:
                        st.write(f"• **Most Common Duty On Hour:** {common_hour.iloc[0]}:00")
            
            # Recent activity
            st.markdown("### 🕒 Recent Activity (Last 5 records)")
            recent_records = employee_data.tail(5)[['Date', 'Status', 'Time']].copy()
            recent_records['Date'] = recent_records['Date'].astype(str)
            st.dataframe(recent_records, width='stretch', hide_index=True)
            
        else:
            st.warning(f"No duty records found for employee: {selected_employee}")
    
    else:
        st.info("👆 Please select an employee name from the dropdown above to view their duty schedule")
        
        # Show available employees
        if df is not None:
            st.markdown("### 👥 Available Employees")
            employees = sorted(df['Name'].unique().tolist())
            
            # Display in columns
            cols = st.columns(3)
            for i, emp in enumerate(employees):
                with cols[i % 3]:
                    record_count = len(df[df['Name'] == emp])
                    st.write(f"• **{emp}** ({record_count} records)")

if __name__ == "__main__":
    main()