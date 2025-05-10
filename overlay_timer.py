import tkinter as tk
import time

class OverlayTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay Timer")
        self.root.attributes('-topmost', True)  # Keep on top
        self.root.configure(bg='black')
        self.root.overrideredirect(True)  # Remove window borders
        
        self.start_time = time.time()
        self.running = True
        self.pause_time = 0
        self.locked = False
        self.offset_x = 0
        self.offset_y = 0
        
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack()
        
        self.label = tk.Label(self.frame, font=("Courier", 20), fg='lime', bg='black')
        self.label.pack(padx=10, pady=5, side=tk.LEFT)
        
        self.lock_button = tk.Button(self.frame, text="🔒", font=("Courier", 12), bg='black', fg='red', borderwidth=0, command=self.toggle_lock)
        self.lock_button.pack(side=tk.RIGHT, padx=5)

        self.reset_button = tk.Button(self.frame, text="R", font=("Courier", 12), bg='black', fg='white', borderwidth=0, command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=5)
        
        self.root.bind("<Button-1>", self.start_move)  # Start moving
        self.root.bind("<B1-Motion>", self.do_move)  # Moving motion
        self.root.bind("<ButtonRelease-1>", self.stop_move)  # Stop moving
        
        self.root.bind("<Button-2>", self.reset_timer)  
 
        self.label.bind("<Double-Button-1>", self.toggle_pause)  # Double click to pause/resume
        self.label.bind("<Triple-Button-1>", self.close_timer)  # Triple click to close
        
        self.update_timer()
        self.root.geometry("250x50+1+25")  # Small size, positioned at top-left
        self.root.mainloop()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
        else:
            elapsed = self.pause_time
        
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        self.label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.root.after(8, self.update_timer)  

    def toggle_pause(self, event):
        if self.running:
            self.pause_time = time.time() - self.start_time
            self.running = False
        else:
            self.start_time = time.time() - self.pause_time
            self.running = True

    def close_timer(self, event):
        self.root.destroy()
    
    def toggle_lock(self):
        self.locked = not self.locked
        self.lock_button.config(fg='green' if self.locked else 'red')
    
    def start_move(self, event):
        if not self.locked:
            self.offset_x = event.x_root - self.root.winfo_x()
            self.offset_y = event.y_root - self.root.winfo_y()
    
    def do_move(self, event):
        if not self.locked:
            x = event.x_root - self.offset_x
            y = event.y_root - self.offset_y
            self.root.geometry(f"+{x}+{y}")
    
    def stop_move(self, event):
        pass
    
    def reset_timer(self):
        self.start_time = time.time()  # Restart the timer
        self.running = True

if __name__ == "__main__":
    OverlayTimer()
