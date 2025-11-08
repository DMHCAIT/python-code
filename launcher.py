#!/usr/bin/env python3
"""
Dashboard Launcher for Duty Schedule Analysis
This script provides easy access to both dashboard options
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("🚀 Duty Schedule Dashboard Launcher")
    print("=" * 50)
    print()
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    print("Available Dashboard Options:")
    print("1. 🌐 Interactive Streamlit Dashboard (Web-based, Real-time)")
    print("2. � Employee Lookup Tool (Select name → View schedule)")
    print("3. �📄 Static HTML Dashboard (File-based, Quick view)")
    print("4. 🔧 Generate New HTML Dashboard")
    print("5. 📊 Run Data Analysis Again")
    print("6. ❌ Exit")
    print()
    
    while True:
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            print("\n🌐 Starting Streamlit Dashboard...")
            print("📍 This will open in your web browser at http://localhost:8501")
            print("⚠️  Keep this terminal open while using the dashboard")
            print("🛑 Press Ctrl+C to stop the dashboard")
            print()
            
            # Change to the correct directory and run streamlit
            os.chdir(current_dir)
            python_path = current_dir / ".venv" / "bin" / "python"
            
            try:
                subprocess.run([str(python_path), "-m", "streamlit", "run", "dashboard.py", "--server.port", "8501"])
            except KeyboardInterrupt:
                print("\n🛑 Dashboard stopped by user")
            break
            
        elif choice == "2":
            print("\n👤 Starting Employee Lookup Tool...")
            print("📍 This will open in your web browser at http://localhost:8502")
            print("⚠️  Keep this terminal open while using the tool")
            print("� Press Ctrl+C to stop the tool")
            print()
            
            # Change to the correct directory and run streamlit
            os.chdir(current_dir)
            python_path = current_dir / ".venv" / "bin" / "python"
            
            try:
                subprocess.run([str(python_path), "-m", "streamlit", "run", "employee_lookup.py", "--server.port", "8502"])
            except KeyboardInterrupt:
                print("\n🛑 Employee Lookup Tool stopped by user")
            break
            
        elif choice == "3":
            print("\n�📄 Opening HTML Dashboard...")
            html_file = current_dir / "duty_dashboard.html"
            
            if html_file.exists():
                # Open in default browser
                webbrowser.open(f"file://{html_file.absolute()}")
                print(f"✅ HTML Dashboard opened: {html_file}")
            else:
                print("❌ HTML Dashboard not found. Please generate it first (option 4)")
            break
            
        elif choice == "4":
            print("\n🔧 Generating new HTML Dashboard...")
            os.chdir(current_dir)
            python_path = current_dir / ".venv" / "bin" / "python"
            
            try:
                result = subprocess.run([str(python_path), "create_html_dashboard.py"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                    print("✅ HTML Dashboard generated successfully!")
                    
                    # Ask if user wants to open it
                    open_choice = input("Would you like to open it now? (y/n): ").strip().lower()
                    if open_choice == 'y':
                        html_file = current_dir / "duty_dashboard.html"
                        webbrowser.open(f"file://{html_file.absolute()}")
                        print(f"✅ HTML Dashboard opened: {html_file}")
                else:
                    print("❌ Error generating dashboard:")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error: {e}")
            break
            
        elif choice == "5":
            print("\n📊 Running data analysis...")
            os.chdir(current_dir)
            python_path = current_dir / ".venv" / "bin" / "python"
            
            try:
                result = subprocess.run([str(python_path), "duty_analyzer.py"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                    print("✅ Data analysis completed successfully!")
                else:
                    print("❌ Error in analysis:")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error: {e}")
            break
            
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-6.")
            continue

if __name__ == "__main__":
    main()