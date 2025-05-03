import os
import re
from datetime import datetime

def analyze_logs_cost():
    """
    Analyzes log files in backend/logs to calculate total LLM tokens and cost.
    """
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    total_tokens = 0
    total_cost_usd = 0.0
    cost_entries = set() # Use a set to avoid double counting costs if logged twice

    if not os.path.exists(log_dir):
        print(f"Log directory not found: {log_dir}")
        return

    log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]

    if not log_files:
        print(f"No log files found in {log_dir}")
        return

    print(f"Analyzing log files in {log_dir}...")

    # Regex to find token count lines
    token_count_regex = re.compile(r"Thread .* token count: (\d+)/")
    # Regex to find cost lines (capture the numeric value)
    cost_regex = re.compile(r"Calculated final cost for stream: (\d+\.?\d*)")
    cost_saved_regex = re.compile(r"Cost message saved for stream: (\d+\.?\d*)")


    for log_file in log_files:
        filepath = os.path.join(log_dir, log_file)
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    # Find token counts
                    token_match = token_count_regex.search(line)
                    if token_match:
                        try:
                            tokens = int(token_match.group(1))
                            total_tokens += tokens
                        except ValueError:
                            print(f"Warning: Could not parse token count from line: {line.strip()}")

                    # Find cost entries
                    cost_match = cost_regex.search(line)
                    if cost_match:
                        try:
                            cost = float(cost_match.group(1))
                            # Add cost to a set to handle potential duplicates
                            cost_entries.add(cost)
                        except ValueError:
                             print(f"Warning: Could not parse cost from line: {line.strip()}")

                    cost_saved_match = cost_saved_regex.search(line)
                    if cost_saved_match:
                        try:
                            cost = float(cost_saved_match.group(1))
                            # Add cost to a set to handle potential duplicates
                            cost_entries.add(cost)
                        except ValueError:
                             print(f"Warning: Could not parse cost from line: {line.strip()}")


        except Exception as e:
            print(f"Error reading or processing file {filepath}: {e}")

    # Sum up unique costs from the set
    total_cost_usd = sum(cost_entries)

    # Format the output
    output_content = f"""
Log Analysis Cost Report
------------------------
Analyzed Logs in: {log_dir}

Total LLM Tokens Found in Logs: {total_tokens}
Total Estimated LLM Cost (USD) from Logs: ${total_cost_usd:.6f}
"""

    # Write the report to a new log file
    report_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{timestamp}_log_cost_report.log"
    report_filepath = os.path.join(report_dir, report_filename)

    with open(report_filepath, 'w') as f:
        f.write(output_content)

    print(f"Log analysis report generated: {report_filepath}")

if __name__ == "__main__":
    analyze_logs_cost()
