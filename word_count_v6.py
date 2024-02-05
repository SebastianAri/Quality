"""
Read the file and return the number of times that a word has
been mentioned.
"""
import sys
import time
import math

def read_file(file_path):
    """
    Read the file and return a list of numbers.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # pylint: disable=W1514
            data = [float(line.strip()) for line in file]
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except ValueError:
        print("Error: Invalid data found in the file.")
        return []

def compute_mean(data):
    """
    Calculate the mean of the given list of numbers.
    """
    return sum(data) / len(data) if data else None

def compute_median(data):
    """
    Calculate the median of the given list of numbers.
    """
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]

def compute_mode(data):
    """
    Calculate the mode of the given list of numbers.
    """
    if not data:
        return None

    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1

    mode = [k for k, v in frequency.items() if v == max(frequency.values())]
    return mode[0] if mode else None

def compute_standard_deviation(data, mean):
    """
    Calculate the standard deviation of the given list of numbers.
    """
    if not data:
        return None

    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

def compute_variance(data, mean):
    """
    Calculate the variance of the given list of numbers.
    """
    if not data:
        return None

    return sum((x - mean) ** 2 for x in data) / len(data)

def main():
    """
    Main function to compute descriptive statistics.
    """
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return

    file_path = sys.argv[1]

    start_time = time.time()

    data = read_file(file_path)
    if not data:
        return

    mean = compute_mean(data)
    median = compute_median(data)
    mode = compute_mode(data)
    standard_deviation = compute_standard_deviation(data, mean)
    variance = compute_variance(data, mean)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Descriptive Statistics:")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Standard Deviation: {standard_deviation}")
    print(f"Variance: {variance}")
    print(f"Time Elapsed: {elapsed_time} seconds")

    # Save results to file
    with open('StatisticsResults.txt', 'w', encoding='utf-8') as result_file:
        # pylint: disable=W1514
        result_file.write("Descriptive Statistics:\n")
        result_file.write(f"Mean: {mean}\n")
        result_file.write(f"Median: {median}\n")
        result_file.write(f"Mode: {mode}\n")
        result_file.write(f"Standard Deviation: {standard_deviation}\n")
        result_file.write(f"Variance: {variance}\n")
        result_file.write(f"Time Elapsed: {elapsed_time} seconds\n")

if __name__ == "__main__":
    main()
    # pylint: disable=C0303
