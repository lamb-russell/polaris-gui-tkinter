# Polaris Management GUI

Polaris Management GUI is a user-friendly interface for managing catalogs, principals, and roles in Polaris via the Polaris CLI. This GUI application is built using Python's Tkinter library, allowing easy interaction with the Polaris CLI without needing to type complex commands.

## Features

- **Catalog Management**:
  - List all available catalogs
  - Create new catalogs with customizable parameters (e.g., storage type, base location, etc.)
  - Delete catalogs
  
- **Principal Management**:
  - List principals (users)
  - Create new principals
  - Delete principals
  
- **Principal Role Management**:
  - List principal roles
  - Create new principal roles with optional properties
  - Delete principal roles
  - Grant a principal role to a selected principal
  - Revoke a principal role from a principal

- **View Assigned Roles**:
  - View roles assigned to a selected principal

## Prerequisites

Before running the application, ensure you have the following installed on your system:

1. **Python 3.x** – The application is written in Python 3.x.
2. **Polaris CLI** – The Polaris CLI is part of the Apache Polaris repository. You can find it [here](https://github.com/apache/polaris).

You can also refer to the [Apache Polaris Quickstart Guide](https://polaris.apache.org/in-dev/unreleased/quickstart/) for more detailed instructions on setting up Polaris, including getting the **client ID** and **client secret** from the Docker container.

### Required Python Libraries:

You need the following Python libraries to run the application:

- `tkinter`
- `subprocess` (part of Python standard library)
- `json` (part of Python standard library)
- `logging` (part of Python standard library)

To install any missing dependencies, you can use:

```bash
pip install tk
```

### Environment Setup Instructions

After running Polaris, you can find the **client ID** and **client secret** by inspecting the Docker logs, as described in the [Polaris Quickstart Documentation](https://polaris.apache.org/in-dev/unreleased/quickstart/). Here’s an example of how to set up the environment variables:

```bash
export CLIENT_ID=<client-id> 
export CLIENT_SECRET=<client-secret>
```

You can set these variables in your shell or alternatively, **manually enter the values** in the GUI fields provided for **Polaris CLI path**, **host**, **port**, **client ID**, and **client secret** if you prefer not to use environment variables.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/lamb-russell/polaris-gui-tkinter.git
   ```

2. Navigate to the project directory:

   ```bash
   cd polaris-gui-tkinter
   ```

3. Ensure the Polaris CLI is accessible and properly configured on your system. You can set the required environment variables for `POLARIS_CLI_PATH`, `POLARIS_HOST`, `POLARIS_PORT`, `POLARIS_CLIENT_ID`, and `POLARIS_CLIENT_SECRET`, or enter them manually into the fields in the application.

   Alternatively, you can set these directly in the application by editing the `DEFAULT_*` values in the source code.

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. The GUI will open with the following features:

   - **Catalogs Tab**: Manage your catalogs (list, create, delete).
   - **Principals Tab**: Manage principals (list, create, delete).
   - **Principal Roles**: Manage roles for principals (list, create, delete, grant, revoke).

3. **Authentication**: 
   - Enter the Polaris CLI path, host, port, client ID, and client secret in the appropriate fields at the top of the GUI window if they are not set in the environment variables.

### Entering Credentials via GUI

If you prefer not to use environment variables, the application provides fields where you can manually enter the required values:

- **Polaris CLI Path**: The path to the Polaris CLI binary.
- **Host**: The host where Polaris is running (default: `localhost`).
- **Port**: The port Polaris is running on (default: `8181`).
- **Client ID**: The client ID for Polaris authentication.
- **Client Secret**: The client secret for Polaris authentication.

These fields can be filled out each time the application starts, or you can modify the default values in the source code for convenience.

## GUI Overview

### Catalogs Tab
- **List Catalogs**: Lists all catalogs in your Polaris instance.
- **Create Catalog**: Opens a dialog to create a new catalog. You can specify storage type, base location, and other parameters.
- **Delete Catalog**: Deletes the selected catalog from the list.

### Principals Tab
- **List Principals**: Displays all available principals.
- **Create Principal**: Opens a dialog to create a new principal.
- **Delete Principal**: Deletes the selected principal from the list.
- **View Assigned Roles**: Automatically displays the roles assigned to the selected principal.

### Principal Roles Management
- **List Principal Roles**: Lists all available principal roles.
- **Create Principal Role**: Opens a dialog to create a new role with optional properties.
- **Delete Principal Role**: Deletes the selected principal role.
- **Grant/Revoke Principal Role**: Assigns or revokes roles for selected principals.

## Logs

The application generates logs for each CLI command execution. You can find logs in the `app.log` file, or view them in the terminal while the application is running.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Contribution

Feel free to submit issues or pull requests if you'd like to contribute to the development of this project.

## Contact

For questions or support, please create an issue on the GitHub repository.
