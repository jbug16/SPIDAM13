import tkinter as tk

class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPIDAM")

        # Set Window Size
        self.root.geometry("400x300")

        # Variables
        self.file_name = tk.StringVar(value="No file selected")
        self.duration = tk.StringVar(value="Duration: N/A")

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Load File Button
        load_button = tk.Button(self.root, text="Load Audio File", command=self.load_audio)
        load_button.pack(pady=10)

        # Display File Name
        self.file_label = tk.Label(self.root, textvariable=self.file_name)
        self.file_label.pack(pady=5)

        # Display Duration
        self.duration_label = tk.Label(self.root, textvariable=self.duration)
        self.duration_label.pack(pady=5)

        # Combine Plots Button
        combine_button = tk.Button(self.root, text="Combine Plots", command=self.combine_plots)
        combine_button.pack(pady=10)

        # Export Button
        export_button = tk.Button(self.root, text="Export Plot", command=self.export_plot)
        export_button.pack(pady=10)

    def load_audio(self):
        return

    def combine_plots(self):
        return

    def export_plot(self):
        return

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioApp(root)
    root.mainloop()