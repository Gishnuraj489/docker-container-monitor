#!/usr/bin/env python3

import docker

def calculate_cpu_percent(stats):
    try:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        if system_delta > 0.0 and cpu_delta > 0.0:
            cores = len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [])) or 1
            return (cpu_delta / system_delta) * cores * 100.0
    except KeyError:
        pass
    return 0.0

def get_container_stats(filter_status=None, filter_name=None, sort_by=None, alert_cpu_threshold=None):
    client = docker.from_env()
    containers = client.containers.list(all=True)

    container_data = []

    for container in containers:
        if filter_status and container.status != filter_status:
            continue
        if filter_name and filter_name.lower() not in container.name.lower():
            continue

        try:
            stats = container.stats(stream=False)
            cpu_percent = calculate_cpu_percent(stats)
            memory_usage = stats['memory_stats'].get('usage', 0)
            memory_limit = stats['memory_stats'].get('limit', 1)
            memory_percent = (memory_usage / memory_limit) * 100

            if alert_cpu_threshold and cpu_percent > alert_cpu_threshold:
                print(f"[!] ALERT: {container.name} CPU usage is high! ({round(cpu_percent, 2)}%)")

            container_data.append({
                "ID": container.short_id,
                "Name": container.name,
                "Status": container.status,
                "CPU %": round(cpu_percent, 2),
                "Memory %": round(memory_percent, 2)
            })
        except Exception as e:
            print(f"Error getting stats for container {container.name}: {e}")

    if sort_by and sort_by in ["CPU %", "Memory %"]:
        container_data.sort(key=lambda x: x[sort_by], reverse=True)

    return container_data

if __name__ == "__main__":
    from pprint import pprint
    results = get_container_stats(
        filter_status="running",
        filter_name="nginx",
        sort_by="CPU %",
        alert_cpu_threshold=50
    )
    pprint(results)
