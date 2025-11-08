import pandas as pd
from datetime import datetime
import os

def analyze_duty_schedule(csv_file_path):
    """
    Analyze duty schedule from CSV file and organize by date and person
    """
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv(csv_file_path, names=['ID', 'Name', 'Status', 'DateTime'])
    
    # Convert DateTime to datetime object
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Date'] = df['DateTime'].dt.date
    df['Time'] = df['DateTime'].dt.time
    
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Unique employees: {df['Name'].nunique()}")
    
    # Sort by Name, Date, and DateTime
    df_sorted = df.sort_values(['Name', 'Date', 'DateTime'])
    
    # Create a summary by person and date
    print("\n" + "="*80)
    print("DUTY SCHEDULE ANALYSIS - BY PERSON AND DATE")
    print("="*80)
    
    # Group by person
    for name in sorted(df['Name'].unique()):
        person_data = df_sorted[df_sorted['Name'] == name]
        print(f"\n📋 Employee: {name.upper()}")
        print("-" * 50)
        
        # Group by date for this person
        for date in sorted(person_data['Date'].unique()):
            date_data = person_data[person_data['Date'] == date]
            print(f"\n📅 Date: {date}")
            
            duty_on_records = date_data[date_data['Status'] == 'DutyOn']
            duty_off_records = date_data[date_data['Status'] == 'DutyOff']
            
            if not duty_on_records.empty:
                for _, record in duty_on_records.iterrows():
                    print(f"  🟢 Duty ON:  {record['Time']}")
            
            if not duty_off_records.empty:
                for _, record in duty_off_records.iterrows():
                    print(f"  🔴 Duty OFF: {record['Time']}")
            
            # Calculate duty duration if both on and off exist
            if not duty_on_records.empty and not duty_off_records.empty:
                # Get the first duty on and last duty off of the day
                first_on = duty_on_records.iloc[0]['DateTime']
                last_off = duty_off_records.iloc[-1]['DateTime']
                duration = last_off - first_on
                hours = duration.total_seconds() / 3600
                print(f"  ⏱️  Total duty time: {hours:.2f} hours")
    
    # Create a date-wise summary
    print("\n\n" + "="*80)
    print("DUTY SCHEDULE ANALYSIS - BY DATE")
    print("="*80)
    
    for date in sorted(df['Date'].unique()):
        date_data = df_sorted[df_sorted['Date'] == date]
        print(f"\n📅 Date: {date}")
        print("-" * 50)
        
        duty_on_data = date_data[date_data['Status'] == 'DutyOn'].sort_values('DateTime')
        duty_off_data = date_data[date_data['Status'] == 'DutyOff'].sort_values('DateTime')
        
        print("\n🟢 DUTY ON:")
        for _, record in duty_on_data.iterrows():
            print(f"  {record['Time']} - {record['Name']}")
        
        print("\n🔴 DUTY OFF:")
        for _, record in duty_off_data.iterrows():
            print(f"  {record['Time']} - {record['Name']}")
        
        print(f"\n📊 Summary for {date}:")
        print(f"  Total employees on duty: {len(duty_on_data)}")
        print(f"  Total employees off duty: {len(duty_off_data)}")
    
    # Create CSV reports
    create_csv_reports(df_sorted)

def create_csv_reports(df):
    """
    Create separate CSV files for different views of the data
    """
    print("\n" + "="*80)
    print("CREATING CSV REPORTS")
    print("="*80)
    
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Person-wise duty schedule
    person_schedule = []
    for name in sorted(df['Name'].unique()):
        person_data = df[df['Name'] == name].sort_values('DateTime')
        for _, record in person_data.iterrows():
            person_schedule.append({
                'Name': record['Name'],
                'Date': record['Date'],
                'Status': record['Status'],
                'Time': record['Time'],
                'DateTime': record['DateTime']
            })
    
    person_df = pd.DataFrame(person_schedule)
    person_file = os.path.join(current_dir, 'duty_schedule_by_person.csv')
    person_df.to_csv(person_file, index=False)
    print("✅ Created: duty_schedule_by_person.csv")
    
    # 2. Date-wise duty schedule
    date_schedule = []
    for date in sorted(df['Date'].unique()):
        date_data = df[df['Date'] == date].sort_values('DateTime')
        for _, record in date_data.iterrows():
            date_schedule.append({
                'Date': record['Date'],
                'Name': record['Name'],
                'Status': record['Status'],
                'Time': record['Time'],
                'DateTime': record['DateTime']
            })
    
    date_df = pd.DataFrame(date_schedule)
    date_file = os.path.join(current_dir, 'duty_schedule_by_date.csv')
    date_df.to_csv(date_file, index=False)
    print("✅ Created: duty_schedule_by_date.csv")
    
    # 3. Daily summary
    daily_summary = []
    for date in sorted(df['Date'].unique()):
        date_data = df[df['Date'] == date]
        duty_on_count = len(date_data[date_data['Status'] == 'DutyOn'])
        duty_off_count = len(date_data[date_data['Status'] == 'DutyOff'])
        unique_employees = date_data['Name'].nunique()
        
        daily_summary.append({
            'Date': date,
            'Total_DutyOn': duty_on_count,
            'Total_DutyOff': duty_off_count,
            'Unique_Employees': unique_employees
        })
    
    summary_df = pd.DataFrame(daily_summary)
    summary_file = os.path.join(current_dir, 'daily_duty_summary.csv')
    summary_df.to_csv(summary_file, index=False)
    print("✅ Created: daily_duty_summary.csv")
    
    # 4. Employee work hours (approximate)
    work_hours = []
    for name in sorted(df['Name'].unique()):
        person_data = df[df['Name'] == name].sort_values('DateTime')
        for date in sorted(person_data['Date'].unique()):
            date_data = person_data[person_data['Date'] == date]
            duty_on = date_data[date_data['Status'] == 'DutyOn']
            duty_off = date_data[date_data['Status'] == 'DutyOff']
            
            if not duty_on.empty and not duty_off.empty:
                first_on = duty_on.iloc[0]['DateTime']
                last_off = duty_off.iloc[-1]['DateTime']
                duration = last_off - first_on
                hours = duration.total_seconds() / 3600
                
                work_hours.append({
                    'Name': name,
                    'Date': date,
                    'Duty_On_Time': duty_on.iloc[0]['Time'],
                    'Duty_Off_Time': duty_off.iloc[-1]['Time'],
                    'Work_Hours': round(hours, 2)
                })
    
    if work_hours:
        hours_df = pd.DataFrame(work_hours)
        hours_file = os.path.join(current_dir, 'employee_work_hours.csv')
        hours_df.to_csv(hours_file, index=False)
        print("✅ Created: employee_work_hours.csv")

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, "Untitled spreadsheet - Sheet3.csv")
    
    if os.path.exists(csv_file_path):
        analyze_duty_schedule(csv_file_path)
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print("Check the created CSV files for detailed reports:")
        print("- duty_schedule_by_person.csv")
        print("- duty_schedule_by_date.csv") 
        print("- daily_duty_summary.csv")
        print("- employee_work_hours.csv")
    else:
        print(f"Error: File not found at {csv_file_path}")