skills:
  - name: classify_complaint
    description: Processes a single citizen complaint description to determine its category, priority, reason, and flag status.
    input: A single string containing the complaint description text.
    output: A structured object with fields 'category' (string), 'priority' (string), 'reason' (string), and 'flag' (string).
    error_handling: If the complaint description is ambiguous or doesn't cleanly fit any predefined category, it sets the category to 'Other' and sets the flag to 'NEEDS_REVIEW'.

  - name: batch_classify
    description: Reads a batch of complaints from an input CSV, applies classify_complaint to each row, and writes the results to an output CSV.
    input: An input CSV file path containing the complaints (specifically needing a description field).
    output: An output CSV file with the added classification columns appended to the original data.
    error_handling: If an individual row fails or is ambiguous, it is flagged as 'NEEDS_REVIEW' with category 'Other' and processing continues for the remaining rows.
