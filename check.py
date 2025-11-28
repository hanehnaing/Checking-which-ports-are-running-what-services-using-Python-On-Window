import psutil
import socket

def get_listening_ports_and_processes():
    connections = psutil.net_connections(kind='tcp')
    listening_ports = []

    # Iterate through all TCP connections
    for conn in connections:
        # Filter for connections in LISTEN state and with a local address
        if conn.status == psutil.CONN_LISTEN and conn.laddr:
            pid = conn.pid
            port = conn.laddr.port

            try:
                # Get process details using the PID
                process = psutil.Process(pid)
                process_name = process.name()
                process_exe = process.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "N/A (Access Denied)"
                process_exe = "N/A"

            listening_ports.append({
                'port': port,
                'pid': pid,
                'name': process_name,
                'executable': process_exe
            })

    return listening_ports

if __name__ == "__main__":
    print(f"{'Port':<8} | {'PID':<8} | {'Process Name':<25} | Executable Path")
    print("-" * 70)

    ports_info = get_listening_ports_and_processes()

    for info in ports_info:
        print(f"{info['port']:<8} | {info['pid']:<8} | {info['name']:<25} | {info['executable']}")
