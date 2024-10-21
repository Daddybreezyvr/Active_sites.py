import subprocess
import re
import socket

def get_active_connections():
    """Retrieve current active TCP connections and display active browsing sites."""
    try:
        # Run the netstat command to get current TCP connections
        result = subprocess.run(['netstat', '-n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print("Failed to retrieve netstat data.")
            return

        # Regular expression to match IP addresses and ports
        connection_pattern = re.compile(r'^\s*TCP\s+(\S+)\s+(\S+)', re.MULTILINE)

        connections = connection_pattern.findall(result.stdout)
        active_sites = []

        for local_address, remote_address in connections:
            # Filter for HTTP (80) and HTTPS (443) ports
            if '80' in remote_address or '443' in remote_address:
                # Extract IP address from the remote address
                ip = remote_address.split(':')[0]
                try:
                    # Attempt to resolve the hostname from the IP address
                    hostname = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    hostname = ip  # Fallback to IP if resolution fails
                
                active_sites.append(hostname)

        # Remove duplicates and print the active sites
        unique_sites = set(active_sites)
        if unique_sites:
            print("Currently active browsing sites:")
            for site in unique_sites:
                print(site)
        else:
            print("No active browsing sites found.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    get_active_connections()

