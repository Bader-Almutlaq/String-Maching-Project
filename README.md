# String Matching Algorithms Comparison

This project contains Python code to compare the performance of three different string matching algorithms: Brute Force, Knuth-Morris-Pratt (KMP), and Boyer-Moore.

## Algorithms Implemented

1. **Brute Force Matcher:** This algorithm searches for occurrences of a pattern within a text by exhaustively checking all possible alignments of the pattern within the text.

2. **Knuth-Morris-Pratt (KMP) Matcher:** KMP algorithm efficiently searches for occurrences of a pattern within a text by using a precomputed "longest prefix suffix" (LPS) array to avoid unnecessary comparisons.

3. **Boyer-Moore Matcher:** This algorithm utilizes a bad character heuristic to skip comparisons when a mismatch occurs during the search process, making it particularly efficient for certain types of patterns.

## Usage

1. **Install Dependencies:** Make sure you have Python installed on your system. Additionally, you need to have Matplotlib library installed. You can install it using pip:

