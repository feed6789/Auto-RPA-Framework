# app_ui.py
import customtkinter as ctk
import threading
from main import AutomationBot

class BotUI(ctk.CTk):
    def __init__(self, bot_instance):
        super().__init__()
        self.bot = bot_instance

        # --- Window Configuration ---
        self.title("Automation Bot Control Panel")
        self.geometry("550x450")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Widgets ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self.main_frame, text="Bot Controls", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 20))

        # Control Buttons
        self.start_button = ctk.CTkButton(self.main_frame, text="Start (F9)", command=self.start_bot_ui, fg_color="green", hover_color="#006400")
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self.main_frame, text="Pause (F10)", command=self.stop_bot_ui, state="disabled", fg_color="orange", hover_color="#FF4500")
        self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.exit_button = ctk.CTkButton(self.main_frame, text="Exit (ESC)", command=self.exit_bot_ui, fg_color="darkred", hover_color="#B22222")
        self.exit_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # --- Status Log ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(self.log_frame, state="disabled", wrap="word", font=("Arial", 12))
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def log(self, message):
        """Adds a message to the UI log."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end") # Auto-scroll to the bottom
        self.log_textbox.configure(state="disabled")

    def start_bot_ui(self):
        """UI function to start the bot."""
        self.start_button.configure(state="disabled", text="Running...")
        self.stop_button.configure(state="normal")
        self.bot.start_bot()

    def stop_bot_ui(self):
        """UI function to pause the bot."""
        self.start_button.configure(state="normal", text="Start (F9)")
        self.stop_button.configure(state="disabled")
        self.bot.stop_bot()

    def exit_bot_ui(self):
        """UI function to exit the application."""
        self.bot.exit_bot()
        self.after(500, self.destroy) # Wait a moment for the thread to close

    def update_ui_from_hotkey(self, event):
        """Listen for state changes from the bot (triggered by hotkeys)."""
        if self.bot.is_running and self.start_button.cget("state") == "normal":
            self.start_bot_ui()
        elif not self.bot.is_running and self.stop_button.cget("state") == "normal":
            self.stop_bot_ui()
        
        # Schedule the next check
        self.after(100, self.update_ui_from_hotkey, None)

if __name__ == "__main__":
    # 1. Create the bot instance
    bot = AutomationBot()

    # 2. Create the UI and pass the bot instance to it
    app = BotUI(bot_instance=bot)

    # 3. Create a custom print function that redirects output to the UI log
    def ui_print(message):
        print(message) # Also print to console for debugging
        app.log(message)

    # 4. Replace the bot's print function with our new UI-aware function
    bot.print = ui_print
    
    # 5. Setup hotkeys and start the bot's main loop in a background thread
    bot.setup_hotkeys()
    bot_thread = threading.Thread(target=bot.main_loop, daemon=True)
    bot_thread.start()

    # 6. Start the UI event loop
    app.after(100, app.update_ui_from_hotkey, None) # Start checking for hotkey state changes
    app.mainloop()