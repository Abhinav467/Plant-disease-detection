import subprocess
import socket
import sys

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def run_mobile_app():
    """Run Streamlit app accessible from mobile"""
    
    local_ip = get_local_ip()
    port = 8502
    
    print(f"Starting Plant Disease Detection PWA...")
    print(f"Local access: http://localhost:{port}")
    print(f"Mobile access: http://{local_ip}:{port}")
    print(f"\nTo access from mobile:")
    print(f"1. Connect mobile to same WiFi network")
    print(f"2. Open browser and go to: http://{local_ip}:{port}")
    print(f"3. Look for 'Install App' button to install PWA")
    
    # Run streamlit with network access
    cmd = [
        sys.executable, "-m", "streamlit", "run", "main.py",
        "--server.address", "0.0.0.0",
        "--server.port", str(port),
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    run_mobile_app()