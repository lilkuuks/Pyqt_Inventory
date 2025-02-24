# Inventory Management System

An inventory management system built using PyQt5 and SQLite to help users add, update, delete,(CRUD) and search inventory items efficiently.

## Features
- Add new inventory items
- Update or delete existing items
- Search items by ID or name using regex
- Highlight selected row in the table
- Export data to a CSV file with a user-specified location
- Responsive UI with PyQt5

## Installation

### Prerequisites
Ensure you have Python 3 installed. Then, install the required dependencies:

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## Usage
Run the application with:
```sh
python main.py
```

### Exporting Data
1. Click the `EXPORT` button.
2. Select a save location via the file dialog.
3. The data will be saved as a CSV file.

## Database
- The system uses an SQLite database (`inventory.db`).
- The `products` table stores inventory items.
- Ensure the database file exists before running the app.

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.




