import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import messagebox
import json
import os
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Default values for Polaris CLI options
DEFAULT_POLARIS_CLI_PATH = os.getenv("POLARIS_CLI_PATH", "./polaris")
DEFAULT_HOST = os.getenv("POLARIS_HOST", "localhost")
DEFAULT_PORT = os.getenv("POLARIS_PORT", "8181")
DEFAULT_CLIENT_ID = os.getenv("POLARIS_CLIENT_ID", None)
DEFAULT_CLIENT_SECRET = os.getenv("POLARIS_CLIENT_SECRET", None)


# Function to call the Polaris CLI
def run_cli_command(args):
    try:
        logging.debug(f"Running CLI command: {' '.join(args)}")
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"CLI Error: {result.stderr}")
            messagebox.showerror("Error", result.stderr)
        else:
            logging.info("CLI command executed successfully")
            return result.stdout
    except Exception as e:
        logging.exception("Failed to execute CLI command")
        messagebox.showerror("Error", f"Failed to execute CLI command: {e}")

# Function to list catalogs
def list_catalogs():
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "catalogs", "list"
    ]
    output = run_cli_command(args)
    logging.debug(f"CLI output: {output}")

    if output:
        try:
            # Split the output by newlines (assuming each line is a separate JSON object)
            catalog_lines = output.strip().split("\n")

            for row in catalog_table.get_children():
                catalog_table.delete(row)

            # Process each catalog JSON object
            for line in catalog_lines:
                if line.strip():  # Skip empty lines
                    catalog = json.loads(line)  # Parse each line as a JSON object
                    catalog_table.insert('', 'end', values=(
                        catalog.get("name", ""),
                        catalog.get("type", ""),
                        catalog.get("storageConfigInfo", {}).get("storageType", ""),
                        catalog.get("properties", {}).get("default-base-location", "")
                    ))
        except json.JSONDecodeError:
            logging.error("Failed to parse catalogs response. Output is not valid JSON.")
            messagebox.showerror("Error", "Failed to parse catalogs response.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")


# Function to list principals
def list_principals():
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principals", "list"
    ]
    output = run_cli_command(args)
    logging.debug(f"CLI output: {output}")

    if output:
        try:
            principals = output.strip().split("\n")  # Assuming each principal is on a new line
            for row in principal_table.get_children():
                principal_table.delete(row)
            for principal in principals:
                # Convert the string to a dictionary
                principal_data = json.loads(principal)
                principal_table.insert('', 'end', values=(
                    principal_data.get("name", ""),
                    principal_data.get("clientId", ""),
                    principal_data.get("type", "N/A"),
                    principal_data.get("createTimestamp", "")
                ))
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse principals response.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")


