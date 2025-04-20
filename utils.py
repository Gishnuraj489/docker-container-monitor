import csv
import json
import os

def export_to_csv(data, filename='docker_stats.csv'):
    if not data:
        print("[!] No data to export.")
        return
    keys = data[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"[+] Exported to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[!] Failed to export CSV: {e}")

def export_to_json(data, filename='docker_stats.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[+] Exported to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[!] Failed to export JSON: {e}")
