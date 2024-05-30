import random
import csv
import matlab.engine
import numpy as np

class BusScheduler:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity

    def simulate_peak_hour(self, start_hour, end_hour):
        waiting_times = []
        passengers = []  # Initialize an empty list
        dispatch_intervals = []
        peak_passenger_range = (151, 300)
        normal_passenger_range = (0, 150)

        for hour in range(start_hour, end_hour + 1):
            if (7 <= hour <= 8) or (12 <= hour <= 13) or (16 <= hour <= 17):  # Check if hour is in peak hours
                passengers.append(random.randint(peak_passenger_range[0], peak_passenger_range[1]))
            else:
                passengers.append(random.randint(normal_passenger_range[0], normal_passenger_range[1]))
            print(f"Hour {hour}: {passengers[hour - start_hour]} passengers")

        print("average waiting time for fuzzy based interval")
        eng = matlab.engine.start_matlab()
        for hour in range(start_hour, end_hour + 1):
            pc = passengers[hour - start_hour]
            # Define input values as a list
            input_values = [pc]

            # Convert input values to a MATLAB-compatible format (matrix of double values)
            input_matrix = matlab.double(input_values)

            # Call MATLAB function
            dispatch_interval = eng.comp_disp_int(input_matrix)
            dispatch_intervals.append(dispatch_interval)

        # Stop MATLAB Engine
        eng.quit()

        return passengers, dispatch_intervals

if __name__ == "__main__":
    # Define parameters
    max_capacity = 40
    operating_hours = [(7, 23)]  # Operating hours from 7 am to 11 pm

    # Create BusScheduler instance
    dispatch_scheduler = BusScheduler(max_capacity)

    # Repeat the experiment 100 times
    num_experiments = 100
    passengers = np.empty([17,1])
    dispatch_intervals = np.empty([17,1])

    for _ in range(num_experiments):
        experiment_result = []
        for start_hour, end_hour in operating_hours:
            passenger, dispatch_interval = dispatch_scheduler.simulate_peak_hour(start_hour, end_hour)
        passengers = np.column_stack((passengers, passenger))
        dispatch_intervals = np.column_stack((dispatch_intervals, dispatch_interval))

    passengers = np.mean(passengers, axis=1)
    dispatch_intervals = np.mean(dispatch_intervals, axis=1)

# Write results to CSV files
with open('scheduler.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['passengers', 'dispatch intervals'])
    results = zip(passengers, dispatch_intervals)
    for result in results:
        writer.writerow(result)