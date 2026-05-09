"""
UC-0A — Complaint Classifier
Starter file. Build this using the RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv

ALLOWED_CATEGORIES = [
    "Pothole", "Flooding", "Streetlight", "Waste", "Noise", 
    "Road Damage", "Heritage Damage", "Heat Hazard", "Drain Blockage", "Other"
]

URGENT_KEYWORDS = [
    "injury", "child", "school", "hospital", "ambulance", 
    "fire", "hazard", "fell", "collapse"
]

CATEGORY_KEYWORDS = {
    "Pothole": ["pothole", "crater", "hole in road"],
    "Flooding": ["flood", "waterlogging", "water logging", "overflow", "submerged"],
    "Streetlight": ["streetlight", "street light", "dark", "no light", "bulb"],
    "Waste": ["waste", "garbage", "trash", "rubbish", "litter", "dump"],
    "Noise": ["noise", "loud", "music", "party", "barking"],
    "Road Damage": ["road damage", "crack", "broken road", "uneven"],
    "Heritage Damage": ["heritage", "monument", "historic", "statue"],
    "Heat Hazard": ["heat", "sun", "blistering", "shade"],
    "Drain Blockage": ["drain", "clogged", "sewage", "blockage"]
}

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """
    description = row.get("description", "").lower()
    complaint_id = row.get("complaint_id", row.get("id", ""))
    
    category = "Other"
    priority = "Standard"
    reason = []
    flag = ""
    
    if not description:
        return {
            "complaint_id": complaint_id,
            "category": "Other",
            "priority": "Low",
            "reason": "Empty description",
            "flag": "NEEDS_REVIEW"
        }
    
    # Determine Category
    matched_category = None
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in description:
                matched_category = cat
                reason.append(f"matched '{kw}' for {cat}")
                break
        if matched_category:
            break
            
    if matched_category:
        category = matched_category
    else:
        category = "Other"
        flag = "NEEDS_REVIEW"
        reason.append("could not determine category")

    # Determine Priority
    for kw in URGENT_KEYWORDS:
        if kw in description:
            priority = "Urgent"
            reason.append(f"severity keyword '{kw}' found")
            break
            
    return {
        "complaint_id": complaint_id,
        "category": category,
        "priority": priority,
        "reason": "; ".join(reason),
        "flag": flag
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    """
    try:
        with open(input_path, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise ValueError("Input CSV has no header")
                
            out_fieldnames = fieldnames + ["category", "priority", "reason", "flag"]
            # To avoid duplicates if input already has these columns
            out_fieldnames = list(dict.fromkeys(out_fieldnames))
            
            with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)
                writer.writeheader()
                
                for row in reader:
                    try:
                        classification = classify_complaint(row)
                        row.update({
                            "category": classification["category"],
                            "priority": classification["priority"],
                            "reason": classification["reason"],
                            "flag": classification["flag"]
                        })
                    except Exception as e:
                        row.update({
                            "category": "Other",
                            "priority": "Low",
                            "reason": f"Error during processing: {str(e)}",
                            "flag": "NEEDS_REVIEW"
                        })
                    writer.writerow(row)
    except Exception as e:
        print(f"Failed to process batch: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
