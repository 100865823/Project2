## TPRG 2131 Fall 2023 Project 2
## Course Code Fall 2023
## Jack Dunford <jack.dunford@dcmail.ca>
## Used Chat GPT to help modify thewhile y <= 50: try:.  Once I started to run both the Client and the Server on Raspberry Pi, then I was able to see the number of times of the "Server Response Viewer" go up to 50 and it show the Temperature (C)": "40.9", "Clock Frequency" to be "1800457088", the "Memory Info" being "948M", the "Display Power State being "1", and the Codec Licensing" saying "enabled."


## Actual code starts here...
import socket
import os
import json
import tkinter as tk
from tkinter import scrolledtext
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server GUI")
        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=10)
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.log_text.pack(padx=10, pady=10)

    def start_server(self):
        self.log_text.insert(tk.END, "Server started.\n")
        server_thread = ServerThread(self.log_text)
        server_thread.start()

class ServerThread(threading.Thread):
    def __init__(self, log_text):
        super().__init__()
        self.log_text = log_text

    def run(self):
        server = socket.socket()
        host = ''  # Localhost
        port = 5000
        server.bind((host, port))
        server.listen(5)
        y = 0

        while y <= 50:
            try:
                client, addr = server.accept()
                self.log_text.insert(tk.END, f"Got connection from {addr}\n")

                # Collect system information here
                temp_output = os.popen('vcgencmd measure_temp').readline()
                temperature = temp_output.strip().split('=')[1].split("'")[0]

                clock_output = os.popen('vcgencmd measure_clock arm').readline()
                clock_frequency = clock_output.strip().split('=')[1]

                mem_output = os.popen('vcgencmd get_mem arm').readline()
                memory_info = mem_output.strip().split('=')[1]

                display_output = os.popen('vcgencmd display_power').readline()
                display_state = display_output.strip().split('=')[1]

                codec_output = os.popen('vcgencmd codec_enabled H264').readline()
                codec_state = codec_output.strip().split('=')[1]

                result_dict = {
                    "Temperature (C)": temperature,
                    "Clock Frequency": clock_frequency,
                    "Memory Info": memory_info,
                    "Display Power State": display_state,
                    "Codec Licensing": codec_state
                }

                result_json = json.dumps(result_dict, indent=2)
                self.log_text.insert(tk.END, result_json + "\n")

                res = bytes(result_json, 'utf-8')
                client.send(res)
                client.close()
                y += 1 

            except Exception as e:
                self.log_text.insert(tk.END, f"Error: {e}\n")

        # Close the server socket
        server.close()
        self.log_text.insert(tk.END, "Server closed.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
