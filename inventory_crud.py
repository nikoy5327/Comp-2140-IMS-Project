# inventory_crud.py

# Import the MySQL connector library used to interact with the database
import mysql.connector
from mysql.connector import Error


class InventoryCRUD:
    """
    This class provides Create, Update, and Delete operations for the products
    table in the inventory management system.
    """

    def __init__(self, host, user, password, database):
        """

        Constructor stores database connection settings.
        These will be used when connect() is called.
        """
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def connect(self):
        """
        Creates and returns a new connection to the database using stored config.
        """
        return mysql.connector.connect(**self.config)

    # ------------------ ADD PRODUCT ------------------
    def add_product(self, name, quantity, price,
                    category_id=None, product_code=None,
                    reorder_threshold=None, user_id=None):
        """
        Requirement 1a: Adds a new product to the inventory.
        Includes validation and duplicate checking.
        """

        # --- VALIDATION ---
        if not name or name.strip() == "":
            raise ValueError("Product name is required.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        try:
            # Establish a database connection
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)

            # Check if a product with the same name already exists (active only)
            cursor.execute(
                "SELECT id FROM products WHERE name = %s AND archived = 0",
                (name,)
            )
            if cursor.fetchone():
                raise ValueError("A product with this name already exists.")

            # SQL INSERT statement for adding the new product
            sql = """
                INSERT INTO products
                (product_code, name, category_id, price, current_quantity,
                 reorder_threshold, created_by, last_updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the INSERT with actual values
            cursor.execute(sql, (
                product_code, name, category_id, price, quantity,
                reorder_threshold, user_id, user_id
            ))

            # Save changes
            conn.commit()

            # Return the ID of the newly inserted row
            return cursor.lastrowid

        finally:
            # Cleanup — always close resources
            cursor.close()
            conn.close()

    # ------------------ UPDATE PRODUCT ------------------
    def update_product(self, product_id,
                       name=None, quantity=None, price=None,
                       category_id=None, reorder_threshold=None,
                       user_id=None):
        """
        Requirement 1b: Updates fields of an existing product.
        Only provided fields are updated. No empty values overwrite existing ones.
        """

        if not product_id:
            raise ValueError("Product ID is required.")

        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)

            # First check if the product exists
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()

            if not product or product["archived"] == 1:
                raise ValueError("Product does not exist or is archived.")

            # Prepare dynamic field updates
            updates = []
            params = []

            # Add each field only if it was provided
            if name is not None:
                updates.append("name = %s")
                params.append(name)

            if quantity is not None:
                updates.append("current_quantity = %s")
                params.append(quantity)

            if price is not None:
                updates.append("price = %s")
                params.append(price)

            if category_id is not None:
                updates.append("category_id = %s")
                params.append(category_id)

            if reorder_threshold is not None:
                updates.append("reorder_threshold = %s")
                params.append(reorder_threshold)

            # If nothing was provided to update, exit early
            if not updates:
                return False

            # Always track who last updated the record
            updates.append("last_updated_by = %s")
            params.append(user_id)

            # Build the final SQL
            sql = f"""
                UPDATE products
                SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """

            # Add product_id to end of params list
            params.append(product_id)

            # Execute update
            cursor.execute(sql, tuple(params))
            conn.commit()

            return True

        finally:
            cursor.close()
            conn.close()

    # ------------------ DELETE PRODUCT ------------------
    def delete_product(self, product_id, user_id=None, permanent=False):
        """
        Requirement 1c: Deletes a product.
        Soft delete: archived = 1
        Hard delete: permanently removed from table
        """

        if not product_id:
            raise ValueError("Product ID is required.")

        try:
            conn = self.connect()
            cursor = conn.cursor()

            if permanent:
                # Hard delete permanently removes the product
                cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            else:
                # Soft delete — marks as archived but keeps record in DB
                cursor.execute(
                    """
                    UPDATE products
                    SET archived = 1,
                        last_updated_by = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (user_id, product_id)
                )

            conn.commit()
            return True

        finally:
            cursor.close()
            conn.close()
