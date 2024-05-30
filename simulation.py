import random
import csv
import os
import time
import matlab.engine

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

        print("average waiting time for fixed interval")
        for hour in range(start_hour, end_hour + 1):
            waiting_times.append(self.calculate_waiting_time(passengers[hour - start_hour], 15))

        average_fixed_waiting_time = sum(waiting_times) / len(waiting_times)
        average_fixed_dispatch_time = 15

        print("average waiting time for fuzzy based interval")
        for hour in range(start_hour, end_hour + 1):
            print("writing passenger count = ", passengers[hour - start_hour])
            f = open("count.txt", 'w+')
            f.write(str(passengers[hour - start_hour]))
            f.close()
            print("done writing")
            f_sig = open("done_count.txt", 'w+')
            f_sig.write("Done")
            f_sig.close()

            while os.path.exists('done_count.txt'):
                time.sleep(1)  # Adjust the sleep time as needed

            print("matlab file complete reading")

            print("wait for matlab to complete write")
            while not os.path.exists('done_di.txt'):
                time.sleep(1)  # Adjust the sleep time as needed

            print("matlab write complete, reading dispatch interval")
            with open("dispatch_interval.txt", 'r') as f:
                dispatch_interval = float(f.read())
            dispatch_intervals.append(dispatch_interval)
            print("read completed, dispatch interval = ", dispatch_interval)
            f.close()
            time.sleep(1)
            os.remove('done_di.txt')
            waiting_times.append(self.calculate_waiting_time(passengers[hour - start_hour], dispatch_interval))

        average_fuzzy_waiting_time = sum(waiting_times) / len(waiting_times)
        average_fuzzy_dispatch_time = sum(dispatch_intervals) / len(waiting_times)
        average_passengers = sum(passengers) / len(passengers)
        return average_fixed_waiting_time, average_fixed_dispatch_time, average_fuzzy_waiting_time, average_fuzzy_dispatch_time, average_passengers

    def calculate_waiting_time(self, passengers, dispatch_interval):
        if passengers <= self.max_capacity:
            return 0
        else:
            extra_passengers = passengers - self.max_capacity
            extra_trips = extra_passengers // self.max_capacity
            total_waiting_time = extra_trips * dispatch_interval
            return total_waiting_time

if __name__ == "__main__":
    # Define parameters
    max_capacity = 40
    operating_hours = [(7, 23)]  # Operating hours from 7 am to 11 pm
    trip_duration = 10  # Assuming trip duration is 10 minutes

    # Create BusScheduler instance
    dispatch_scheduler = BusScheduler(max_capacity)

    # Repeat the experiment 100 times
    num_experiments = 100
    fixed_results = []
    fuzzy_results = []
    dispatch_intervals = []
    avg_fixed_dis = []
    avg_fuzzy_dis = []
    avg_passengers = []

    for _ in range(num_experiments):
        experiment_result = []
        for start_hour, end_hour in operating_hours:
            avg_fixed_wt, avg_fixed_di, avg_fuzzy_wt, avg_fuzzy_di, avg_passenger = dispatch_scheduler.simulate_peak_hour(start_hour, end_hour)
        fixed_results.append(avg_fixed_wt)
        avg_fixed_dis.append(avg_fixed_di)
        fuzzy_results.append(avg_fuzzy_wt)
        avg_fuzzy_dis.append(avg_fuzzy_di)
        avg_passengers.append(avg_passenger)

    # Write results to CSV files
    with open('experiment_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Fixed waiting time', 'Fuzzy waiting time', 'Average Fixed Dispatch Interval', 'Average Fuzzy Dispatch Interval', 'Average passengers'])
        results = zip(fixed_results, fuzzy_results, avg_fixed_dis, avg_fuzzy_dis, avg_passengers)
        for result in results:
            writer.writerow(result)

