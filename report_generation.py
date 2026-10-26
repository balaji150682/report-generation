import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Sample parameters with reference ranges: (Name, Min, Max, Unit, Decimal Places)
PARAMETERS = [
    ("Parameter A (Count)", 4000, 11000, "units/vol", 0),
    ("Parameter B (Percentage)", 40, 70, "%", 0),
    ("Parameter C (Level)", 13.5, 18.0, "g/dL", 1),
    ("Parameter D (Ratio)", 0.6, 1.3, "mg/dL", 2),
    ("Parameter E (Index)", 70, 150, "mg/dL", 0),
]

class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Entry & PDF Generator")
        self.root.geometry("650x600")

        # --- Top Frame: User Details ---
        details_frame = ttk.LabelFrame(root, text="General Information", padding=(10, 10))
        details_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="Age:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.age_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.age_var, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(details_frame, text="Sex:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sex_var = tk.StringVar(value="Male")
        ttk.Combobox(details_frame, textvariable=self.sex_var, values=["Male", "Female", "Other"], state="readonly", width=22).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="ID Number:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.emp_id_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.emp_id_var, width=15).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(details_frame, text="Organization:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.company_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.company_var, width=25).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="Date (DD/MM/YYYY):").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(details_frame, textvariable=self.date_var, width=15).grid(row=2, column=3, padx=5, pady=5)

        # --- Middle Frame: Parameters List ---
        params_frame = ttk.LabelFrame(root, text="Parameters", padding=(10, 10))
        params_frame.pack(fill="both", expand=True, padx=10, pady=5)

        headers = ["Test Name", "Result", "Units", "Reference Range"]
        for col, text in enumerate(headers):
            ttk.Label(params_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        self.result_vars = []
        for idx, (name, min_val, max_val, unit, decimals) in enumerate(PARAMETERS, start=1):
            ttk.Label(params_frame, text=name).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            
            res_var = tk.StringVar()
            self.result_vars.append((res_var, min_val, max_val, decimals))
            ttk.Entry(params_frame, textvariable=res_var, width=12).grid(row=idx, column=1, padx=10, pady=5)
            
            ttk.Label(params_frame, text=unit).grid(row=idx, column=2, padx=10, pady=5, sticky="w")
            ttk.Label(params_frame, text=f"{min_val} - {max_val}").grid(row=idx, column=3, padx=10, pady=5, sticky="w")

        # --- Bottom Frame: Buttons ---
        btn_frame = ttk.Frame(root, padding=(10, 10))
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Generate Random Values", command=self.generate_values).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save as PDF", command=self.save_pdf).pack(side="right", padx=5)

    def generate_values(self):
        """Generates random values within the specified reference ranges."""
        for res_var, min_val, max_val, decimals in self.result_vars:
            if decimals == 0:
                val = random.randint(int(min_val), int(max_val))
                res_var.set(str(val))
            else:
                val = random.uniform(min_val, max_val)
                res_var.set(f"{val:.{decimals}f}")

    def save_pdf(self):
        """Saves the current form data into a structured PDF document."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Report As"
        )
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4

            # --- Header Placeholder ---
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width / 2, height - 50, "SAMPLE ORGANIZATION HEADER")
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2, height - 65, "Standardized Report Template")
            c.line(40, height - 75, width - 40, height - 75)

            # --- Metadata Section ---
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, height - 100, f"Name: {self.name_var.get()}")
            c.drawString(350, height - 100, f"Date: {self.date_var.get()}")
            
            c.drawString(50, height - 120, f"Age: {self.age_var.get()}")
            c.drawString(150, height - 120, f"Sex: {self.sex_var.get()}")
            c.drawString(350, height - 120, f"ID: {self.emp_id_var.get()}")
            
            c.drawString(50, height - 140, f"Organization: {self.company_var.get()}")
            c.line(40, height - 155, width - 40, height - 155)

            # --- Table Headers ---
            y_pos = height - 180
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Parameter Name")
            c.drawString(250, y_pos, "Result")
            c.drawString(350, y_pos, "Units")
            c.drawString(450, y_pos, "Reference Range")
            c.line(40, y_pos - 5, width - 40, y_pos - 5)

            # --- Table Content ---
            c.setFont("Helvetica", 10)
            y_pos -= 25
            for idx, (name, min_val, max_val, unit, _) in enumerate(PARAMETERS):
                result_val = self.result_vars[idx][0].get()
                c.drawString(50, y_pos, name)
                c.drawString(250, y_pos, result_val)
                c.drawString(350, y_pos, unit)
                c.drawString(450, y_pos, f"{min_val} - {max_val}")
                y_pos -= 20

            # --- Footer Placeholder ---
            c.line(40, 100, width - 40, 100)
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, 70, "Authorized Seal Placeholder")
            c.drawRightString(width - 50, 70, "Authorized Signature Placeholder")

            c.save()
            messagebox.showinfo("Success", "PDF saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()