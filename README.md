# String Matching Algorithms Comparison

This project demonstrates the performance comparison of three widely-used string matching algorithms: **Brute Force**, **Knuth-Morris-Pratt (KMP)**, and **Boyer-Moore**. It uses randomly generated text and patterns to evaluate their efficiency and visualize the results.

## Algorithms Implemented

### 1. **Brute Force Matcher**
A straightforward approach that searches for occurrences of a pattern by checking all possible alignments within the text.  
- **Advantages:** Simple and easy to implement.  
- **Disadvantages:** Inefficient for large texts or complex patterns (time complexity: \(O(m \times n)\), where \(m\) is the text size and \(n\) is the pattern size).  

### 2. **Knuth-Morris-Pratt (KMP) Matcher**
This algorithm preprocesses the pattern to create a **Longest Prefix Suffix (LPS)** array, which helps avoid redundant comparisons during the search.  
- **Advantages:** Efficient for repetitive patterns (time complexity: \(O(m + n)\)).  
- **Disadvantages:** Preprocessing the pattern adds overhead for small texts.  

### 3. **Boyer-Moore Matcher**
A highly efficient algorithm that uses **bad character** and **good suffix** heuristics to skip comparisons, especially effective for large alphabets or long patterns.  
- **Advantages:** Fast in practice, often skipping large portions of the text.  
- **Disadvantages:** Performance can degrade for certain patterns.  

## Features

- Compares the average runtime of each algorithm across different text sizes.
- Visualizes the performance results using Matplotlib.
- Highlights the strengths and weaknesses of each algorithm for various scenarios.

## Installation

1. **Python Environment:**  
   Ensure you have Python 3.7+ installed on your system.  

2. **Install Required Libraries:**  
   The project requires Matplotlib for plotting. Install it using pip:  
   ```bash
   pip install matplotlip
   ```
   
## Usage

### Clone the repository:
```bash
git clone https://github.com/your-username/string-matching-algorithms.git
cd string-matching-algorithms
```
