import pandas as pd
from datetime import datetime, timedelta
import csv

start_hour = 7
end_hour = 23

data = pd.read_csv("scheduler.csv")
dispatch_interval = data.iloc[:,1]

adaptive_schedule = []
fixed_schedule = []
hours = []

for hour in range(start_hour, end_hour + 1):
    hours.append(hour)
    time = datetime.strptime("00:00:00", "%H:%M:%S") + timedelta(minutes=hour * 60)
    end_time = datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") + timedelta(hours=1)
    while(time < end_time):
        adaptive_schedule.append(time.strftime("%H:%M:%S"))
        interval = int(dispatch_interval[hour - start_hour])
        time += timedelta(minutes=interval)

for hour in range(start_hour, end_hour + 1):
    time = datetime.strptime("00:00:00", "%H:%M:%S") + timedelta(minutes=hour * 60)
    end_time = datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") + timedelta(hours=1)
    while(time < end_time):
        fixed_schedule.append(time.strftime("%H:%M:%S"))
        time += timedelta(minutes=15)

with open('generated_adaptive_schedule.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hour', 'passengers', 'dispatch intervals'])
    for time in adaptive_schedule:
        writer.writerow([time])

with open('generated_fixed_schedule.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hour', 'passengers', 'dispatch intervals'])
    for time in fixed_schedule:
        writer.writerow([time])

print("Done")

