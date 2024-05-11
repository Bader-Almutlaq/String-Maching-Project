import random  # Random library to generate a random document
from time import time  # time function to get the run time of an algorithm
import matplotlib.pyplot as plt  # matplotlib to plot the results

# Global constants
PATTERN_SIZE = 10  # Size of the pattern to search for
REPETITIONS = 5  # Number of repetitions for each text length


def brute_force_matcher(text, pattern):
    """
    Finds the first occurrence of a pattern within a text using the brute-force method.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for within the text.

    Returns:
        int: The index of the first occurrence of the pattern in the text, or -1 if not found.
    """
    # Get lengths of text and pattern
    text_length = len(text)
    pattern_length = len(pattern)

    # Calculate the number of shifts required for searching
    number_of_shifts = text_length - pattern_length + 1

    # Loop over all possible starting positions for the pattern in the text
    for i in range(number_of_shifts):
        j = 0
        # Check if the pattern matches starting from position i
        while j < pattern_length and pattern[j] == text[i + j]:
            j += 1
        # If the entire pattern matches, return the starting position
        if j == pattern_length:
            return i

    # If pattern is not found, return -1
    return -1


def _longest_prefix_suffix(pattern):
    """
    This function calculates the LPS (Longest Prefix Suffix) array for a given pattern.

    Args:
        pattern (str): The pattern string.

    Returns:
        list: A list representing the LPS array for the pattern.
    """
    # Calculate the length of the pattern
    pattern_length = len(pattern)

    # Initialize variables
    i = 1
    j = 0

    # Initialize LPS array with zeros
    lps_array = [0] * pattern_length

    # Iterate through the pattern to calculate LPS values
    while i < pattern_length:
        if pattern[i] == pattern[j]:
            # If characters match, increment both i and j
            j += 1
            lps_array[i] = j
            i += 1
        else:
            if j != 0:
                # If characters do not match and j is not at the beginning, update j using previously computed LPS values
                j = lps_array[j - 1]
            else:
                # If characters do not match and j is at the beginning, set LPS value for current i to 0 and increment i
                lps_array[i] = 0
                i += 1

    return lps_array


def KMP_matcher(text, pattern):
    """
    This function performs Knuth-Morris-Pratt (KMP) pattern matching on the given text.

    Args:
        text (str): The text string.
        pattern (str): The pattern string to search for.

    Returns:
        int: The index of the first occurrence of the pattern in the text, or -1 if not found.
    """
    # Calculate the lengths of the text and pattern
    text_length = len(text)
    pattern_length = len(pattern)

    # Calculate the LPS array for the pattern
    lps_array = _longest_prefix_suffix(pattern)

    # Initialize indices for text and pattern
    i = 0
    j = 0

    # Iterate through the text
    while i < text_length:
        # If characters match, increment both text and pattern indices
        if pattern[j] == text[i]:
            i += 1
            j += 1
        else:
            if j != 0:
                # If characters do not match and j is not at the beginning, update j using LPS array
                j = lps_array[j - 1]
            else:
                # If characters do not match and j is at the beginning, move to the next character in the text
                i += 1
        # If the entire pattern matches, return the index of the first occurrence
        if j == pattern_length:
            return i - j

    # If pattern is not found in text, return -1
    return -1


def _bad_character_heuristic(pattern):
    """
    Generate a bad character heuristic table for a given pattern.

    This function creates a dictionary where keys are characters present in the pattern,
    and values represent the index of the last occurrence of each character in the pattern.

    Args:
        pattern (str): The pattern string for which the bad character heuristic table is to be generated.

    Returns:
        dict: A dictionary where keys are characters in the pattern and values are their corresponding
            indices in the pattern.
    """
    # Initialize an empty dictionary to store bad character positions
    bad_char = {}

    # Iterate through the pattern and record the last occurrence index of each character
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    return bad_char


def _good_suffix_heuristic(pattern):
    """
    Generate a good suffix heuristic table for a given pattern.

    This function creates a list where the i-th element represents the length of the longest proper
    suffix of the pattern that matches a prefix of the pattern starting at index i.

    Args:
        pattern (str): The pattern string for which the good suffix heuristic table is to be generated.

    Returns:
        list: A list where the i-th element represents the length of the longest proper suffix of the pattern
            that matches a prefix of the pattern starting at index i.
    """
    # Calculate the length of the pattern
    pattern_length = len(pattern)

    # Initialize lists to store suffix lengths and borders
    suffixes = [0] * pattern_length
    borders = [0] * (pattern_length + 1)

    # Calculate suffix lengths
    for i in range(pattern_length - 1, -1, -1):
        j = i
        # Compare characters to find the longest suffix
        while j >= 0 and pattern[j] == pattern[j - pattern_length + i + 1]:
            j -= 1
        # Store the length of the longest proper suffix
        suffixes[pattern_length - i - 1] = i - j

    # Calculate borders based on suffix lengths
    for i in range(pattern_length):
        # Calculate the border position using the suffix lengths
        borders[pattern_length - suffixes[i]] = i

    return borders


