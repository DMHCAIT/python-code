import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime

def create_html_dashboard():
    """Create an HTML dashboard with interactive charts"""
    
    # Load data - use relative paths and support multiple input CSVs
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
    
    # Convert DateTime to datetime object
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Date'] = df['DateTime'].dt.date
    df['Time'] = df['DateTime'].dt.time
    df['Hour'] = df['DateTime'].dt.hour
    df['DayOfWeek'] = df['DateTime'].dt.day_name()
    
    # Load work hours data
    try:
        work_hours_file = os.path.join(current_dir, 'employee_work_hours.csv')
        work_hours_df = pd.read_csv(work_hours_file)
    except:
        work_hours_df = None
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Daily Activity', 'Top 15 Active Employees', 
                       'Hourly Pattern', 'Day of Week Activity',
                       'Work Hours Distribution', 'Average Work Hours by Employee'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Chart 1: Daily Activity
    daily_stats = df.groupby(['Date', 'Status']).size().reset_index(name='Count')
    duty_on_daily = daily_stats[daily_stats['Status'] == 'DutyOn']
    duty_off_daily = daily_stats[daily_stats['Status'] == 'DutyOff']
    
    fig.add_trace(
        go.Bar(x=duty_on_daily['Date'], y=duty_on_daily['Count'], 
               name='Duty On', marker_color='#2E8B57'),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=duty_off_daily['Date'], y=duty_off_daily['Count'], 
               name='Duty Off', marker_color='#DC143C'),
        row=1, col=1
    )
    
    # Chart 2: Employee Activity
    employee_stats = df['Name'].value_counts().head(15)
    fig.add_trace(
        go.Bar(x=employee_stats.values, y=employee_stats.index, 
               orientation='h', name='Total Records', marker_color='#4169E1'),
        row=1, col=2
    )
    
    # Chart 3: Hourly Pattern
    hourly_stats = df.groupby(['Hour', 'Status']).size().reset_index(name='Count')
    hourly_on = hourly_stats[hourly_stats['Status'] == 'DutyOn']
    hourly_off = hourly_stats[hourly_stats['Status'] == 'DutyOff']
    
    fig.add_trace(
        go.Scatter(x=hourly_on['Hour'], y=hourly_on['Count'], 
                  mode='lines+markers', name='Duty On (Hourly)', line_color='#2E8B57'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=hourly_off['Hour'], y=hourly_off['Count'], 
                  mode='lines+markers', name='Duty Off (Hourly)', line_color='#DC143C'),
        row=2, col=1
    )
    
    # Chart 4: Day of Week
    dow_stats = df.groupby(['DayOfWeek', 'Status']).size().reset_index(name='Count')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_stats['DayOfWeek'] = pd.Categorical(dow_stats['DayOfWeek'], categories=day_order, ordered=True)
    dow_stats = dow_stats.sort_values('DayOfWeek')
    
    dow_on = dow_stats[dow_stats['Status'] == 'DutyOn']
    dow_off = dow_stats[dow_stats['Status'] == 'DutyOff']
    
    fig.add_trace(
        go.Bar(x=dow_on['DayOfWeek'], y=dow_on['Count'], 
               name='Duty On (DoW)', marker_color='#2E8B57'),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(x=dow_off['DayOfWeek'], y=dow_off['Count'], 
               name='Duty Off (DoW)', marker_color='#DC143C'),
        row=2, col=2
    )
    
    # Charts 5 & 6: Work Hours Analysis (if available)
    if work_hours_df is not None:
        # Work Hours Distribution
        fig.add_trace(
            go.Histogram(x=work_hours_df['Work_Hours'], name='Work Hours Distribution', 
                        marker_color='#FF6347'),
            row=3, col=1
        )
        
        # Average Work Hours by Employee
        avg_hours = work_hours_df.groupby('Name')['Work_Hours'].mean().sort_values(ascending=False).head(15)
        fig.add_trace(
            go.Bar(x=avg_hours.values, y=avg_hours.index, 
                   orientation='h', name='Avg Work Hours', marker_color='#32CD32'),
            row=3, col=2
        )
    
    # Update layout
    fig.update_layout(
        height=1200,
        title_text="Duty Schedule Dashboard",
        title_x=0.5,
        title_font_size=24,
        showlegend=True
    )
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Duty Schedule Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
            }}
            .metrics {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
                flex-wrap: wrap;
            }}
            .metric-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                margin: 10px;
                min-width: 150px;
            }}
            .metric-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }}
            .metric-label {{
                color: #666;
                margin-top: 5px;
            }}
            .chart-container {{
                background: white;
                margin: 20px 0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .summary-table {{
                background: white;
                margin: 20px 0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Duty Schedule Dashboard</h1>
            <p>Interactive Analysis of Employee Duty Records</p>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-label">Total Records</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{df['Name'].nunique()}</div>
                <div class="metric-label">Unique Employees</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(df[df['Status'] == 'DutyOn']):,}</div>
                <div class="metric-label">Duty On Records</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(df[df['Status'] == 'DutyOff']):,}</div>
                <div class="metric-label">Duty Off Records</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{(df['Date'].max() - df['Date'].min()).days + 1}</div>
                <div class="metric-label">Days Tracked</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div id="main-charts"></div>
        </div>
        
        <div class="summary-table">
            <h3>📋 Employee Summary</h3>
            <table>
                <tr>
                    <th>Employee</th>
                    <th>Total Records</th>
                    <th>Duty On</th>
                    <th>Duty Off</th>
                    <th>Unique Days</th>
                </tr>
    """
    
    # Add employee summary table
    employee_summary = df.groupby('Name').agg({
        'Status': 'count',
        'Date': 'nunique'
    }).reset_index()
    
    duty_on_counts = df[df['Status'] == 'DutyOn'].groupby('Name').size()
    duty_off_counts = df[df['Status'] == 'DutyOff'].groupby('Name').size()
    
    for _, row in employee_summary.iterrows():
        name = row['Name']
        total = row['Status']
        days = row['Date']
        duty_on = duty_on_counts.get(name, 0)
        duty_off = duty_off_counts.get(name, 0)
        
        html_content += f"""
                <tr>
                    <td>{name}</td>
                    <td>{total}</td>
                    <td>{duty_on}</td>
                    <td>{duty_off}</td>
                    <td>{days}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <script>
    """
    
    # Add the plotly chart
    html_content += f"var fig = {fig.to_json()};"
    html_content += """
            Plotly.newPlot('main-charts', fig.data, fig.layout);
        </script>
    </body>
    </html>
    """
    
    # Save HTML file
    output_file = os.path.join(current_dir, 'duty_dashboard.html')
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print("✅ HTML Dashboard created: duty_dashboard.html")
    print("✅ Interactive charts and metrics included")
    print("✅ Employee summary table added")

if __name__ == "__main__":
    create_html_dashboard()