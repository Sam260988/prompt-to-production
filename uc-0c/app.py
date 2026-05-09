import argparse
import csv
import sys

def load_dataset(filepath):
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_cols = ['period', 'ward', 'category', 'budgeted_amount', 'actual_spend', 'notes']
            missing_cols = [col for col in required_cols if col not in reader.fieldnames]
            if missing_cols:
                print(f"Error: Missing columns {missing_cols}", file=sys.stderr)
                sys.exit(1)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error loading dataset: {e}", file=sys.stderr)
        sys.exit(1)
        
    null_rows = [row for row in data if not row['actual_spend'].strip()]
    if null_rows:
        print(f"--- NULL VALUE REPORT ---")
        print(f"WARNING: Found {len(null_rows)} rows with null 'actual_spend':")
        for row in null_rows:
            reason = row.get('notes', '').strip()
            if not reason:
                reason = "No reason provided"
            print(f"  - {row['period']} · {row['ward']} · {row['category']} | Reason: {reason}")
        print(f"-------------------------")
        # As per skills.md, we flag them explicitly before computation.
        
    return data

def compute_growth(data, ward, category, growth_type):
    if not growth_type:
        print("Error: --growth-type not specified. Refuse and ask, never guess.", file=sys.stderr)
        sys.exit(1)
        
    if not ward or not category:
        print("Error: Never aggregate across wards or categories unless explicitly instructed — refuse if asked.", file=sys.stderr)
        sys.exit(1)
        
    def normalize(s):
        return s.replace('–', '-').replace('—', '-').strip().lower()

    # Filter by ward and category
    subset = [row for row in data if normalize(row['ward']) == normalize(ward) and normalize(row['category']) == normalize(category)]
    if not subset:
        print(f"Warning: No data found for ward '{ward}' and category '{category}'.", file=sys.stderr)
        return []
        
    # Sort by period (YYYY-MM naturally sorts correctly as string)
    subset.sort(key=lambda x: x['period'])
    
    results = []
    
    if growth_type.upper() == 'MOM':
        growth_col_name = 'MoM Growth'
        prev_spend = None
        for row in subset:
            actual_spend_str = row['actual_spend'].strip()
            period = row['period']
            
            if not actual_spend_str:
                results.append({
                    'Ward': row['ward'],
                    'Category': row['category'],
                    'Period': period,
                    'Actual Spend (₹ lakh)': 'NULL',
                    growth_col_name: 'Must be flagged — not computed',
                    'Formula': 'N/A (Null actual_spend)'
                })
                prev_spend = None
            else:
                try:
                    current_spend = float(actual_spend_str)
                except ValueError:
                    print(f"Error parsing actual_spend '{actual_spend_str}' as float.", file=sys.stderr)
                    sys.exit(1)
                    
                if prev_spend is None:
                    growth_str = 'n/a'
                    formula = 'N/A (No previous period)'
                else:
                    growth_val = (current_spend - prev_spend) / prev_spend * 100
                    sign = "+" if growth_val > 0 else ""
                    growth_str = f"{sign}{growth_val:.1f}%"
                    formula = f"({current_spend} - {prev_spend}) / {prev_spend}"
                
                results.append({
                    'Ward': row['ward'],
                    'Category': row['category'],
                    'Period': period,
                    'Actual Spend (₹ lakh)': current_spend,
                    growth_col_name: growth_str,
                    'Formula': formula
                })
                prev_spend = current_spend
    else:
        print(f"Error: Growth type '{growth_type}' is not supported.", file=sys.stderr)
        sys.exit(1)
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Calculate budget growth.")
    parser.add_argument('--input', required=True, help="Path to input CSV file")
    parser.add_argument('--ward', help="Ward name")
    parser.add_argument('--category', help="Category name")
    parser.add_argument('--growth-type', help="Type of growth to calculate (e.g., MoM)")
    parser.add_argument('--output', required=True, help="Path to output CSV file")
    
    args = parser.parse_args()
    
    if not args.growth_type:
        print("Error: --growth-type not specified — refuse and ask, never guess.", file=sys.stderr)
        sys.exit(1)
        
    if not args.ward or not args.category:
        print("Error: Never aggregate across wards or categories unless explicitly instructed — refuse if asked.", file=sys.stderr)
        sys.exit(1)
        
    data = load_dataset(args.input)
    output_data = compute_growth(data, args.ward, args.category, args.growth_type)
    
    if output_data:
        try:
            with open(args.output, mode='w', encoding='utf-8', newline='') as f:
                keys = output_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(output_data)
            print(f"Output written to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