# Function to create a catalog
def create_catalog_dialog():
    # Create a new dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Create Catalog")

    # Catalog Name
    tk.Label(dialog, text="Catalog Name:").grid(row=0, column=0)
    catalog_name_entry = tk.Entry(dialog, width=30)
    catalog_name_entry.grid(row=0, column=1)

    # Catalog Type
    tk.Label(dialog, text="Catalog Type (INTERNAL/EXTERNAL):").grid(row=1, column=0)
    catalog_type_entry = tk.Entry(dialog, width=30)
    catalog_type_entry.grid(row=1, column=1)

    # Storage Type
    tk.Label(dialog, text="Storage Type (e.g., FILE):").grid(row=2, column=0)
    catalog_storage_type_entry = tk.Entry(dialog, width=30)
    catalog_storage_type_entry.grid(row=2, column=1)

    # Base Location
    tk.Label(dialog, text="Default Base Location:").grid(row=3, column=0)
    catalog_base_location_entry = tk.Entry(dialog, width=30)
    catalog_base_location_entry.grid(row=3, column=1)

    # Optional fields
    tk.Label(dialog, text="Role ARN (S3):").grid(row=4, column=0)
    role_arn_entry = tk.Entry(dialog, width=30)
    role_arn_entry.grid(row=4, column=1)

    tk.Label(dialog, text="External ID (S3):").grid(row=5, column=0)
    external_id_entry = tk.Entry(dialog, width=30)
    external_id_entry.grid(row=5, column=1)

    tk.Label(dialog, text="Tenant ID (Azure):").grid(row=6, column=0)
    tenant_id_entry = tk.Entry(dialog, width=30)
    tenant_id_entry.grid(row=6, column=1)

    tk.Label(dialog, text="App Name (Azure):").grid(row=7, column=0)
    app_name_entry = tk.Entry(dialog, width=30)
    app_name_entry.grid(row=7, column=1)

    tk.Label(dialog, text="Consent URL (Azure):").grid(row=8, column=0)
    consent_url_entry = tk.Entry(dialog, width=30)
    consent_url_entry.grid(row=8, column=1)

    tk.Label(dialog, text="Service Account (GCS):").grid(row=9, column=0)
    service_account_entry = tk.Entry(dialog, width=30)
    service_account_entry.grid(row=9, column=1)

    tk.Label(dialog, text="Remote URL (External):").grid(row=10, column=0)
    remote_url_entry = tk.Entry(dialog, width=30)
    remote_url_entry.grid(row=10, column=1)

    tk.Label(dialog, text="Allowed Location:").grid(row=11, column=0)
    allowed_location_entry = tk.Entry(dialog, width=30)
    allowed_location_entry.grid(row=11, column=1)

    # Function to run when "Create" button is clicked
    def create_catalog():
        catalog_name = catalog_name_entry.get().strip()
        if not catalog_name:
            messagebox.showerror("Error", "Catalog name is required!")
            return
        args = [
            polaris_cli_path_entry.get(),
            "--host", host_entry.get(),
            "--port", port_entry.get(),
            "--client-id", client_id_entry.get(),
            "--client-secret", client_secret_entry.get(),
            "catalogs", "create",
            "--type", catalog_type_entry.get(),
            "--storage-type", catalog_storage_type_entry.get(),
            "--default-base-location", catalog_base_location_entry.get(),
            catalog_name  # Add the catalog name as the positional argument
        ]

        # Add optional fields for S3, Azure, GCS, etc.
        if role_arn_entry.get():
            args.extend(["--role-arn", role_arn_entry.get()])
        if external_id_entry.get():
            args.extend(["--external-id", external_id_entry.get()])
        if tenant_id_entry.get():
            args.extend(["--tenant-id", tenant_id_entry.get()])
        if app_name_entry.get():
            args.extend(["--multi-tenant-app-name", app_name_entry.get()])
        if consent_url_entry.get():
            args.extend(["--consent-url", consent_url_entry.get()])
        if service_account_entry.get():
            args.extend(["--service-account", service_account_entry.get()])
        if remote_url_entry.get():
            args.extend(["--remote-url", remote_url_entry.get()])
        if allowed_location_entry.get():
            args.extend(["--allowed-location", allowed_location_entry.get()])


        output = run_cli_command(args)
        #if output:
        messagebox.showinfo("Sent", "Catalog creation command sent.")
        dialog.destroy()  # Close the dialog after successful creation
    list_catalogs()
    # Create button in dialog
    tk.Button(dialog, text="Create", command=create_catalog).grid(row=12, columnspan=2, pady=10)

# Function to delete the selected catalog
def delete_catalog():
    # Get the selected item in the catalog table
    selected_item = catalog_table.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a catalog to delete.")
        return

    # Get the catalog name from the selected row
    catalog_name = catalog_table.item(selected_item, 'values')[0]  # Assuming the catalog name is in the first column

    if not catalog_name:
        messagebox.showerror("Error", "Unable to retrieve the selected catalog name.")
        return

    # Ask for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the catalog '{catalog_name}'?")
    if not confirm:
        return

    # Run the CLI command to delete the catalog
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "catalogs", "delete", catalog_name
    ]
    output = run_cli_command(args)
    messagebox.showinfo("Sent", "Catalog delete command sent.")

    list_catalogs()


# Function to create a principal using a dialog
def create_principal_dialog():
    # Create a new dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Create Principal")

    # Principal Name
    tk.Label(dialog, text="Principal Name:").grid(row=0, column=0)
    principal_name_entry = tk.Entry(dialog, width=30)
    principal_name_entry.grid(row=0, column=1)

    # Function to run when the "Create" button is clicked
    def create_principal():
        args = [
            polaris_cli_path_entry.get(),
            "--host", host_entry.get(),
            "--port", port_entry.get(),
            "--client-id", client_id_entry.get(),
            "--client-secret", client_secret_entry.get(),
            "principals", "create",
            principal_name_entry.get(),
        ]

        output = run_cli_command(args)
        messagebox.showinfo("Sent", "Principal creation command sent.")
        dialog.destroy()  # Close the dialog after successful creation

    # Create button in dialog
    tk.Button(dialog, text="Create", command=create_principal).grid(row=4, columnspan=2, pady=10)
    list_principals()

