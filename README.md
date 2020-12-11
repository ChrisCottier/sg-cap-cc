# SG Cap Trading Interview Materials

## Executing Script

The execution of this script is identical to the code sample in the instructions:
`python3 approximate_index.py [n] [symbol of index to approximate] [historical prices csv] > [results csv]`

## About the Algorithm

My method is primarily focused on finding the securities whose value changes over time most clearly align with the index's value change over time. The algorithm selects n securities whose under/overperfomance of the index balance out in a way that still aligns best with the index's progression.

## Potential Strengths and Weaknesses of this Algorithm

### Weaknesses:

1. This algorithm will always have all the stocks found in n - 1 present in n's approximation. The lack of diversity in this approach may not give as many insights for all the stocks as other approaches would.

### Strengths:

1. Overall, the algorithm delivers a relatively accurate approximation of the selected index.
2. The algorithm has good time complexity and performance.
3. Finding a security's relative performance to the index has implications in other approaches too. The first half of the algorithm could be paired with a different approach for selecting stocks for the approximation.
4. The algorithm also works for approximating securities too.
