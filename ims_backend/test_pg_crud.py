from inventory_crud_pg import InventoryCRUD

db = InventoryCRUD(
    host="localhost",
    database="carols_ims",
    user="ims_user",
    password="password123"
)

# Test ADD
new_id = db.add_product(
    name="PGTest",
    quantity=15,
    price=9.99,
    user_id=1
)
print("Added product ID:", new_id)

# Test UPDATE
db.update_product(
    new_id,
    quantity=25,
    price=10.99,
    user_id=1
)
print("Updated product.")

# Test SOFT DELETE
db.delete_product(new_id, user_id=1)
print("Soft deleted.")
