import sqlite3

def delete_orders():
    try:
        # Connect to the database
        conn = sqlite3.connect('canteen.db')
        cursor = conn.cursor()

        # Execute the DELETE statement to remove all rows in the orders table
        cursor.execute('DELETE FROM orders')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("All orders deleted successfully.")
    except Exception as e:
        print(f"Error deleting orders: {e}")

# Call the function to delete all orders
delete_orders()