# Function to delete the selected principal
def delete_principal():
    # Get the selected item in the principal table
    selected_item = principal_table.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a principal to delete.")
        return

    # Get the principal name from the selected row
    principal_name = principal_table.item(selected_item, 'values')[0]  # Assuming the principal name is in the first column

    if not principal_name:
        messagebox.showerror("Error", "Unable to retrieve the selected principal name.")
        return

    # Ask for confirmation before deleting
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the principal '{principal_name}'?")
    if not confirm:
        return

    # Run the CLI command to delete the principal
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principals", "delete", principal_name
    ]
    output = run_cli_command(args)

    #if output:
    messagebox.showinfo("Sent", f"Principal '{principal_name}' deletion command sent.")
        # Refresh the principal list after deletion
    list_principals()
# Function to list principal roles
def list_principal_roles():
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principal-roles", "list"
    ]
    output = run_cli_command(args)
    logging.debug(f"CLI output: {output}")

    if output:
        try:
            # Split the output by newlines, assuming each line is a separate JSON object
            principal_role_lines = output.strip().split("\n")

            # Clear the table before inserting new data
            for row in principal_role_table.get_children():
                principal_role_table.delete(row)

            # Process each line of the output as a JSON object
            for line in principal_role_lines:
                if line.strip():  # Ignore any empty lines
                    role_data = json.loads(line)  # Parse each line as JSON
                    principal_role_table.insert('', 'end', values=(
                        role_data.get("name", ""),  # Principal role name
                        role_data.get("properties", {})  # Properties
                    ))
        except json.JSONDecodeError:
            logging.error("Failed to parse principal roles response.")
            messagebox.showerror("Error", "Failed to parse principal roles response.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open a dialog for creating a principal role
def create_principal_role_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Create Principal Role")

    # Principal Role Name
    tk.Label(dialog, text="Principal Role Name:").grid(row=0, column=0)
    principal_role_entry = tk.Entry(dialog, width=30)
    principal_role_entry.grid(row=0, column=1)

    # Optional Property (Key-Value)
    tk.Label(dialog, text="Property Key:").grid(row=1, column=0)
    property_key_entry = tk.Entry(dialog, width=30)
    property_key_entry.grid(row=1, column=1)

    tk.Label(dialog, text="Property Value:").grid(row=2, column=0)
    property_value_entry = tk.Entry(dialog, width=30)
    property_value_entry.grid(row=2, column=1)

    def create_principal_role():
        principal_role = principal_role_entry.get().strip()
        if not principal_role:
            messagebox.showerror("Error", "Principal role name is required.")
            return

        args = [
            polaris_cli_path_entry.get(),
            "--host", host_entry.get(),
            "--port", port_entry.get(),
            "--client-id", client_id_entry.get(),
            "--client-secret", client_secret_entry.get(),
            "principal-roles", "create", principal_role
        ]

        # Add property if provided
        if property_key_entry.get() and property_value_entry.get():
            args.extend(["--property", f"{property_key_entry.get()}={property_value_entry.get()}"])

        output = run_cli_command(args)
        if output:
            messagebox.showinfo("Success", f"Principal role '{principal_role}' created successfully.")
            dialog.destroy()
            list_principal_roles()

    # Add button to submit the dialog form
    tk.Button(dialog, text="Create", command=create_principal_role).grid(row=3, columnspan=2, pady=10)
# Function to delete the selected principal role
def delete_principal_role():
    selected_item = principal_role_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a principal role to delete.")
        return

    # Get the principal role from the selected row
    principal_role = principal_role_table.item(selected_item, 'values')[0]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the principal role '{principal_role}'?")
    if not confirm:
        return

    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principal-roles", "delete", principal_role
    ]
    output = run_cli_command(args)

    if output:
        messagebox.showinfo("Success", f"Principal role '{principal_role}' deleted successfully.")
        list_principal_roles()
