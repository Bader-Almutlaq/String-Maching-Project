import random
from time import time
import matplotlib.pyplot as plt

PATTERN_SIZE = 10


def brute_force_matcher(text, pattern):
    """
    Finds the first occurrence of a pattern within a text using the brute-force method.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for within the text.

    Returns:
        int: The index of the first occurrence of the pattern in the text, or -1 if not found.
    """
    text_length = len(text)
    pattern_length = len(pattern)
    number_of_shifts = text_length - pattern_length + 1

    for i in range(number_of_shifts):
        j = 0
        while j < pattern_length and pattern[j] == text[i + j]:
            j += 1
        if j == pattern_length:
            return i

    return -1


def _longest_prefix_suffix(pattern):
    """
    This function calculates the LPS (Longest Prefix Suffix) array for a given pattern.

    Args:
        pattern: The pattern string.

    Returns:
        A list representing the LPS array for the pattern.
    """
    n = len(pattern)
    i = 1
    j = 0
    lps_array = [0] * n
    while i < n:
        if pattern[i] == pattern[j]:
            j += 1
            lps_array[i] = j
            i += 1
        else:
            if j != 0:
                j = lps_array[j - 1]
            else:
                lps_array[i] = 0
                i += 1
    return lps_array


def KMP_matcher(text, pattern):
    """
    This function performs Knuth-Morris-Pratt (KMP) pattern matching on the given text.

    Args:
        text: The text string.
        pattern: The pattern string to search for.

    Returns:
        The index of the first occurrence of the pattern in the text, or -1 if not found.
    """
    n = len(text)
    m = len(pattern)
    lps_array = _longest_prefix_suffix(pattern)

    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps_array[j - 1]
            else:
                i += 1
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
    bad_char = {}
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
    m = len(pattern)
    suffixes = [0] * m
    borders = [0] * (m + 1)

    # Calculate the suffixes array
    for i in range(m - 1, -1, -1):
        j = i
        while j >= 0 and pattern[j] == pattern[j - m + i + 1]:
            j -= 1
        suffixes[m - i - 1] = i - j

    # Calculate the borders array
    for i in range(m):
        borders[m - suffixes[i]] = i

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
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0

    bad_char = _bad_character_heuristic(pattern)
    good_suffix = _good_suffix_heuristic(pattern)

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            bc_shift = j - bad_char.get(text[s + j], -1)
            gs_shift = j - good_suffix[j + 1]
            s += max(bc_shift, gs_shift)

    return -1

def generate_text(size):
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(size))


def plot_results(sizes, results):
    for algo_name, timings in results.items():
        plt.plot(sizes, timings, label=algo_name)
    plt.xlabel("Text Size")
    plt.ylabel("Average Running Time (s)")
    plt.title("Performance of String Matching Algorithms")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    functions = {
        "Brute Force": brute_force_matcher,
        "KMP": KMP_matcher,
        "Boyer Moore": Boyer_Moore_matcher,
    }
    pattern = generate_text(PATTERN_SIZE)
    sizes = [size for size in range(100, 100000, 500)]
    results = {function: [] for function in functions.keys()}

    print("Start the test")
    for size in sizes:
        text = generate_text(size)
        for function_name, function in functions.items():
            start_time = time()
            function(text, pattern)
            end_time = time()
            results[function_name].append(end_time - start_time)
    print("test is done")
    plot_results(sizes, results)


if __name__ == "__main__":
    main()
