"""
Desktop Graphical User Interface (Tkinter / ttk)
Climate-Smart Agricultural Loan & Insurance Decision System
Palette: Warm Earthy Beige, Walnut Brown, and Light Botanical Sage Green
Currency: Indian Rupees (₹)
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional, Dict, Any, List

from db_manager import DatabaseManager
from risk_engine import AgriRiskEngine


class AgriFinanceApp:
    """
    Main Tkinter Desktop Application for Climate-Smart Agricultural Finance & Insurance.
    Designed with a warm earthy aesthetic (Beige, Brown & Light Sage Green) and Rupee (₹) denomination.
    """

    # UI Theme Palette: Warm Earthy Beige, Walnut Brown & Light Sage Green
    COLOR_BG_MAIN = "#F5F2EB"        # Soft Warm Linen / Sand Beige background
    COLOR_SURFACE = "#FCFBF8"        # Warm Off-White / Parchment card surface
    COLOR_SURFACE_ALT = "#EFEAE0"    # Soft Oat / Cream sub-container
    COLOR_PRIMARY = "#5A3E2B"        # Rich Warm Earth Brown / Saddle Brown
    COLOR_PRIMARY_DARK = "#352317"   # Deep Espresso Walnut Brown (Header)
    COLOR_ACCENT = "#5E8B64"         # Light Botanical Sage / Field Green
    COLOR_ACCENT_HOVER = "#49704E"   # Deep Sage Green hover
    COLOR_BROWN_BTN = "#6E4F39"      # Warm Chestnut Brown button
    COLOR_BROWN_HOVER = "#553B28"    # Deep Earth Brown hover
    COLOR_DANGER = "#B84232"         # Warm Terracotta Clay Red
    COLOR_WARNING = "#C28322"        # Harvest Golden Ochre
    COLOR_TEXT_MAIN = "#2A211B"      # Deep Coffee / Charcoal Brown text
    COLOR_TEXT_MUTED = "#786C60"     # Warm Muted Stone / Taupe text
    COLOR_BORDER = "#DDD7C8"         # Gentle Warm Sand border

    # Risk Color Tokens (Natural botanical harmony)
    COLOR_RISK_LOW = "#3B7547"       # Lush Leaf / Sage Green
    COLOR_RISK_LOW_BG = "#E8F3EA"    # Very Soft Light Sage Mint
    COLOR_RISK_MED = "#B87A1E"       # Harvest Gold / Ochre
    COLOR_RISK_MED_BG = "#FAF2E3"    # Warm Wheat / Pale Butter
    COLOR_RISK_HIGH = "#B84232"      # Terracotta Clay Red
    COLOR_RISK_HIGH_BG = "#FAECE8"   # Pale Terracotta Mist

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AGRO-SHIELD AI | Climate-Smart Agricultural Loan & Insurance Decision System")
        self.root.geometry("1240x800")
        self.root.minsize(1050, 680)

        # Set window background
        self.root.configure(bg=self.COLOR_BG_MAIN)

        # Initialize Backend Components
        self.db = DatabaseManager()
        self.risk_engine = AgriRiskEngine()

        # State Variables
        self.selected_farmer_id: Optional[int] = None
        self.current_farmers_map: Dict[int, Dict[str, Any]] = {}
        self.selected_ledger_claim_id: Optional[int] = None
        self.selected_ledger_assessment_id: Optional[int] = None

        # Build UI Components
        self._setup_styles()
        self._build_header()
        self._build_notebook_tabs()
        self._build_status_bar()

        # Initial Data Load
        self.refresh_farmers_table()
        self.refresh_farmer_combobox()
        self.refresh_ledger_and_kpis()

    def _setup_styles(self) -> None:
        """Configure ttk theme and custom widget styles for Beige/Brown/Sage palette."""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Configure Notebook
        self.style.configure(
            "TNotebook",
            background=self.COLOR_BG_MAIN,
            borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab",
            font=("Helvetica", 11, "bold"),
            padding=(18, 9),
            background="#E8E2D5",
            foreground=self.COLOR_TEXT_MUTED
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.COLOR_SURFACE)],
            foreground=[("selected", self.COLOR_PRIMARY_DARK)]
        )

        # Configure Treeviews
        self.style.configure(
            "Treeview",
            font=("Helvetica", 10),
            rowheight=28,
            background=self.COLOR_SURFACE,
            fieldbackground=self.COLOR_SURFACE,
            foreground=self.COLOR_TEXT_MAIN,
            borderwidth=1
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Helvetica", 10, "bold"),
            background="#EAE4D7",
            foreground=self.COLOR_PRIMARY_DARK,
            relief="flat"
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#E2ECE3")],
            foreground=[("selected", "#1E3E26")]
        )

        # Configure Primary Buttons (Sage Green Accent)
        self.style.configure(
            "Accent.TButton",
            font=("Helvetica", 10, "bold"),
            background=self.COLOR_ACCENT,
            foreground="white",
            padding=(12, 6)
        )
        self.style.map("Accent.TButton", background=[("active", self.COLOR_ACCENT_HOVER)])

        # Configure Earthy Brown Primary Button
        self.style.configure(
            "Primary.TButton",
            font=("Helvetica", 10, "bold"),
            background=self.COLOR_PRIMARY,
            foreground="white",
            padding=(12, 6)
        )
        self.style.map("Primary.TButton", background=[("active", self.COLOR_BROWN_HOVER)])

        # Terracotta Danger Button
        self.style.configure(
            "Danger.TButton",
            font=("Helvetica", 10, "bold"),
            background=self.COLOR_DANGER,
            foreground="white",
            padding=(10, 5)
        )
        self.style.map("Danger.TButton", background=[("active", "#9B3325")])

        # Muted Warm Beige Button
        self.style.configure(
            "Muted.TButton",
            font=("Helvetica", 10),
            background="#EAE4D7",
            foreground=self.COLOR_PRIMARY_DARK,
            padding=(10, 5)
        )
        self.style.map("Muted.TButton", background=[("active", "#DDD5C4")])

    def _build_header(self) -> None:
        """Top Application Brand & Status Header in Deep Warm Espresso."""
        header_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY_DARK, height=72)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_container = tk.Frame(header_frame, bg=self.COLOR_PRIMARY_DARK)
        title_container.pack(side=tk.LEFT, padx=22, pady=10)

        app_title = tk.Label(
            title_container,
            text="AGRO-SHIELD AI  |  Climate-Smart Loan & Insurance Decision System",
            font=("Helvetica", 16, "bold"),
            fg="#FDFBF7",
            bg=self.COLOR_PRIMARY_DARK
        )
        app_title.pack(anchor="w")

        app_subtitle = tk.Label(
            title_container,
            text="Autonomous Agricultural Heatwave Analytics • Parametric Microfinance (₹) • Dynamic Risk Adjustment",
            font=("Helvetica", 9),
            fg="#D6C9BC",
            bg=self.COLOR_PRIMARY_DARK
        )
        app_subtitle.pack(anchor="w")

        # Badges on right
        badge_container = tk.Frame(header_frame, bg=self.COLOR_PRIMARY_DARK)
        badge_container.pack(side=tk.RIGHT, padx=20, pady=14)

        ml_acc = self.risk_engine.model_metrics.get("test_accuracy", 94.5)
        ml_badge = tk.Label(
            badge_container,
            text=f"🤖 ML Engine: Active ({ml_acc}% Acc)",
            font=("Helvetica", 9, "bold"),
            bg="#243F29",
            fg="#A7E4B0",
            padx=10,
            pady=4,
            relief="flat"
        )
        ml_badge.pack(side=tk.LEFT, padx=6)

        db_badge = tk.Label(
            badge_container,
            text="🗄️ SQLite: Connected (₹)",
            font=("Helvetica", 9, "bold"),
            bg="#4A3525",
            fg="#E9D6BF",
            padx=10,
            pady=4,
            relief="flat"
        )
        db_badge.pack(side=tk.LEFT, padx=6)

    def _build_notebook_tabs(self) -> None:
        """Constructs Tabbed UI."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=14, pady=(10, 5))

        self.tab_farmers = ttk.Frame(self.notebook)
        self.tab_assessment = ttk.Frame(self.notebook)
        self.tab_ledger = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_farmers, text="  🌾 Farmer Profile Manager  ")
        self.notebook.add(self.tab_assessment, text="  🌡️ Climate Risk & Insurance Engine  ")
        self.notebook.add(self.tab_ledger, text="  📊 Financial Ledger & Claims Center  ")

        self._init_tab_farmers()
        self._init_tab_assessment()
        self._init_tab_ledger()

    def _build_status_bar(self) -> None:
        """Bottom status bar with warm beige/sand styling."""
        self.status_bar = tk.Frame(self.root, bg="#EAE4D7", height=24)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            self.status_bar,
            text="System Ready. Climate risk engine initialized with Rupee (₹) financial logic.",
            font=("Helvetica", 9),
            bg="#EAE4D7",
            fg=self.COLOR_TEXT_MUTED
        )
        self.status_label.pack(side=tk.LEFT, padx=14, pady=2)

        self.timestamp_label = tk.Label(
            self.status_bar,
            text=datetime.now().strftime("%Y-%m-%d %H:%M"),
            font=("Helvetica", 9),
            bg="#EAE4D7",
            fg=self.COLOR_TEXT_MUTED
        )
        self.timestamp_label.pack(side=tk.RIGHT, padx=14, pady=2)

    def set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    # =========================================================================
    # TAB 1: FARMER PROFILE MANAGER
    # =========================================================================
    def _init_tab_farmers(self) -> None:
        container = tk.Frame(self.tab_farmers, bg=self.COLOR_BG_MAIN)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Left Column: Registration & Update Form
        form_card = tk.LabelFrame(
            container,
            text=" Farmer Profile Details ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=16,
            pady=14
        )
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.f_name_var = tk.StringVar()
        self.f_region_var = tk.StringVar()
        self.f_crop_var = tk.StringVar()
        self.f_size_var = tk.StringVar()
        self.f_loan_var = tk.StringVar()
        self.f_rate_var = tk.StringVar()
        self.f_credit_var = tk.StringVar()

        fields = [
            ("Full Name:", self.f_name_var),
            ("Region / District:", self.f_region_var),
            ("Crop Type:", self.f_crop_var),
            ("Farm Size (Acres):", self.f_size_var),
            ("Loan Amount (₹):", self.f_loan_var),
            ("Base Interest Rate (%):", self.f_rate_var),
            ("Credit Score (300-900):", self.f_credit_var)
        ]

        for i, (label_text, var) in enumerate(fields):
            lbl = tk.Label(form_card, text=label_text, font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN)
            lbl.grid(row=i*2, column=0, sticky="w", pady=(6, 1))

            if label_text.startswith("Region"):
                entry = ttk.Combobox(
                    form_card,
                    textvariable=var,
                    width=28,
                    values=[
                        "Vidarbha, Maharashtra", "Ludhiana, Punjab", "Bikaner, Rajasthan",
                        "Indore, Madhya Pradesh", "Varanasi, Uttar Pradesh", "Palakkad, Kerala",
                        "Burdwan, West Bengal", "Anand, Gujarat", "Dharwad, Karnataka", "Guntur, Andhra Pradesh"
                    ]
                )
            elif label_text.startswith("Crop"):
                entry = ttk.Combobox(
                    form_card,
                    textvariable=var,
                    width=28,
                    values=["Cotton", "Wheat", "Rice (Paddy)", "Bajra (Millet)", "Soybean", "Maize", "Groundnut", "Sugarcane", "Mustard", "Spices / Pepper"]
                )
            else:
                entry = ttk.Entry(form_card, textvariable=var, width=30)

            entry.grid(row=i*2+1, column=0, sticky="w", pady=(0, 4))

        self.lbl_selected_farmer = tk.Label(
            form_card,
            text="Mode: New Registration",
            font=("Helvetica", 9, "italic"),
            fg=self.COLOR_ACCENT,
            bg=self.COLOR_SURFACE
        )
        self.lbl_selected_farmer.grid(row=len(fields)*2, column=0, sticky="w", pady=(10, 4))

        btn_frame = tk.Frame(form_card, bg=self.COLOR_SURFACE)
        btn_frame.grid(row=len(fields)*2 + 1, column=0, sticky="we", pady=(8, 4))

        self.btn_add_farmer = ttk.Button(btn_frame, text="➕ Add Farmer", style="Accent.TButton", command=self.handle_add_farmer)
        self.btn_add_farmer.pack(fill=tk.X, pady=3)

        self.btn_update_farmer = ttk.Button(btn_frame, text="✏️ Update Farmer", style="Primary.TButton", command=self.handle_update_farmer)
        self.btn_update_farmer.pack(fill=tk.X, pady=3)

        row_sub_btns = tk.Frame(btn_frame, bg=self.COLOR_SURFACE)
        row_sub_btns.pack(fill=tk.X, pady=3)

        self.btn_clear_farmer = ttk.Button(row_sub_btns, text="🔄 Clear Form", style="Muted.TButton", command=self.clear_farmer_form)
        self.btn_clear_farmer.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))

        self.btn_delete_farmer = ttk.Button(row_sub_btns, text="🗑️ Delete", style="Danger.TButton", command=self.handle_delete_farmer)
        self.btn_delete_farmer.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))

        # Right Column: Search bar and Farmers Table
        table_card = tk.LabelFrame(
            container,
            text=" Registered Farmers Database ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=14,
            pady=12
        )
        table_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        filter_bar = tk.Frame(table_card, bg=self.COLOR_SURFACE)
        filter_bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(filter_bar, text="Search Name/Crop:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 6))
        self.farmer_search_var = tk.StringVar()
        entry_search = ttk.Entry(filter_bar, textvariable=self.farmer_search_var, width=18)
        entry_search.pack(side=tk.LEFT, padx=(0, 10))
        entry_search.bind("<Return>", lambda e: self.refresh_farmers_table())

        tk.Label(filter_bar, text="Region:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 6))
        self.farmer_region_filter_var = tk.StringVar(value="All Regions")
        combo_reg_filter = ttk.Combobox(
            filter_bar,
            textvariable=self.farmer_region_filter_var,
            width=16,
            values=["All Regions", "Maharashtra", "Punjab", "Rajasthan", "Madhya Pradesh", "Uttar Pradesh", "Kerala", "West Bengal", "Gujarat"]
        )
        combo_reg_filter.pack(side=tk.LEFT, padx=(0, 10))
        combo_reg_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_farmers_table())

        ttk.Button(filter_bar, text="🔍 Search", style="Primary.TButton", command=self.refresh_farmers_table).pack(side=tk.LEFT, padx=4)
        ttk.Button(filter_bar, text="Reset", style="Muted.TButton", command=self._reset_farmer_filters).pack(side=tk.LEFT, padx=4)

        self.lbl_farmer_count = tk.Label(filter_bar, text="Total: 0", font=("Helvetica", 9, "bold"), fg=self.COLOR_PRIMARY, bg=self.COLOR_SURFACE)
        self.lbl_farmer_count.pack(side=tk.RIGHT, padx=6)

        tree_scroll_y = ttk.Scrollbar(table_card, orient=tk.VERTICAL)
        tree_scroll_x = ttk.Scrollbar(table_card, orient=tk.HORIZONTAL)

        columns = ("id", "name", "region", "crop", "acres", "loan", "rate", "credit")
        self.farmer_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.farmer_tree.yview)
        tree_scroll_x.config(command=self.farmer_tree.xview)

        self.farmer_tree.heading("id", text="ID")
        self.farmer_tree.heading("name", text="Farmer Name")
        self.farmer_tree.heading("region", text="Region")
        self.farmer_tree.heading("crop", text="Crop Type")
        self.farmer_tree.heading("acres", text="Acres")
        self.farmer_tree.heading("loan", text="Loan Amount (₹)")
        self.farmer_tree.heading("rate", text="Base Rate (%)")
        self.farmer_tree.heading("credit", text="Credit Score")

        self.farmer_tree.column("id", width=45, anchor="center")
        self.farmer_tree.column("name", width=130, anchor="w")
        self.farmer_tree.column("region", width=145, anchor="w")
        self.farmer_tree.column("crop", width=100, anchor="w")
        self.farmer_tree.column("acres", width=65, anchor="e")
        self.farmer_tree.column("loan", width=115, anchor="e")
        self.farmer_tree.column("rate", width=90, anchor="e")
        self.farmer_tree.column("credit", width=85, anchor="center")

        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.farmer_tree.pack(fill=tk.BOTH, expand=True)

        self.farmer_tree.bind("<<TreeviewSelect>>", self._on_farmer_selected)

    def _reset_farmer_filters(self) -> None:
        self.farmer_search_var.set("")
        self.farmer_region_filter_var.set("All Regions")
        self.refresh_farmers_table()

    def refresh_farmers_table(self) -> None:
        search = self.farmer_search_var.get().strip()
        reg_filter = self.farmer_region_filter_var.get().strip()

        for row in self.farmer_tree.get_children():
            self.farmer_tree.delete(row)

        farmers = self.db.get_all_farmers(search_query=search, region_filter=reg_filter)
        self.current_farmers_map = {f["farmer_id"]: f for f in farmers}

        for f in farmers:
            self.farmer_tree.insert(
                "",
                tk.END,
                values=(
                    f["farmer_id"],
                    f["name"],
                    f["region"],
                    f["crop_type"],
                    f"{f['farm_size_acres']:.1f}",
                    f"₹{f['loan_amount']:,.2f}",
                    f"{f['interest_rate']:.2f}%",
                    f["credit_score"]
                )
            )

        self.lbl_farmer_count.config(text=f"Total: {len(farmers)} Farmers")
        self.set_status(f"Loaded {len(farmers)} registered farmers.")

    def _on_farmer_selected(self, event) -> None:
        selected_items = self.farmer_tree.selection()
        if not selected_items:
            return

        values = self.farmer_tree.item(selected_items[0])["values"]
        if not values:
            return

        farmer_id = int(values[0])
        farmer = self.db.get_farmer(farmer_id)
        if not farmer:
            return

        self.selected_farmer_id = farmer_id
        self.f_name_var.set(farmer["name"])
        self.f_region_var.set(farmer["region"])
        self.f_crop_var.set(farmer["crop_type"])
        self.f_size_var.set(str(farmer["farm_size_acres"]))
        self.f_loan_var.set(str(farmer["loan_amount"]))
        self.f_rate_var.set(str(farmer["interest_rate"]))
        self.f_credit_var.set(str(farmer["credit_score"]))

        self.lbl_selected_farmer.config(
            text=f"Selected Farmer ID: #{farmer_id} (Ready to Edit or Delete)",
            fg=self.COLOR_PRIMARY
        )

    def clear_farmer_form(self) -> None:
        self.selected_farmer_id = None
        self.f_name_var.set("")
        self.f_region_var.set("")
        self.f_crop_var.set("")
        self.f_size_var.set("")
        self.f_loan_var.set("")
        self.f_rate_var.set("")
        self.f_credit_var.set("")
        self.lbl_selected_farmer.config(
            text="Mode: New Registration",
            fg=self.COLOR_ACCENT
        )
        if self.farmer_tree.selection():
            self.farmer_tree.selection_remove(self.farmer_tree.selection())

    def _validate_farmer_inputs(self) -> Optional[Dict[str, Any]]:
        name = self.f_name_var.get().strip()
        region = self.f_region_var.get().strip()
        crop = self.f_crop_var.get().strip()

        if not name:
            messagebox.showerror("Validation Error", "Please provide the Farmer's Full Name.")
            return None
        if not region:
            messagebox.showerror("Validation Error", "Please provide or select a Region.")
            return None
        if not crop:
            messagebox.showerror("Validation Error", "Please specify the Crop Type.")
            return None

        try:
            acres = float(self.f_size_var.get().strip())
            if acres <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Farm Size (Acres) must be a positive number.")
            return None

        try:
            loan = float(self.f_loan_var.get().strip())
            if loan < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Loan Amount (₹) must be a non-negative number.")
            return None

        try:
            rate = float(self.f_rate_var.get().strip())
            if rate < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Base Interest Rate (%) must be non-negative.")
            return None

        try:
            credit = int(self.f_credit_var.get().strip())
            if not (300 <= credit <= 900):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Credit Score must be an integer between 300 and 900.")
            return None

        return {
            "name": name,
            "region": region,
            "crop_type": crop,
            "farm_size_acres": acres,
            "loan_amount": loan,
            "interest_rate": rate,
            "credit_score": credit
        }

    def handle_add_farmer(self) -> None:
        data = self._validate_farmer_inputs()
        if not data:
            return

        try:
            new_id = self.db.add_farmer(**data)
            messagebox.showinfo("Success", f"Farmer '{data['name']}' registered successfully with ID #{new_id}!")
            self.clear_farmer_form()
            self.refresh_farmers_table()
            self.refresh_farmer_combobox()
            self.refresh_ledger_and_kpis()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add farmer: {str(e)}")

    def handle_update_farmer(self) -> None:
        if not self.selected_farmer_id:
            messagebox.showwarning("Notice", "Please select a farmer from the table to update.")
            return

        data = self._validate_farmer_inputs()
        if not data:
            return

        try:
            success = self.db.update_farmer(farmer_id=self.selected_farmer_id, **data)
            if success:
                messagebox.showinfo("Success", f"Farmer #{self.selected_farmer_id} updated successfully!")
                self.clear_farmer_form()
                self.refresh_farmers_table()
                self.refresh_farmer_combobox()
                self.refresh_ledger_and_kpis()
            else:
                messagebox.showerror("Error", "Farmer update failed: Record not found.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update farmer: {str(e)}")

    def handle_delete_farmer(self) -> None:
        if not self.selected_farmer_id:
            messagebox.showwarning("Notice", "Please select a farmer from the table to delete.")
            return

        farmer = self.db.get_farmer(self.selected_farmer_id)
        name = farmer["name"] if farmer else f"#{self.selected_farmer_id}"

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete farmer '{name}' (ID: {self.selected_farmer_id})?\n\n"
            "This will also delete associated risk assessments and payout claims.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.db.delete_farmer(self.selected_farmer_id)
            messagebox.showinfo("Deleted", f"Farmer record #{self.selected_farmer_id} removed.")
            self.clear_farmer_form()
            self.refresh_farmers_table()
            self.refresh_farmer_combobox()
            self.refresh_ledger_and_kpis()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete farmer: {str(e)}")

    # =========================================================================
    # TAB 2: CLIMATE RISK & INSURANCE ENGINE
    # =========================================================================
    def _init_tab_assessment(self) -> None:
        main_frame = tk.Frame(self.tab_assessment, bg=self.COLOR_BG_MAIN)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        top_grid = tk.Frame(main_frame, bg=self.COLOR_BG_MAIN)
        top_grid.pack(fill=tk.X, pady=(0, 10))

        # Card 1: Farmer Selection
        farmer_card = tk.LabelFrame(
            top_grid,
            text=" 1. Select Farmer for Underwriting ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=16,
            pady=12
        )
        farmer_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        tk.Label(farmer_card, text="Choose Registered Farmer Profile:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 4))

        self.assess_farmer_combobox_var = tk.StringVar()
        self.assess_farmer_combo = ttk.Combobox(
            farmer_card,
            textvariable=self.assess_farmer_combobox_var,
            state="readonly",
            width=45
        )
        self.assess_farmer_combo.pack(fill=tk.X, pady=(0, 10))
        self.assess_farmer_combo.bind("<<ComboboxSelected>>", self._on_assess_farmer_selected)

        # Warm Cream Preview Box
        self.farmer_meta_frame = tk.Frame(farmer_card, bg="#F6F2E9", highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=12, pady=10)
        self.farmer_meta_frame.pack(fill=tk.BOTH, expand=True)

        self.meta_labels: Dict[str, tk.Label] = {}
        meta_keys = [
            ("Farmer Name:", "None Selected"),
            ("Region / Location:", "-"),
            ("Crop & Acreage:", "-"),
            ("Active Loan (₹):", "₹0.00"),
            ("Base Interest Rate:", "0.0%"),
            ("Credit Score:", "-")
        ]

        for i, (k, val) in enumerate(meta_keys):
            lbl_k = tk.Label(self.farmer_meta_frame, text=k, font=("Helvetica", 9, "bold"), bg="#F6F2E9", fg=self.COLOR_TEXT_MUTED)
            lbl_k.grid(row=i, column=0, sticky="w", pady=2)
            lbl_v = tk.Label(self.farmer_meta_frame, text=val, font=("Helvetica", 9), bg="#F6F2E9", fg=self.COLOR_TEXT_MAIN)
            lbl_v.grid(row=i, column=1, sticky="w", padx=10, pady=2)
            self.meta_labels[k] = lbl_v

        # Card 2: Climate & Meteorological Inputs
        weather_card = tk.LabelFrame(
            top_grid,
            text=" 2. Meteorological & Thermal Intelligence Inputs ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=16,
            pady=12
        )
        weather_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        w_grid = tk.Frame(weather_card, bg=self.COLOR_SURFACE)
        w_grid.pack(fill=tk.X)

        self.w_obs_temp_var = tk.StringVar(value="38.5")
        self.w_fcst_temp_var = tk.StringVar(value="41.0")
        self.w_humidity_var = tk.StringVar(value="32.0")
        self.w_season_var = tk.StringVar(value="Summer")

        tk.Label(w_grid, text="Observed Max Temp (°C):", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(w_grid, textvariable=self.w_obs_temp_var, width=16).grid(row=0, column=1, sticky="w", padx=8, pady=4)

        tk.Label(w_grid, text="Forecast Max Temp (°C):", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).grid(row=0, column=2, sticky="w", padx=(10, 0), pady=4)
        ttk.Entry(w_grid, textvariable=self.w_fcst_temp_var, width=16).grid(row=0, column=3, sticky="w", padx=8, pady=4)

        tk.Label(w_grid, text="Relative Humidity (%):", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(w_grid, textvariable=self.w_humidity_var, width=16).grid(row=1, column=1, sticky="w", padx=8, pady=4)

        tk.Label(w_grid, text="Crop Season:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).grid(row=1, column=2, sticky="w", padx=(10, 0), pady=4)
        season_combo = ttk.Combobox(w_grid, textvariable=self.w_season_var, state="readonly", width=14, values=["Kharif", "Rabi", "Summer"])
        season_combo.grid(row=1, column=3, sticky="w", padx=8, pady=4)

        preset_frame = tk.Frame(weather_card, bg=self.COLOR_SURFACE)
        preset_frame.pack(fill=tk.X, pady=(10, 8))

        tk.Label(preset_frame, text="⚡ Climate Simulation Presets:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 4))

        p_btns = tk.Frame(preset_frame, bg=self.COLOR_SURFACE)
        p_btns.pack(fill=tk.X)

        ttk.Button(p_btns, text="🔥 Heatwave Spike (43°C, Summer)", style="Muted.TButton", command=lambda: self._apply_weather_preset(42.5, 44.5, 22.0, "Summer")).pack(side=tk.LEFT, padx=3)
        ttk.Button(p_btns, text="⛅ Moderate Stress (35°C, Kharif)", style="Muted.TButton", command=lambda: self._apply_weather_preset(34.8, 36.2, 72.0, "Kharif")).pack(side=tk.LEFT, padx=3)
        ttk.Button(p_btns, text="🌱 Optimal Climate (26°C, Rabi)", style="Muted.TButton", command=lambda: self._apply_weather_preset(25.0, 26.5, 60.0, "Rabi")).pack(side=tk.LEFT, padx=3)

        self.btn_run_assessment = ttk.Button(
            weather_card,
            text="🚀  RUN AI RISK ASSESSMENT & COMPUTE PAYOUT (₹)",
            style="Accent.TButton",
            command=self.handle_run_assessment
        )
        self.btn_run_assessment.pack(fill=tk.X, pady=(6, 0))

        # Bottom Section: Results & Financial Decision Card
        self.results_card = tk.LabelFrame(
            main_frame,
            text=" 3. Real-Time AI Risk Classification & Parametric Financial Decision ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=18,
            pady=14
        )
        self.results_card.pack(fill=tk.BOTH, expand=True)

        self.risk_banner_frame = tk.Frame(self.results_card, bg="#F3EFE5", relief="flat", padx=16, pady=10)
        self.risk_banner_frame.pack(fill=tk.X, pady=(0, 10))

        self.lbl_risk_badge = tk.Label(
            self.risk_banner_frame,
            text="AWAITING ASSESSMENT — Select a farmer and click 'Run AI Risk Assessment'",
            font=("Helvetica", 13, "bold"),
            fg=self.COLOR_TEXT_MUTED,
            bg="#F3EFE5"
        )
        self.lbl_risk_badge.pack(side=tk.LEFT)

        self.lbl_risk_confidence = tk.Label(self.risk_banner_frame, text="", font=("Helvetica", 10), fg=self.COLOR_TEXT_MUTED, bg="#F3EFE5")
        self.lbl_risk_confidence.pack(side=tk.RIGHT)

        # 4 KPI Summary Cards Grid
        kpi_grid = tk.Frame(self.results_card, bg=self.COLOR_SURFACE)
        kpi_grid.pack(fill=tk.X, pady=6)
        kpi_grid.columnconfigure(0, weight=1)
        kpi_grid.columnconfigure(1, weight=1)
        kpi_grid.columnconfigure(2, weight=1)
        kpi_grid.columnconfigure(3, weight=1)

        c1 = tk.Frame(kpi_grid, bg="#FAF7F0", highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=12, pady=10)
        c1.grid(row=0, column=0, sticky="nsew", padx=4)
        tk.Label(c1, text="Calculated Insurance Payout (₹)", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0").pack(anchor="w")
        self.lbl_res_payout = tk.Label(c1, text="₹0.00", font=("Helvetica", 16, "bold"), fg=self.COLOR_PRIMARY, bg="#FAF7F0")
        self.lbl_res_payout.pack(anchor="w", pady=(4, 0))
        self.lbl_res_payout_pct = tk.Label(c1, text="0.0% of Active Loan", font=("Helvetica", 9), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0")
        self.lbl_res_payout_pct.pack(anchor="w")

        c2 = tk.Frame(kpi_grid, bg="#FAF7F0", highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=12, pady=10)
        c2.grid(row=0, column=1, sticky="nsew", padx=4)
        tk.Label(c2, text="Dynamic Adjusted Interest Rate", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0").pack(anchor="w")
        self.lbl_res_rate = tk.Label(c2, text="0.00%", font=("Helvetica", 16, "bold"), fg=self.COLOR_PRIMARY, bg="#FAF7F0")
        self.lbl_res_rate.pack(anchor="w", pady=(4, 0))
        self.lbl_res_rate_delta = tk.Label(c2, text="Base Rate + 0.0%", font=("Helvetica", 9), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0")
        self.lbl_res_rate_delta.pack(anchor="w")

        c3 = tk.Frame(kpi_grid, bg="#FAF7F0", highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=12, pady=10)
        c3.grid(row=0, column=2, sticky="nsew", padx=4)
        tk.Label(c3, text="ML Class Probabilities", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0").pack(anchor="w")
        self.lbl_res_probs = tk.Label(c3, text="Low: - | Med: - | High: -", font=("Helvetica", 11, "bold"), fg=self.COLOR_TEXT_MAIN, bg="#FAF7F0")
        self.lbl_res_probs.pack(anchor="w", pady=(8, 0))

        c4 = tk.Frame(kpi_grid, bg="#FAF7F0", highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=12, pady=10)
        c4.grid(row=0, column=3, sticky="nsew", padx=4)
        tk.Label(c4, text="Underwriting Action", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0").pack(anchor="w")
        self.lbl_res_action = tk.Label(c4, text="Standard", font=("Helvetica", 14, "bold"), fg=self.COLOR_TEXT_MAIN, bg="#FAF7F0")
        self.lbl_res_action.pack(anchor="w", pady=(4, 0))
        self.lbl_res_claim_status = tk.Label(c4, text="No active claim generated", font=("Helvetica", 9), fg=self.COLOR_TEXT_MUTED, bg="#FAF7F0")
        self.lbl_res_claim_status.pack(anchor="w")

        self.lbl_res_narrative = tk.Label(
            self.results_card,
            text="The Random Forest model evaluates meteorological conditions (observed and forecasted heatwave metrics) against crop vulnerability thresholds.",
            font=("Helvetica", 9, "italic"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_SURFACE,
            wraplength=1050,
            justify="left"
        )
        self.lbl_res_narrative.pack(anchor="w", pady=(8, 0))

    def _apply_weather_preset(self, obs_t: float, fcst_t: float, hum: float, season: str) -> None:
        self.w_obs_temp_var.set(str(obs_t))
        self.w_fcst_temp_var.set(str(fcst_t))
        self.w_humidity_var.set(str(hum))
        self.w_season_var.set(season)
        self.set_status(f"Applied preset: {season} ({obs_t}°C obs / {fcst_t}°C fcst).")

    def refresh_farmer_combobox(self) -> None:
        farmers = self.db.get_all_farmers()
        options = [
            f"ID #{f['farmer_id']} - {f['name']} ({f['crop_type']}, ₹{f['loan_amount']:,.2f})"
            for f in farmers
        ]
        self.assess_farmer_combo["values"] = options
        if options and not self.assess_farmer_combobox_var.get():
            self.assess_farmer_combo.current(0)
            self._on_assess_farmer_selected(None)

    def _on_assess_farmer_selected(self, event) -> None:
        val = self.assess_farmer_combobox_var.get()
        if not val or "ID #" not in val:
            return

        try:
            farmer_id_str = val.split("ID #")[1].split(" -")[0].strip()
            fid = int(farmer_id_str)
            farmer = self.db.get_farmer(fid)
            if not farmer:
                return

            self.meta_labels["Farmer Name:"].config(text=farmer["name"])
            self.meta_labels["Region / Location:"].config(text=farmer["region"])
            self.meta_labels["Crop & Acreage:"].config(text=f"{farmer['crop_type']} ({farmer['farm_size_acres']} Acres)")
            self.meta_labels["Active Loan (₹):"].config(text=f"₹{farmer['loan_amount']:,.2f}")
            self.meta_labels["Base Interest Rate:"].config(text=f"{farmer['interest_rate']:.2f}%")
            self.meta_labels["Credit Score:"].config(text=f"{farmer['credit_score']} / 900")
        except Exception as e:
            print("Error parsing farmer combobox:", e)

    def handle_run_assessment(self) -> None:
        val = self.assess_farmer_combobox_var.get()
        if not val or "ID #" not in val:
            messagebox.showwarning("Notice", "Please select a registered farmer first.")
            return

        farmer_id = int(val.split("ID #")[1].split(" -")[0].strip())
        farmer = self.db.get_farmer(farmer_id)
        if not farmer:
            messagebox.showerror("Error", "Farmer profile could not be retrieved from database.")
            return

        try:
            obs_temp = float(self.w_obs_temp_var.get().strip())
            fcst_temp = float(self.w_fcst_temp_var.get().strip())
            humidity = float(self.w_humidity_var.get().strip())
            season = self.w_season_var.get().strip()

            if not (10.0 <= obs_temp <= 55.0):
                raise ValueError("Observed Temperature must be between 10°C and 55°C.")
            if not (10.0 <= fcst_temp <= 58.0):
                raise ValueError("Forecast Temperature must be between 10°C and 58°C.")
            if not (5.0 <= humidity <= 100.0):
                raise ValueError("Relative Humidity must be between 5% and 100%.")
            if season not in ("Kharif", "Rabi", "Summer"):
                raise ValueError("Invalid season selected.")

        except ValueError as ve:
            messagebox.showerror("Invalid Weather Data", str(ve))
            return

        try:
            eval_result = self.risk_engine.evaluate_full_case(
                farmer_data=farmer,
                obs_temp=obs_temp,
                forecast_temp=fcst_temp,
                humidity=humidity,
                season=season
            )
        except Exception as ex:
            messagebox.showerror("ML Engine Failure", f"Risk evaluation failed: {str(ex)}")
            return

        risk_category = eval_result["risk_category"]
        payout = eval_result["calculated_payout"]
        payout_pct = eval_result["payout_percentage"]
        adj_rate = eval_result["adjusted_interest_rate"]
        rate_delta = eval_result["rate_delta"]
        conf = eval_result["confidence_percent"]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            asst_id = self.db.add_risk_assessment(
                farmer_id=farmer_id,
                obs_temp=obs_temp,
                predicted_temp=fcst_temp,
                season=season,
                risk_score=risk_category,
                calculated_payout=payout,
                adjusted_interest_rate=adj_rate,
                assessment_date=now_str
            )

            claim_id = None
            if payout > 0:
                claim_id = self.db.add_payout_claim(
                    farmer_id=farmer_id,
                    claim_amount=payout,
                    status="Pending",
                    assessment_id=asst_id,
                    created_at=now_str
                )

        except Exception as db_err:
            messagebox.showerror("Database Save Error", f"Failed to persist assessment: {str(db_err)}")
            return

        self._render_assessment_visuals(eval_result, claim_id)
        self.refresh_ledger_and_kpis()

        alert_msg = (
            f"Assessment Completed for {farmer['name']}!\n\n"
            f"• Risk Classification: {risk_category} ({conf}% confidence)\n"
            f"• Insurance Payout Triggered: ₹{payout:,.2f} ({payout_pct}% of loan)\n"
            f"• Adjusted Interest Rate: {adj_rate:.2f}% (delta: {rate_delta:+.1f}%)\n"
            f"• Assessment ID #{asst_id} logged to database."
        )
        if claim_id:
            alert_msg += f"\n• Payout Claim #{claim_id} created in 'Pending' status."

        messagebox.showinfo("Risk Assessment Complete", alert_msg)
        self.set_status(f"Assessment #{asst_id} recorded for {farmer['name']}: {risk_category}.")

    def _render_assessment_visuals(self, res: Dict[str, Any], claim_id: Optional[int]) -> None:
        risk = res["risk_category"]

        if "High" in risk:
            bg_col = self.COLOR_RISK_HIGH_BG
            fg_col = self.COLOR_RISK_HIGH
            badge_icon = "🔴 HIGH CLIMATE RISK ALERT"
            action_text = "Restructure / Payout"
        elif "Medium" in risk:
            bg_col = self.COLOR_RISK_MED_BG
            fg_col = self.COLOR_RISK_MED
            badge_icon = "🟡 MEDIUM CLIMATE STRESS"
            action_text = "Parametric Payout"
        else:
            bg_col = self.COLOR_RISK_LOW_BG
            fg_col = self.COLOR_RISK_LOW
            badge_icon = "🟢 LOW RISK (OPTIMAL CLIMATE)"
            action_text = "Standard / Discount"

        self.risk_banner_frame.config(bg=bg_col)
        self.lbl_risk_badge.config(
            text=f"{badge_icon} — {risk.upper()}",
            fg=fg_col,
            bg=bg_col
        )
        self.lbl_risk_confidence.config(
            text=f"AI Confidence: {res['confidence_percent']}%",
            fg=fg_col,
            bg=bg_col
        )

        self.lbl_res_payout.config(text=f"₹{res['calculated_payout']:,.2f}", fg=fg_col)
        self.lbl_res_payout_pct.config(text=f"{res['payout_percentage']}% of Loan (₹{res['loan_amount']:,.2f})")

        delta_sign = f"+{res['rate_delta']:.1f}%" if res['rate_delta'] >= 0 else f"{res['rate_delta']:.1f}%"
        self.lbl_res_rate.config(text=f"{res['adjusted_interest_rate']:.2f}%", fg=fg_col)
        self.lbl_res_rate_delta.config(text=f"Base {res['base_interest_rate']:.2f}% ({delta_sign})")

        p = res["probabilities"]
        self.lbl_res_probs.config(
            text=f"Low: {p.get('Low Risk', 0)}% | Med: {p.get('Medium Risk', 0)}% | High: {p.get('High Risk', 0)}%"
        )

        self.lbl_res_action.config(text=action_text, fg=fg_col)
        if claim_id:
            self.lbl_res_claim_status.config(text=f"Claim #{claim_id} Pending Approval", fg=self.COLOR_WARNING)
        else:
            self.lbl_res_claim_status.config(text="0% Payout (No Claim Needed)", fg=self.COLOR_ACCENT)

        self.lbl_res_narrative.config(
            text=f"Policy Rationale: {res['rate_rationale']} "
                 f"Weather profile evaluated: {res['meteorological_data']['season']} season with "
                 f"{res['meteorological_data']['obs_temp']}°C observed, {res['meteorological_data']['forecast_temp']}°C forecast, "
                 f"and {res['meteorological_data']['humidity']}% RH."
        )

    # =========================================================================
    # TAB 3: FINANCIAL LEDGER & CLAIMS CENTER
    # =========================================================================
    def _init_tab_ledger(self) -> None:
        container = tk.Frame(self.tab_ledger, bg=self.COLOR_BG_MAIN)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        # 1. Top KPI Summary Banner
        kpi_banner = tk.Frame(container, bg=self.COLOR_BG_MAIN)
        kpi_banner.pack(fill=tk.X, pady=(0, 10))
        kpi_banner.columnconfigure(0, weight=1)
        kpi_banner.columnconfigure(1, weight=1)
        kpi_banner.columnconfigure(2, weight=1)
        kpi_banner.columnconfigure(3, weight=1)

        k1 = tk.Frame(kpi_banner, bg=self.COLOR_SURFACE, highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=14, pady=10)
        k1.grid(row=0, column=0, sticky="nsew", padx=4)
        tk.Label(k1, text="Total Active Loans Portfolio (₹)", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_SURFACE).pack(anchor="w")
        self.lbl_kpi_total_loans = tk.Label(k1, text="₹0.00", font=("Helvetica", 16, "bold"), fg=self.COLOR_PRIMARY, bg=self.COLOR_SURFACE)
        self.lbl_kpi_total_loans.pack(anchor="w", pady=(2, 0))

        k2 = tk.Frame(kpi_banner, bg=self.COLOR_SURFACE, highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=14, pady=10)
        k2.grid(row=0, column=1, sticky="nsew", padx=4)
        tk.Label(k2, text="Total Estimated Payout Exposure (₹)", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_SURFACE).pack(anchor="w")
        self.lbl_kpi_payout_exposure = tk.Label(k2, text="₹0.00", font=("Helvetica", 16, "bold"), fg=self.COLOR_WARNING, bg=self.COLOR_SURFACE)
        self.lbl_kpi_payout_exposure.pack(anchor="w", pady=(2, 0))

        k3 = tk.Frame(kpi_banner, bg=self.COLOR_SURFACE, highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=14, pady=10)
        k3.grid(row=0, column=2, sticky="nsew", padx=4)
        tk.Label(k3, text="High Risk Farmers Count", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_SURFACE).pack(anchor="w")
        self.lbl_kpi_high_risk_count = tk.Label(k3, text="0", font=("Helvetica", 16, "bold"), fg=self.COLOR_DANGER, bg=self.COLOR_SURFACE)
        self.lbl_kpi_high_risk_count.pack(anchor="w", pady=(2, 0))

        k4 = tk.Frame(kpi_banner, bg=self.COLOR_SURFACE, highlightbackground=self.COLOR_BORDER, highlightthickness=1, padx=14, pady=10)
        k4.grid(row=0, column=3, sticky="nsew", padx=4)
        tk.Label(k4, text="Total Claims Disbursed (₹)", font=("Helvetica", 9, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_SURFACE).pack(anchor="w")
        self.lbl_kpi_disbursed = tk.Label(k4, text="₹0.00", font=("Helvetica", 16, "bold"), fg=self.COLOR_ACCENT, bg=self.COLOR_SURFACE)
        self.lbl_kpi_disbursed.pack(anchor="w", pady=(2, 0))

        # 2. Ledger Card with Filters & Actions
        ledger_card = tk.LabelFrame(
            container,
            text=" Financial Risk Ledger & Insurance Claims Center ",
            font=("Helvetica", 11, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_PRIMARY_DARK,
            padx=14,
            pady=10
        )
        ledger_card.pack(fill=tk.BOTH, expand=True)

        tool_frame = tk.Frame(ledger_card, bg=self.COLOR_SURFACE)
        tool_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(tool_frame, text="Region:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 4))
        self.ledger_region_filter_var = tk.StringVar(value="All Regions")
        combo_ledger_reg = ttk.Combobox(
            tool_frame,
            textvariable=self.ledger_region_filter_var,
            width=14,
            values=["All Regions", "Maharashtra", "Punjab", "Rajasthan", "Madhya Pradesh", "Uttar Pradesh", "Kerala", "West Bengal", "Gujarat"]
        )
        combo_ledger_reg.pack(side=tk.LEFT, padx=(0, 8))
        combo_ledger_reg.bind("<<ComboboxSelected>>", lambda e: self.refresh_ledger_and_kpis())

        tk.Label(tool_frame, text="Risk Level:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 4))
        self.ledger_risk_filter_var = tk.StringVar(value="All Risk Levels")
        combo_ledger_risk = ttk.Combobox(
            tool_frame,
            textvariable=self.ledger_risk_filter_var,
            width=13,
            values=["All Risk Levels", "Low Risk", "Medium Risk", "High Risk"]
        )
        combo_ledger_risk.pack(side=tk.LEFT, padx=(0, 8))
        combo_ledger_risk.bind("<<ComboboxSelected>>", lambda e: self.refresh_ledger_and_kpis())

        tk.Label(tool_frame, text="Claim Status:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 4))
        self.ledger_status_filter_var = tk.StringVar(value="All Statuses")
        combo_ledger_stat = ttk.Combobox(
            tool_frame,
            textvariable=self.ledger_status_filter_var,
            width=12,
            values=["All Statuses", "Pending", "Approved", "Disbursed"]
        )
        combo_ledger_stat.pack(side=tk.LEFT, padx=(0, 8))
        combo_ledger_stat.bind("<<ComboboxSelected>>", lambda e: self.refresh_ledger_and_kpis())

        tk.Label(tool_frame, text="Farmer:", font=("Helvetica", 9, "bold"), bg=self.COLOR_SURFACE, fg=self.COLOR_TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 4))
        self.ledger_name_search_var = tk.StringVar()
        entry_ledger_name = ttk.Entry(tool_frame, textvariable=self.ledger_name_search_var, width=12)
        entry_ledger_name.pack(side=tk.LEFT, padx=(0, 8))
        entry_ledger_name.bind("<Return>", lambda e: self.refresh_ledger_and_kpis())

        ttk.Button(tool_frame, text="Filter", style="Primary.TButton", command=self.refresh_ledger_and_kpis).pack(side=tk.LEFT, padx=3)
        ttk.Button(tool_frame, text="Reset", style="Muted.TButton", command=self._reset_ledger_filters).pack(side=tk.LEFT, padx=3)

        self.btn_export_csv = ttk.Button(tool_frame, text="📥 Export CSV", style="Muted.TButton", command=self.handle_export_csv)
        self.btn_export_csv.pack(side=tk.RIGHT, padx=4)

        self.btn_disburse_claim = ttk.Button(tool_frame, text="💳 Disburse Payout", style="Accent.TButton", command=self.handle_disburse_payout)
        self.btn_disburse_claim.pack(side=tk.RIGHT, padx=4)

        self.btn_approve_claim = ttk.Button(tool_frame, text="✅ Approve Claim", style="Primary.TButton", command=self.handle_approve_claim)
        self.btn_approve_claim.pack(side=tk.RIGHT, padx=4)

        # Treeview for Ledger
        ledger_scroll_y = ttk.Scrollbar(ledger_card, orient=tk.VERTICAL)
        ledger_scroll_x = ttk.Scrollbar(ledger_card, orient=tk.HORIZONTAL)

        cols = (
            "asst_id", "claim_id", "date", "farmer", "region", "crop",
            "weather", "risk", "base_rate", "adj_rate", "loan", "payout", "status"
        )
        self.ledger_tree = ttk.Treeview(
            ledger_card,
            columns=cols,
            show="headings",
            selectmode="browse",
            yscrollcommand=ledger_scroll_y.set,
            xscrollcommand=ledger_scroll_x.set
        )

        ledger_scroll_y.config(command=self.ledger_tree.yview)
        ledger_scroll_x.config(command=self.ledger_tree.xview)

        self.ledger_tree.heading("asst_id", text="Asst #")
        self.ledger_tree.heading("claim_id", text="Claim #")
        self.ledger_tree.heading("date", text="Date & Time")
        self.ledger_tree.heading("farmer", text="Farmer Name")
        self.ledger_tree.heading("region", text="Region")
        self.ledger_tree.heading("crop", text="Crop")
        self.ledger_tree.heading("weather", text="Obs/Fcst Temp")
        self.ledger_tree.heading("risk", text="Risk Score")
        self.ledger_tree.heading("base_rate", text="Base %")
        self.ledger_tree.heading("adj_rate", text="Adj Rate %")
        self.ledger_tree.heading("loan", text="Active Loan (₹)")
        self.ledger_tree.heading("payout", text="Payout (₹)")
        self.ledger_tree.heading("status", text="Claim Status")

        self.ledger_tree.column("asst_id", width=55, anchor="center")
        self.ledger_tree.column("claim_id", width=60, anchor="center")
        self.ledger_tree.column("date", width=125, anchor="center")
        self.ledger_tree.column("farmer", width=120, anchor="w")
        self.ledger_tree.column("region", width=135, anchor="w")
        self.ledger_tree.column("crop", width=90, anchor="w")
        self.ledger_tree.column("weather", width=105, anchor="center")
        self.ledger_tree.column("risk", width=95, anchor="center")
        self.ledger_tree.column("base_rate", width=65, anchor="e")
        self.ledger_tree.column("adj_rate", width=80, anchor="e")
        self.ledger_tree.column("loan", width=115, anchor="e")
        self.ledger_tree.column("payout", width=110, anchor="e")
        self.ledger_tree.column("status", width=90, anchor="center")

        # Botanical harmonious tags for risk levels
        self.ledger_tree.tag_configure("high_risk", background=self.COLOR_RISK_HIGH_BG, foreground="#922F22")
        self.ledger_tree.tag_configure("med_risk", background=self.COLOR_RISK_MED_BG, foreground="#885A14")
        self.ledger_tree.tag_configure("low_risk", background=self.COLOR_RISK_LOW_BG, foreground="#205029")

        ledger_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        ledger_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.ledger_tree.pack(fill=tk.BOTH, expand=True)

        self.ledger_tree.bind("<<TreeviewSelect>>", self._on_ledger_item_selected)

    def _reset_ledger_filters(self) -> None:
        self.ledger_region_filter_var.set("All Regions")
        self.ledger_risk_filter_var.set("All Risk Levels")
        self.ledger_status_filter_var.set("All Statuses")
        self.ledger_name_search_var.set("")
        self.refresh_ledger_and_kpis()

    def _on_ledger_item_selected(self, event) -> None:
        selected_items = self.ledger_tree.selection()
        if not selected_items:
            self.selected_ledger_claim_id = None
            self.selected_ledger_assessment_id = None
            return

        values = self.ledger_tree.item(selected_items[0])["values"]
        if not values:
            return

        asst_id = int(values[0])
        claim_id_val = values[1]
        try:
            claim_id = int(claim_id_val) if int(claim_id_val) > 0 else None
        except ValueError:
            claim_id = None

        self.selected_ledger_assessment_id = asst_id
        self.selected_ledger_claim_id = claim_id

    def refresh_ledger_and_kpis(self) -> None:
        kpis = self.db.get_financial_kpis()
        self.lbl_kpi_total_loans.config(text=f"₹{kpis['total_loans_active']:,.2f}")
        self.lbl_kpi_payout_exposure.config(text=f"₹{kpis['total_payout_exposure']:,.2f}")
        self.lbl_kpi_high_risk_count.config(text=str(kpis['high_risk_farmer_count']))
        self.lbl_kpi_disbursed.config(text=f"₹{kpis['total_disbursed']:,.2f}")

        reg = self.ledger_region_filter_var.get().strip()
        risk = self.ledger_risk_filter_var.get().strip()
        stat = self.ledger_status_filter_var.get().strip()
        name = self.ledger_name_search_var.get().strip()

        records = self.db.get_claims_ledger(
            region_filter=reg,
            risk_filter=risk,
            name_filter=name,
            status_filter=stat
        )

        for item in self.ledger_tree.get_children():
            self.ledger_tree.delete(item)

        for r in records:
            risk_val = r["risk_score"]
            if "High" in risk_val:
                tag = "high_risk"
            elif "Medium" in risk_val:
                tag = "med_risk"
            else:
                tag = "low_risk"

            claim_id_disp = r["claim_id"] if r["claim_id"] > 0 else "-"
            weather_disp = f"{r['obs_temp']:.1f}° / {r['predicted_temp']:.1f}°C"

            self.ledger_tree.insert(
                "",
                tk.END,
                values=(
                    r["assessment_id"],
                    claim_id_disp,
                    r["assessment_date"],
                    r["farmer_name"],
                    r["region"],
                    r["crop_type"],
                    weather_disp,
                    r["risk_score"],
                    f"{r['base_interest_rate']:.2f}%",
                    f"{r['adjusted_interest_rate']:.2f}%",
                    f"₹{r['loan_amount']:,.2f}",
                    f"₹{r['calculated_payout']:,.2f}",
                    r["claim_status"]
                ),
                tags=(tag,)
            )

        self.set_status(f"Ledger updated: {len(records)} records displayed.")

    def handle_approve_claim(self) -> None:
        if not self.selected_ledger_claim_id:
            messagebox.showwarning("Notice", "Please select a ledger record with an active claim to approve.")
            return

        try:
            self.db.update_claim_status(self.selected_ledger_claim_id, "Approved")
            messagebox.showinfo("Claim Approved", f"Insurance Claim #{self.selected_ledger_claim_id} has been APPROVED.")
            self.refresh_ledger_and_kpis()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve claim: {str(e)}")

    def handle_disburse_payout(self) -> None:
        if not self.selected_ledger_claim_id:
            messagebox.showwarning("Notice", "Please select a ledger record with an active claim to disburse.")
            return

        confirm = messagebox.askyesno(
            "Confirm Disbursement",
            f"Are you sure you want to DISBURSE funds for Claim #{self.selected_ledger_claim_id}?\n\n"
            "This will mark the funds as released to the farmer's microfinance account.",
            icon="question"
        )
        if not confirm:
            return

        try:
            self.db.update_claim_status(self.selected_ledger_claim_id, "Disbursed")
            messagebox.showinfo("Payout Disbursed", f"Funds successfully DISBURSED for Claim #{self.selected_ledger_claim_id}!")
            self.refresh_ledger_and_kpis()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disburse payout: {str(e)}")

    def handle_export_csv(self) -> None:
        records = self.db.get_claims_ledger(
            region_filter=self.ledger_region_filter_var.get().strip(),
            risk_filter=self.ledger_risk_filter_var.get().strip(),
            name_filter=self.ledger_name_search_var.get().strip(),
            status_filter=self.ledger_status_filter_var.get().strip()
        )

        if not records:
            messagebox.showwarning("Export Notice", "No records found in current view to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Financial Risk Ledger as CSV",
            initialfile=f"agro_risk_ledger_rupees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if not file_path:
            return

        try:
            fieldnames = [
                "assessment_id", "claim_id", "assessment_date", "farmer_name", "region",
                "crop_type", "loan_amount", "base_interest_rate", "obs_temp",
                "predicted_temp", "season", "risk_score", "calculated_payout",
                "adjusted_interest_rate", "claim_status"
            ]

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for row in records:
                    writer.writerow(row)

            messagebox.showinfo("Export Successful", f"Exported {len(records)} records to:\n{file_path}")
            self.set_status(f"Exported ledger CSV to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write CSV file: {str(e)}")