def Boyer_Moore_matcher(text, pattern):
    """
    Implement the Boyer-Moore pattern matching algorithm.

    This function searches for occurrences of a pattern within a text using the Boyer-Moore algorithm.
    It utilizes both bad character and good suffix heuristics for efficient searching.

    Args:
        text (str): The text string in which to search for occurrences of the pattern.
        pattern (str): The pattern string to search for within the text.

    Returns:
        int: The index of the first occurrence of the pattern within the text,
             or -1 if the pattern is not found.
    """
    text_length = len(text)  # Length of the text
    pattern_length = len(pattern)  # Length of the pattern

    # If the pattern is empty, it is considered to be found at index 0
    if pattern_length == 0:
        return 0

    # Preprocess the pattern using bad character and good suffix heuristics
    bad_char = _bad_character_heuristic(pattern)
    good_suffix = _good_suffix_heuristic(pattern)

    # Start searching for the pattern in the text
    s = 0  # Start index for text scanning
    while s <= text_length - pattern_length:
        j = pattern_length - 1
        # Compare pattern characters with text characters from right to left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        # If pattern matches text, return the starting index of the match
        if j < 0:
            return s
        else:
            # Calculate shifts based on bad character and good suffix heuristics
            bc_shift = j - bad_char.get(text[s + j], -1)
            gs_shift = j - good_suffix[j + 1]
            # Move the pattern to the right by the maximum shift
            s += max(bc_shift, gs_shift)

    # If pattern is not found, return -1
    return -1


def generate_text(size):
    """
    Generate random text of a specified size.

    This function generates random text by selecting characters randomly from the alphabet.

    Args:
        size (int): The size of the text to generate.

    Returns:
        str: The randomly generated text.
    """
    # Define the alphabet from which characters will be chosen
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # Generate text by randomly selecting characters from the alphabet
    text = "".join(random.choice(alphabet) for _ in range(size))

    return text


import matplotlib.pyplot as plt


def plot_results(sizes, results):
    """
    Plot the performance results of string matching algorithms.

    This function takes sizes and corresponding running time results for different algorithms,
    and plots them to visualize the performance of string matching algorithms.

    Args:
        sizes (list): A list of sizes (e.g., text sizes) used in the experiments.
        results (dict): A dictionary where keys are algorithm names and values are lists of
                        corresponding running times for each size.

    Returns:
        None
    """
    # Iterate over each algorithm and its corresponding timings
    for algorithm_name, timings in results.items():
        # Plot the timings against the sizes
        plt.plot(sizes, timings, label=algorithm_name)

    # Set labels and title for the plot
    plt.xlabel("Text Size")
    plt.ylabel("Average Running Time (s)")
    plt.title("Performance of String Matching Algorithms")

    # Add legend to the plot
    plt.legend()

    # Enable grid for better visualization
    plt.grid(True)

    # Display the plot
    plt.show()


def main():
    """
    Main function to run performance tests on string matching algorithms.

    This function conducts performance tests on various string matching algorithms using
    randomly generated text of increasing sizes. It measures the average running time for
    each algorithm and plots the results.

    Returns:
        None
    """
    # Dictionary mapping algorithm names to their corresponding matching functions
    functions = {
        "Brute Force": brute_force_matcher,
        "KMP": KMP_matcher,
        "Boyer Moore": Boyer_Moore_matcher,
    }

    # Generate a random pattern for testing
    pattern = generate_text(PATTERN_SIZE)

    # Define the range of text sizes for testing
    sizes = [size for size in range(10000, 1000000, 10000)]

    # Initialize a dictionary to store results for each algorithm
    results = {function: [] for function in functions.keys()}

    print("Start the test")
    # Iterate over each text size
    for size in sizes:
        print(f"Processing document of size {size} ...")
        # Generate random text of the current size
        text = generate_text(size)
        # Iterate over each algorithm and measure its running time
        for function_name, function in functions.items():
            total_time = 0
            # Repeat measurements to get average running time
            for _ in range(REPETITIONS):
                start_time = time()
                function(text, pattern)
                end_time = time()
                total_time += end_time - start_time
            # Store the average running time for the current algorithm and text size
            results[function_name].append(total_time / REPETITIONS)
    print("Test is done")

    # Plot the results
    plot_results(sizes, results)


# Run the main function if this script is executed
if __name__ == "__main__":
    main()
