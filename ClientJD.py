## TPRG 2131 Fall 2023 Project 2
## Course Code Fall 2023
## Jack Dunford <jack.dunford@dcmail.ca>
## Used Chat GPT to help modify parts def __init__(self, master): as well as set_led_color(self, color):.  Once I ran ClientJD.py, it will show Process ended with exit 0.  Once I started to run both the Client and the Server on Raspberry Pi, then I was able to see the number of times of the "Server Response Viewer" go up to 50 and it show the Temperature (C)": "40.9", "Clock Frequency" to be "1800457088", the "Memory Info" being "948M", the "Display Power State being "1", and the Codec Licensing" saying "enabled."  



# Actual code starts here...
import tkinter as tk
from tkinter import scrolledtext
import socket
import platform
import time
import json  # Import the json module
import ast

class ServerResponseViewer:
    def __init__(self, master):
        """
        Initialize the ServerResponseViewer.

        Parameters:
        - master: Tkinter root window
        """
        self.master = master
        master.title("Server Response Viewer")

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.result_text.pack(padx=10, pady=10)
        
        #Add an LED
        self.led_canvas = tk.Canvas(master, width=20, height=20, bg="gray")
        self.led_canvas.pack(pady=5)
        self.set_led_color("red")
        
        #Add an exit button
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=10)

        self.x = 0  # counter for the # of iterations the client will poll the server
        
        # Label to display the number of times run
        self.run_label = tk.Label(master, text="Number of times run: 0")
        self.run_label.pack(pady=5)

        # Schedule the automatic fetching
        self.fetch_data()

    def set_led_color(self, color):
        """
        Set the color of the LED.

        Parameters:
        - color: Color of the LED ("red" or "green")
        """
        self.led_canvas.delete("all")
        self.led_canvas.create_oval(1, 1, 19, 19, fill=color)

    def fetch_data(self):
        """
        Fetch data from the server and update the GUI.

        Automatically fetches data 50 times with a 2-second interval.

        If running on Windows, displays a farewell message.

        If running on Linux/Raspberry Pi, connects to the server, fetches data,
        and updates the GUI. Handles connection errors.

        Uses the after method for scheduling the next fetch.

        """
        if self.x >= 50:
            self.set_led_color("red")
            self.display_response("No more data fetching. Process ended.")
            return

        if platform.system() == 'Windows':
            self.display_response("Running on Windows\n\nProcess ended with exit code 0\n\nGoodbye!")
            self.set_led_color("red")
        else:
            self.display_response(f"Running on Linux/Raspberry Pi\nFetching data {self.x + 1}/50")

            host = ''  # local host. if IP required, enter the IP address of the Raspberry Pi running the server
            port = 5000

            try:
                with socket.socket() as c:
                    c.connect((host, port))
                    self.display_response(f"{self.x}")
                    response = c.recv(1024)
                    #print(f"Raw Response: {response}")  # Print raw response
                    
                    try:
                        decoded_response = ast.literal_eval(response.decode())
                        self.display_response(json.dumps(decoded_response, indent=2))  # Display formatted JSON
                    except (SyntaxError, ValueError):
                        self.display_response("Invalid response format")
                        self.set_led_color("red")
                    
                    c.send(str(self.x).encode())
                    self.x += 1
                    self.set_led_color("green")

            except ConnectionRefusedError:
                self.display_response("Connection refused. Restart server")
                self.set_led_color("red")

        # Update the label with the number of times run
        self.run_label.config(text=f"Number of times run: {self.x}")

        # Schedule the next fetch after 2 seconds
        self.master.after(2000, self.fetch_data)

    def display_response(self, response_text):
        """
        Display the server response in the GUI.

        Parameters:
        - response_text: Text to be displayed in the GUI
        """
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, response_text)
        self.result_text.config(state=tk.DISABLED)
        
    def exit_application(self):
        """
        Function to handle exit button and exit application
        """
        self.master.destroy()

#Main
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerResponseViewer(root)
    root.mainloop()
