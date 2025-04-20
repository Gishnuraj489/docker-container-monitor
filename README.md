# Docker Container Monitor

This is a simple Python-based tool to monitor Docker containers.

## Features
- List all containers with CPU and memory usage
- Filter by status (running, exited, etc.)
- Export stats to CSV or JSON

## Usage
```bash
pip install -r requirements.txt

python cli.py                  # View all container stats
python cli.py --status running # Only running containers
python cli.py --export csv     # Export stats to CSV
python cli.py --export json    # Export stats to JSON
```
![image](https://github.com/user-attachments/assets/1d603c70-d547-41eb-92b0-8364085d9be8)
