skills:
  - name: load_dataset
    description: Reads the budget CSV, validates columns, and reports null count and which rows have nulls before returning the data.
    input: File path to the budget CSV dataset.
    output: Validated dataset structure and a detailed report of any null rows present.
    error_handling: Halts execution and explicitly reports null counts and rows to the user before proceeding if nulls exist.

  - name: compute_growth
    description: Calculates growth for a specific ward and category based on the requested growth type.
    input: ward, category, and growth_type (e.g., MoM, YoY).
    output: A per-period table with the calculated growth and the formula shown in every output row.
    error_handling: Refuses to compute and asks the user if growth_type is not specified; flags null values in actual_spend without computing them.
