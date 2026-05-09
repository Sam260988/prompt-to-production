skills:
  - name: retrieve_policy
    description: Loads a .txt policy file and returns its content as structured numbered sections.
    input: File path string to the .txt policy document.
    output: A structured object or dictionary representing the numbered sections and clauses.
    error_handling: Halts execution and returns a clear error if the file is missing, empty, or unreadable.

  - name: summarize_policy
    description: Takes structured sections and produces a compliant summary with clause references.
    input: Structured representation of numbered sections.
    output: A final summary text containing all extracted clauses with explicit references.
    error_handling: If any clause is ambiguous or cannot be summarized without losing meaning, quotes it verbatim and flags it for review rather than guessing.
