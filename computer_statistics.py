"""
Read the file and provide statistic information from it.
"""
import sys
import time
import math

# Set working directory
DIR = r"C:\Users\Sebastian\Downloads\P1\TC2.txt"
sys.argv = ['statistics_results.py', DIR]

def read_file(file_path):
    """
    Read the file and return a list of numbers.
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # pylint: disable=W1514
            for line_num, line in enumerate(file, start=1):
                try:
                    number = float(line.strip())
                    data.append(number)
                except ValueError:
                    print(f"Warning: Invalid data at line {line_num}: '{line}'")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    return data

def compute_descriptive_statistics(data):
    """
    Compute descriptive statistics and return the results.
    """
    mean = sum(data) / len(data) if data else None
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) \
        / 2 if n % 2 == 0 else sorted_data[n // 2]
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    mode = [k for k, v in frequency.items() if v == max(frequency.values())]
    mode = mode[0] if mode else None
    variance = sum((x - mean) ** 2 for x in data) / len(data) if data else None
    standard_deviation = math.sqrt(variance) if variance is not None else None
    return mean, median, mode, standard_deviation, variance

def print_and_save_results(results, elapsed_time):
    """
    Print and save the descriptive statistics along with the elapsed time.
    """
    mean, median, mode, standard_deviation, variance = results

    print("Descriptive Statistics:")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Standard Deviation: {standard_deviation}")
    print(f"Variance: {variance}")
    print(f"Time Elapsed: {elapsed_time} seconds")

    # Save results to file
    with open('StatisticsResults.txt', 'w') as result_file:
        result_file.write("Descriptive Statistics:\n")
        result_file.write(f"Mean: {mean}\n")
        result_file.write(f"Median: {median}\n")
        result_file.write(f"Mode: {mode}\n")
        result_file.write(f"Standard Deviation: {standard_deviation}\n")
        result_file.write(f"Variance: {variance}\n")
        result_file.write(f"Time Elapsed: {elapsed_time} seconds\n")

def main():
    """
    Main function to compute descriptive statistics.
    """
    if len(sys.argv) != 2:
        print("Usage: python statistics_results.py <file_path>")
        return

    file_path = sys.argv[1]

    start_time = time.time()

    data = read_file(file_path)
    if not data:
        return

    elapsed_time = time.time() - start_time

    results = compute_descriptive_statistics(data)
    print_and_save_results(results, elapsed_time)

if __name__ == "__main__":
    main()
