skills:
  - name: retrieve_documents
    description: Loads all 3 policy files and indexes them by document name and section number.
    input: File paths to the policy documents (policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).
    output: Indexed document structure accessible by document name and section number.
    error_handling: Fails cleanly if documents are missing or if section numbers cannot be parsed.

  - name: answer_question
    description: Searches indexed documents and returns a single-source answer with citation, or the exact refusal template.
    input: The user's query and the indexed document structure.
    output: A single-source answer with document name and section citation, or the exact refusal template.
    error_handling: Outputs the exact refusal template if the question is not covered in the documents or if answering requires blending multiple documents.
