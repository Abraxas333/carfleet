import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv


saved_queries = './output.csv'

class VehicleAdministration:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Administration App")
        self.root.geometry("600x500")
        self.create_gui()
        self.vehicles = {}
        self.customers = {}

    def create_gui(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        def clear_placeholder(event, placeholder):
            if event.widget.get() == placeholder:
                event.widget.delete(0, "end")
                event.widget.config(foreground='black')

        def set_placeholder(widget, placeholder):
            if widget.get() == "":
                widget.insert(0, placeholder)
                widget.config(foreground='grey')

        options = {
            "add vehicle": "input vehicle ID...",
            "delete vehicle": "input vehicle ID...",
            "add customer": "input customer ID...",
            "delete customer": "input customer ID..."
        }

        self.entries = {}
        self.labels = {}

        row = 1
        column = 1
        column_label = 0
        for key, value in options.items():
            entry = ttk.Entry(self.root, foreground='grey')
            label = ttk.Label(self.root, text=key)
            entry.grid(row=row, column=column)
            label.grid(row=row, column=column_label, sticky= tk.E)
            entry.insert(0, value)
            entry.bind("<FocusIn>", lambda event, value=value: clear_placeholder(event, value))
            entry.bind("<FocusOut>", lambda event, value=value: set_placeholder(event.widget, value))
            self.entries[key] = entry
            self.labels[key] = label
            row += 1 

        self.button_add_vehicle = ttk.Button(self.root, text="Add Vehicle", command=self.add_vehicle)
        self.button_add_vehicle.grid(row=5, column=0, pady=10)

        self.button_delete_vehicle = ttk.Button(self.root, text="Delete Vehicle", command=self.delete_vehicle)
        self.button_delete_vehicle.grid(row=5, column=1, pady=10)

        self.button_add_customer = ttk.Button(self.root, text="Add Customer", command=self.add_customer)
        self.button_add_customer.grid(row=5, column=2, pady=10)

        self.button_delete_customer = ttk.Button(self.root, text="Delete Customer", command=self.delete_customer)
        self.button_delete_customer.grid(row=6, column=2, pady=10)

        self.butotton_export = ttk.Button(self.root, text="export", command=self.export_info)
        self.butotton_export.grid(row=6, column=0, pady=10)

        self.butotton_import = ttk.Button(self.root, text="import", command=self.import_info)
        self.butotton_import.grid(row=6, column=1, pady=10)

        self.display_box = tk.Text(self.root, height=10, width=50)
        self.display_box.grid(row=9, columnspan=4, padx=20, pady=20)

    def add_vehicle(self):
        vehicle_id = self.entries["add vehicle"].get()
        if vehicle_id != "input vehicle ID..." and vehicle_id:
            self.vehicles[vehicle_id] = True
            self.display_info()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid vehicle ID.")

    def delete_vehicle(self):
        vehicle_id = self.entries["delete vehicle"].get()
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]
            self.display_info()
        else:
            messagebox.showwarning("Delete Error", "Vehicle ID not found.")

    def add_customer(self):
        customer_id = self.entries["add customer"].get()
        if customer_id != "input customer ID..." and customer_id:
            self.customers[customer_id] = True
            self.display_info()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid customer ID.")

    def delete_customer(self):
        customer_id = self.entries["delete customer"].get()
        if customer_id in self.customers:
            del self.customers[customer_id]
            self.display_info()
        else:
            messagebox.showwarning("Delete Error", "Customer ID not found.")

    def display_info(self):
        self.display_box.delete(1.0, tk.END)
        self.display_box.insert(tk.END, "Vehicles:\n")
        for vehicle in self.vehicles:
            self.display_box.insert(tk.END, f"{vehicle}\n")
        self.display_box.insert(tk.END, "\nCustomers:\n")
        for customer in self.customers:
            self.display_box.insert(tk.END, f"{customer}\n")
        

    
    def export_info(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[('csv files', '*.csv'), ('All files', '*.*')])
        if f:
            with open(f, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.info.keys())
                writer.writerow(self.info.values())
            messagebox.showinfo("Success", f"Exported Data to: {f}")

    def import_info(self):
        f = filedialog.askopenfilename(defaultextension=".csv", filetypes=[('csv files', '*.csv'), ('All files', '*.*')])
        if f:
            with open(f, "r", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                values = next(reader)
                self.info = dict(zip(headers, values))
                self.display_info()
            messagebox.showinfo("Success", f"Data imported from {f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleAdministration(root)
    root.mainloop()
