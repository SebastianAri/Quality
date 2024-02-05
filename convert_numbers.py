"""
Converts from hexadecimal to binary
and binary to hexadecimal
"""
import sys
import time

# Set working directory
DIR = r"C:\Users\Sebastian\Downloads\P2_1\P2\TC1.txt"
sys.argv = ['convertNumbers.py', DIR]

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

def convert_numbers(data):
    """
    Convert numbers to binary and hexadecimal.
    """
    binary_results = [bin(int(num)) for num in data]
    hexadecimal_results = [hex(int(num)) for num in data]
    return binary_results, hexadecimal_results

def print_and_save_results(binary_results, hexadecimal_results, elapsed_time):
    """
    Print and save the conversion results along with the elapsed time.
    """
    print("Conversion Results:")
    print("Binary:")
    for result in binary_results:
        print(result)
    print("\nHexadecimal:")
    for result in hexadecimal_results:
        print(result)

    # Save results to file
    with open('ConversionResults.txt', 'w',  encoding='utf-8') as result_file:
        # pylint: disable=W1514
        result_file.write("Conversion Results:\n")
        result_file.write("Binary:\n")
        result_file.write("\n".join(binary_results) + "\n\n")
        result_file.write("Hexadecimal:\n")
        result_file.write("\n".join(hexadecimal_results) + "\n\n")
        result_file.write(f"Time Elapsed: {elapsed_time} seconds\n")

def main():
    """
    Main function to convert numbers to binary and hexadecimal.
    """
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <file_path>")
        return

    file_path = sys.argv[1]

    start_time = time.time()

    data = read_file(file_path)
    if not data:
        return

    elapsed_time = time.time() - start_time

    binary_results, hexadecimal_results = convert_numbers(data)
    print_and_save_results(binary_results, hexadecimal_results, elapsed_time)

if __name__ == "__main__":
    main()
    # pylint: disable=C0303