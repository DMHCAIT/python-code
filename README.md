# 📊 Duty Schedule Dashboard

A comprehensive Python-based dashboard system for analyzing employee duty schedules with interactive visualizations and detailed reporting.

## 🚀 Quick Start

Run the launcher to access all dashboard options:
```bash
python launcher.py
```

## 📁 Project Structure

```
PYTHON CODE/
├── 📊 DASHBOARDS
│   ├── dashboard.py              # Interactive Streamlit dashboard
│   ├── duty_dashboard.html       # Static HTML dashboard
│   └── create_html_dashboard.py  # HTML dashboard generator
├── 📈 ANALYSIS
│   ├── duty_analyzer.py          # Main data analysis script
│   └── launcher.py               # Dashboard launcher utility
├── 📄 DATA FILES
│   ├── Untitled spreadsheet - Sheet3.csv  # Original data
│   ├── duty_schedule_by_person.csv        # Person-wise analysis
│   ├── duty_schedule_by_date.csv          # Date-wise analysis
│   ├── daily_duty_summary.csv             # Daily statistics
│   └── employee_work_hours.csv            # Work hours calculation
└── 🔧 ENVIRONMENT
    └── .venv/                     # Python virtual environment
```

## 🎯 Features

### 📊 Interactive Streamlit Dashboard
- **Real-time filtering** by date range, employees, and status
- **Key metrics** display with live updates
- **Interactive charts** including:
  - Daily duty activity trends
  - Employee activity distribution
  - Hourly activity patterns
  - Day-of-week analysis
  - Work hours distribution
- **Data export** capabilities
- **Multi-tab interface** for detailed data exploration

### 📄 HTML Dashboard
- **Static visualization** for quick sharing
- **Interactive Plotly charts**
- **Employee summary tables**
- **Key performance indicators**
- **Professional styling** with responsive design

### 📈 Data Analysis Engine
- **Automated data processing** from CSV input
- **Work hours calculation** (duty on to duty off)
- **Multiple output formats** (CSV reports)
- **Statistical summaries** and insights

## 🔍 Available Visualizations

1. **📅 Daily Activity Trends**
   - Bar charts showing duty on/off patterns by date
   - Trend analysis across time periods

2. **👥 Employee Performance**
   - Activity distribution by employee
   - Individual work hour analysis
   - Attendance patterns

3. **🕐 Time Analysis**
   - Hourly activity patterns
   - Peak duty hours identification
   - Day-of-week trends

4. **📊 Statistical Insights**
   - Average work hours per employee
   - Work hours distribution
   - Attendance consistency metrics

## 🛠️ Installation & Setup

1. **Install Python Dependencies**:
   ```bash
   pip install pandas streamlit plotly matplotlib seaborn
   ```

2. **Prepare Your Data**:
   - Place your CSV file in the project directory
   - Ensure CSV format: `ID,Name,Status,DateTime`
   - Status should be either 'DutyOn' or 'DutyOff'

3. **Run Analysis**:
   ```bash
   python duty_analyzer.py
   ```

4. **Launch Dashboards**:
   ```bash
   python launcher.py
   ```

## 📋 Data Format

Your CSV file should contain these columns:
- **ID**: Employee identifier
- **Name**: Employee name
- **Status**: 'DutyOn' or 'DutyOff'
- **DateTime**: Timestamp in format 'YYYY-MM-DD HH:MM:SS'

Example:
```csv
9218,shilpi,DutyOn,2025-10-09 09:36:14
9218,shilpi,DutyOff,2025-10-09 19:07:23
```

## 🎨 Dashboard Options

### Option 1: Streamlit Dashboard (Recommended)
- **URL**: http://localhost:8501
- **Features**: Interactive filters, real-time updates, data export
- **Best for**: Detailed analysis, data exploration

### Option 2: HTML Dashboard
- **File**: duty_dashboard.html
- **Features**: Static charts, summary tables, easy sharing
- **Best for**: Quick reports, presentations, sharing

## 📊 Key Metrics Displayed

- **Total Records**: Count of all duty entries
- **Unique Employees**: Number of different employees
- **Duty On/Off Counts**: Breakdown by status type
- **Date Range**: Analysis period coverage
- **Average Work Hours**: Mean daily work duration
- **Work Hours Distribution**: Statistical analysis of work patterns

## 🔧 Customization

### Adding New Charts
Edit `dashboard.py` to add new visualizations:
```python
# Example: Add new chart
fig = px.scatter(data, x='Date', y='Hours', color='Employee')
st.plotly_chart(fig, use_container_width=True)
```

### Modifying Filters
Update the sidebar filters in `dashboard.py`:
```python
# Example: Add department filter
departments = st.sidebar.multiselect("Select Departments", df['Department'].unique())
```

### Changing Color Schemes
Modify color mappings in chart definitions:
```python
color_discrete_map={'DutyOn': '#your_color', 'DutyOff': '#your_color'}
```

## 📁 Output Files

The system generates several CSV reports:

1. **duty_schedule_by_person.csv**: Employee-focused view
2. **duty_schedule_by_date.csv**: Date-focused view  
3. **daily_duty_summary.csv**: Aggregated daily statistics
4. **employee_work_hours.csv**: Work duration calculations

## 🔍 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing packages with pip
2. **File not found**: Ensure CSV file path is correct
3. **Date parsing errors**: Check DateTime format in CSV
4. **Dashboard not loading**: Verify Streamlit installation

### Performance Tips

- **Large datasets**: Use date range filters to improve performance
- **Memory usage**: Close unused browser tabs
- **Slow loading**: Consider data sampling for very large files

## 🆕 Recent Updates

- ✅ Added interactive Streamlit dashboard
- ✅ Created HTML dashboard with Plotly charts
- ✅ Implemented work hours calculation
- ✅ Added employee and date filtering
- ✅ Created launcher utility for easy access

## 📞 Support

For issues or feature requests:
1. Check the troubleshooting section
2. Verify data format compliance
3. Review terminal output for error messages

## 🏆 Best Practices

1. **Data Quality**: Ensure consistent date/time formats
2. **Regular Updates**: Re-run analysis when new data is added
3. **Backup**: Keep original data files safe
4. **Performance**: Use filters for large datasets
5. **Sharing**: Use HTML dashboard for presentations

---

*Generated on: November 8, 2025*  
*Dashboard System Version: 1.0*