import pandas as pd
from datetime import datetime, timedelta

# Replace this sample data with your actual data
data = {
    "Position ID": ["WFS000065", "WFS000065", "WFS000065", "WFS000101", "WFS000101", "WFS000101", "WFS000127", "WFS000127", "WFS000127", "WFS000127", "WFS000127", "WFS000054", "WFS000054", "WFS000054", "WFS000065", "WFS000065"],
    "Time": ["09/12/2023 10:08 AM", "09/12/2023 02:23 PM", "09/13/2023 10:08 AM", "09/10/2023 10:15 AM", "09/10/2023 03:00 PM", "09/11/2023 10:10 AM", "09/15/2023 08:00 AM", "09/15/2023 12:00 PM", "09/16/2023 08:30 AM", "09/16/2023 12:30 PM", "09/16/2023 03:30 PM", "09/10/2023 09:00 AM", "09/11/2023 09:30 AM", "09/11/2023 02:00 PM", "09/12/2023 10:08 AM", "09/12/2023 02:23 PM"],
    "Time Out": ["09/12/2023 01:53 PM", "09/12/2023 07:02 PM", "09/13/2023 02:20 PM", "09/10/2023 02:30 PM", "09/10/2023 06:50 PM", "09/11/2023 02:30 PM", "09/15/2023 11:30 AM", "09/15/2023 03:15 PM", "09/16/2023 12:00 PM", "09/16/2023 03:00 PM", "09/16/2023 08:36 PM", "09/10/2023 01:30 PM", "09/11/2023 03:00 PM", "09/11/2023 06:00 PM", "09/12/2023 01:53 PM", "09/12/2023 07:02 PM"],
    "Employee Name": ["REsaXiaWE, XAis"] * 5 + ["Sparks, KeWWeMh"] * 6 + ["GaXCes, EXias XEpez"] * 5
}

df = pd.read_csv('Assignment_Timecard.xlsx - Sheet1.csv')

def parse_time(time_str):
    #return datetime.strptime(time_str, '%m/%d/%Y %I:%M %p')
    return pd.to_datetime(time_str,  format='%m/%d/%Y %I:%M %p')

def find_employees_consecutive_days(df, consecutive_days):
    print('\n\n Employees who have worked for consecutive seven days')
    for employee, group in df.groupby("Employee Name"):
        shifts = group["Time"].apply(parse_time)
        shifts.sort_values(inplace=True)

        for i in range(len(shifts) - consecutive_days + 1):
            if all(shifts.iloc[i + j] == shifts.iloc[i] + timedelta(days=j) for j in range(consecutive_days)):
                print(f"Employee Name: {employee}, Position ID: {group['Position ID'].iloc[0]}")
                break

def find_employees_short_breaks(df, min_hours, max_hours):
    print('\n\n Employees who have less than 10 hours of time between shifts but greater than 1 hour:')
    for employee, group in df.groupby("Employee Name"):
        shifts = group["Time"].apply(parse_time)
        shifts.sort_values(inplace=True)

        for i in range(len(shifts) - 1):
            time_between_shifts = shifts.iloc[i + 1] - shifts.iloc[i]
            if min_hours < time_between_shifts.total_seconds() / 3600 < max_hours:
                print(f"Employee Name: {employee}, Position ID: {group['Position ID'].iloc[0]}")
                break

def find_employees_long_shifts(df, min_hours):
    print( '\n\n Employees who have worked for more than 14 hours in a single shift:')
    for _, entry in df.iterrows():
        time_in = parse_time(entry["Time"])
        time_out = parse_time(entry["Time Out"])
        time_worked = time_out - time_in
        if time_worked.total_seconds() / 3600 > min_hours:
            print(f"Employee Name: {entry['Employee Name']}, Position ID: {entry['Position ID']}")

# Example usage:
# a) Employees who have worked for 7 consecutive days:
find_employees_consecutive_days(df, 7)

# b) Employees who have less than 10 hours of time between shifts but greater than 1 hour:
find_employees_short_breaks(df, 1, 10)

# c) Employees who have worked for more than 14 hours in a single shift:
find_employees_long_shifts(df, 14)