# Function to grant the selected principal role to the selected principal
def grant_principal_role():
    # Get the selected principal
    selected_principal_item = principal_table.selection()

    if not selected_principal_item:
        messagebox.showerror("Error", "Please select a principal to assign a role to.")
        return

    # Get the principal name from the selected row
    principal_name = principal_table.item(selected_principal_item, 'values')[0]

    if not principal_name:
        messagebox.showerror("Error", "Unable to retrieve the selected principal name.")
        return

    # Get the selected principal role
    selected_role_item = principal_role_table.selection()

    if not selected_role_item:
        messagebox.showerror("Error", "Please select a principal role to assign.")
        return

    # Get the role name from the selected row
    principal_role_name = principal_role_table.item(selected_role_item, 'values')[0]

    if not principal_role_name:
        messagebox.showerror("Error", "Unable to retrieve the selected role name.")
        return

    # Run the CLI command to grant the selected role to the selected principal
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principal-roles", "grant", principal_role_name,
        "--principal", principal_name
    ]

    output = run_cli_command(args)

    if output:
        messagebox.showinfo("Success", f"Principal role '{principal_role_name}' granted to principal '{principal_name}' successfully.")
        # Optionally, you can refresh the roles assigned to the selected principal
        load_assigned_roles()

# Function to open a dialog for revoking a principal role from a principal
def revoke_principal_role_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Revoke Principal Role")

    # Principal Role
    tk.Label(dialog, text="Principal Role Name:").grid(row=0, column=0)
    principal_role_entry = tk.Entry(dialog, width=30)
    principal_role_entry.grid(row=0, column=1)

    # Principal
    tk.Label(dialog, text="Principal Name:").grid(row=1, column=0)
    principal_entry = tk.Entry(dialog, width=30)
    principal_entry.grid(row=1, column=1)

    def revoke_principal_role():
        principal_role = principal_role_entry.get().strip()
        principal = principal_entry.get().strip()
        if not principal_role or not principal:
            messagebox.showerror("Error", "Both Principal Role and Principal are required.")
            return

        args = [
            polaris_cli_path_entry.get(),
            "--host", host_entry.get(),
            "--port", port_entry.get(),
            "--client-id", client_id_entry.get(),
            "--client-secret", client_secret_entry.get(),
            "principal-roles", "revoke", principal_role,
            "--principal", principal
        ]

        output = run_cli_command(args)
        if output:
            messagebox.showinfo("Success", f"Principal role '{principal_role}' revoked from '{principal}'.")
            dialog.destroy()
            list_principal_roles()

    # Add button to submit the form
    tk.Button(dialog, text="Revoke", command=revoke_principal_role).grid(row=2, columnspan=2, pady=10)

# Function to load assigned roles for the selected principal
def load_assigned_roles():
    # Get the selected principal
    selected_item = principal_table.selection()

    if not selected_item:
        return  # No principal selected, do nothing

    # Get the principal name from the selected row
    principal_name = principal_table.item(selected_item, 'values')[0]

    if not principal_name:
        return  # Unable to retrieve the principal name, do nothing

    # Run the CLI command to list roles assigned to the principal
    args = [
        polaris_cli_path_entry.get(),
        "--host", host_entry.get(),
        "--port", port_entry.get(),
        "--client-id", client_id_entry.get(),
        "--client-secret", client_secret_entry.get(),
        "principal-roles", "list",
        "--principal", principal_name
    ]
    output = run_cli_command(args)
    logging.debug(f"CLI output: {output}")

    # Clear the table before inserting new data
    for row in assigned_roles_table.get_children():
        assigned_roles_table.delete(row)

    if output:
        try:
            # Split the output by newlines, assuming each line is a separate JSON object for a role
            role_lines = output.strip().split("\n")



            # Process each role in the output
            for line in role_lines:
                if line.strip():  # Ignore empty lines
                    role_data = json.loads(line)  # Parse each line as JSON
                    assigned_roles_table.insert('', 'end', values=(
                        role_data.get("name", ""),  # Role name
                        role_data.get("properties", {})  # Role properties
                    ))
        except json.JSONDecodeError:
            logging.error("Failed to parse roles assigned to the principal.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")


# Main Application window
root = tk.Tk()
root.title("Polaris Management GUI")

# Set up frames for Polaris CLI path, Host, Port, Client ID, and Secret input
auth_frame = ttk.Frame(root)
auth_frame.pack(pady=10)

tk.Label(auth_frame, text="Polaris CLI Path:").grid(row=0, column=0)
polaris_cli_path_entry = tk.Entry(auth_frame, width=30)
polaris_cli_path_entry.insert(0, DEFAULT_POLARIS_CLI_PATH)
polaris_cli_path_entry.grid(row=0, column=1)

