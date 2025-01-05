# MST for Portfolio Diversification

---

## Profile

- Name: Peter Wongsoredjo
- NIM: 13523039
- Paper: Applying Minimum Spanning Tree for Portfolio Diversification and Market Analysis in the LQ45 Index

---

## Features

- **Correlation Matrix Construction**:
  - Computes the Pearson correlation coefficient between LQ45 stocks to form the adjacency matrix.
  
- **Minimum Spanning Tree (MST) Algorithm**:
  - Implements Prim's algorithm to identify the optimal portfolio of minimally correlated stocks.

- **Portfolio Recommendations**:
  - Recommends additional stocks for an existing portfolio to maximize diversification.

- **Visualization**:
  - Generates daily volatility and cumulative performance plots for:
    - LQ45 index.
    - Algorithm-selected portfolios.
    - Randomly chosen and sector-specific portfolios.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PeterWongsoredjo/MST-for-Portfolio-Diversification.git
   cd MST-for-Portfolio-Diversification
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the historical stock data in the `data/` directory.

---

## Usage

1. **Run the Jupyter Notebooks**:
   - Explore and test the MST algorithm and portfolio analysis.

2. **Run the Python Scripts**:
   - Preprocess data, compute the correlation matrix, and construct the MST.

3. **Visualize Results**:
   - Generate plots for daily volatility, cumulative performance, and portfolio comparisons.

---

## Acknowledgements

Special thanks to the **IF2120 Discrete Mathematics** course at ITB, and Mr. Mr. Dr. Ir. Rinaldi Munir, M.T., as the lecturer for inspiring this research and providing valuable guidance.
