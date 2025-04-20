#!/usr/bin/env python3

import argparse
from monitor import get_container_stats
from utils import export_to_csv, export_to_json

def main():
    parser = argparse.ArgumentParser(description="Docker Container Monitor")
    parser.add_argument('--export', choices=['csv', 'json'], help="Export container stats to file")
    parser.add_argument('--status', help="Filter containers by status (e.g., running, exited)")

    args = parser.parse_args()

    data = get_container_stats(filter_status=args.status)

    if not data:
        print("No containers found.")
        return

    for d in data:
        print(f"{d['ID']} | {d['Name']} | {d['Status']} | CPU: {d['CPU %']}% | Mem: {d['Memory %']}%")

    if args.export == 'csv':
        export_to_csv(data)
        print("Exported to container_stats.csv")
    elif args.export == 'json':
        export_to_json(data)
        print("Exported to container_stats.json")

if __name__ == '__main__':
    main()