tk.Label(auth_frame, text="Host:").grid(row=1, column=0)
host_entry = tk.Entry(auth_frame, width=30)
host_entry.insert(0, DEFAULT_HOST)
host_entry.grid(row=1, column=1)

tk.Label(auth_frame, text="Port:").grid(row=2, column=0)
port_entry = tk.Entry(auth_frame, width=30)
port_entry.insert(0, DEFAULT_PORT)
port_entry.grid(row=2, column=1)

tk.Label(auth_frame, text="Client ID:").grid(row=3, column=0)
client_id_entry = tk.Entry(auth_frame, width=30)
client_id_entry.insert(0, DEFAULT_CLIENT_ID)
client_id_entry.grid(row=3, column=1)

tk.Label(auth_frame, text="Client Secret:").grid(row=4, column=0)
client_secret_entry = tk.Entry(auth_frame, width=30, show="*")
client_secret_entry.insert(0, DEFAULT_CLIENT_SECRET)
client_secret_entry.grid(row=4, column=1)

# Tabbed interface for Catalog and Principal management
notebook = ttk.Notebook(root)
# Catalogs Tab
catalog_frame = ttk.Frame(notebook)
notebook.add(catalog_frame, text="Catalogs")

# Catalog Table
catalog_table = ttk.Treeview(catalog_frame, columns=("Name", "Type", "Storage Type", "Base Location"), show="headings")
catalog_table.heading("Name", text="Name")
catalog_table.heading("Type", text="Type")
catalog_table.heading("Storage Type", text="Storage Type")
catalog_table.heading("Base Location", text="Base Location")
catalog_table.grid(row=0, column=0, columnspan=3, sticky="nsew")

tk.Button(catalog_frame, text="List Catalogs", command=list_catalogs).grid(row=1, column=0, sticky="ew", padx=5, pady=5)
tk.Button(catalog_frame, text="Create Catalog", command=create_catalog_dialog).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
tk.Button(catalog_frame, text="Delete Catalog", command=delete_catalog).grid(row=1, column=2, sticky="ew", padx=5, pady=5)

# Principals Tab
principal_frame = ttk.Frame(notebook)
notebook.add(principal_frame, text="Principals")

# Principal Table
principal_table = ttk.Treeview(principal_frame, columns=("Name", "Client ID", "Type", "Created Timestamp"), show="headings")
principal_table.heading("Name", text="Name")
principal_table.heading("Client ID", text="Client ID")
principal_table.heading("Type", text="Type")
principal_table.heading("Created Timestamp", text="Created Timestamp")
principal_table.grid(row=0, column=0, columnspan=3, sticky="nsew")

# Principal Roles Table
principal_role_table = ttk.Treeview(principal_frame, columns=("Principal Role", "Properties"), show="headings")
principal_role_table.heading("Principal Role", text="Principal Role")
principal_role_table.heading("Properties", text="Properties")
principal_role_table.grid(row=1, column=0, columnspan=3, sticky="nsew")

# Assigned Roles Table (for roles assigned to selected principal)
assigned_roles_table = ttk.Treeview(principal_frame, columns=("Role Name", "Properties"), show="headings")
assigned_roles_table.heading("Role Name", text="Role Name")
assigned_roles_table.heading("Properties", text="Properties")
assigned_roles_table.grid(row=2, column=0, columnspan=3, sticky="nsew")

# Bind the selection event for the Principals Table
principal_table.bind("<<TreeviewSelect>>", lambda event: load_assigned_roles())

# Buttons for managing principals
tk.Button(principal_frame, text="List Principals", command=list_principals).grid(row=3, column=0, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Create Principal", command=create_principal_dialog).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Delete Principal", command=delete_principal).grid(row=3, column=2, sticky="ew", padx=5, pady=5)

# Buttons for managing principal roles
tk.Button(principal_frame, text="List Principal Roles", command=list_principal_roles).grid(row=4, column=0, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Create Principal Role", command=create_principal_role_dialog).grid(row=4, column=1, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Delete Principal Role", command=delete_principal_role).grid(row=4, column=2, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Grant Principal Role", command=grant_principal_role).grid(row=5, column=0, sticky="ew", padx=5, pady=5)
tk.Button(principal_frame, text="Revoke Principal Role", command=revoke_principal_role_dialog).grid(row=5, column=1, sticky="ew", padx=5, pady=5)


# Add the notebook (tab interface) to the window
notebook.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter loop
root.mainloop()
