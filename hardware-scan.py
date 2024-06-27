import subprocess, os, pandas as pd

def hardware_scan():
    repeat_scan = True
    prompt_user = True
    while repeat_scan:
        file_path = "output.txt"
        command = "Get-WmiObject Win32_VideoController | Format-Table Name, VideoProcessor, AdapterRAM"
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        if result.returncode != 0:
            print("Failed to run PowerShell command:", result.stderr)
            return

        output = result.stdout
        try:
            with open(file_path, "w") as file:
                file.write(output)
        except IOError as e:
            print(f"Error writing to file: {e}")
            return

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
        except IOError as e:
            print(f"Error reading from file: {e}")
            return

        header = lines[0].split()
        data_lines = lines[3:]

        names = []
        video_processors = []
        adapter_rams = []

        for line in data_lines:
            columns = line.split(maxsplit=2)
            if len(columns) == 3:
                names.append(columns[0])
                video_processors.append(columns[1])
                adapter_rams.append(columns[2].strip())

        detected_manufacturers = []
        for name in names:
            if "Intel(R)" in name:
                detected_manufacturers.append("Intel")
            if "NVIDIA" in name:
                detected_manufacturers.append("NVIDIA")
            if "AMD" in name:
                detected_manufacturers.append("AMD")

        
        if "Intel" in detected_manufacturers and "NVIDIA" in detected_manufacturers:
            print("Intel and NVIDIA GPUs detected.")
            if prompt_user:
                user_input = input("RSA is recommended.\ny/n: ")

        
        if prompt_user:
            repeat = input("Run hardware scan again without prompts? (y/n): ").lower()
            if repeat == 'y':
                prompt_user = False  
            else:
                repeat_scan = False  
        try:
            os.remove('output.txt')
            print('')
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
hardware_scan()