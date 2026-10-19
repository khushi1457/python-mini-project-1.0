"""
Climate-Smart Agricultural Loan & Insurance Decision System
Main Desktop Application Launcher
"""

import sys
import os
import tkinter as tk
from gui import AgriFinanceApp


def main():
    """
    Main entrypoint for launching the Agri-Finance Desktop Application.
    Supports '--test' or '--headless-check' for automated CI/terminal verification.
    """
    is_headless_test = "--test" in sys.argv or "--headless-check" in sys.argv

    root = tk.Tk()

    if is_headless_test:
        # In test mode, hide window and verify instantiation
        root.withdraw()
        app = AgriFinanceApp(root)
        print("[SUCCESS] AGRO-SHIELD AI Desktop application successfully initialized in test mode.")
        print(f"Loaded {len(app.current_farmers_map)} initial farmer profiles.")
        root.destroy()
        sys.exit(0)
    else:
        app = AgriFinanceApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()
