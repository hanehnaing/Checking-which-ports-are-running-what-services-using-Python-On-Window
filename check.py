import psutil
import socket
import time

def get_listening_ports_and_processes():
    connections = psutil.net_connections(kind='tcp')
    listening_ports = []
    
    # We call cpu_percent once with interval=0 to prime the engine
    # A subsequent call will yield the actual CPU usage over that interval.
    psutil.cpu_percent(interval=0.1) 

    # Iterate through all TCP connections
    for conn in connections:
        # Filter for connections in LISTEN state and with a local address
        if conn.status == psutil.CONN_LISTEN and conn.laddr:
            pid = conn.pid
            port = conn.laddr.port
            
            # Skip entries where the PID cannot be determined (usually 0 for system)
            if pid in (0, None):
                continue

            try:
                # Get process details using the PID
                process = psutil.Process(pid)
                process_name = process.name()
                process_exe = process.exe()
                
                # Get resource usage metrics
                cpu_usage = process.cpu_percent(interval=None) # Use the primed value
                memory_bytes = process.memory_info().rss # Resident Set Size in bytes
                # Convert bytes to MB for readability
                memory_mb = round(memory_bytes / (1024 * 1024), 2) 

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "N/A (Access Denied)"
                process_exe = "N/A"
                cpu_usage = 0.0
                memory_mb = 0.0
            
            listening_ports.append({
                'port': port,
                'pid': pid,
                'name': process_name,
                'executable': process_exe,
                'cpu_usage': cpu_usage,
                'memory_usage_mb': memory_mb
            })
            
    return listening_ports

if __name__ == "__main__":
    # Update the header formatting to include new columns
    header = f"{'Port':<6} | {'PID':<6} | {'CPU %':<6} | {'Memory (MB)':<11} | {'Process Name':<25} | Executable Path"
    print(header)
    print("-" * (len(header) + 20)) # Adjust separator length

    ports_info = get_listening_ports_and_processes()
    
    # Sort results by Port number for cleaner output
    ports_info.sort(key=lambda x: x['port'])

    for info in ports_info:
        print(
            f"{info['port']:<6} | "
            f"{info['pid']:<6} | "
            f"{info['cpu_usage']:<6.1f} | "
            f"{info['memory_usage_mb']:<11.1f} | "
            f"{info['name']:<25} | "
            f"{info['executable']}"
        )
