import InventoryCRUD
from inventory_crud import InventoryCRUD

db = InventoryCRUD(
    host="localhost",
    user="ims_user",
    password="yourpassword",
    database="carols_ims"
)

# 1a — Add product
product_id = db.add_product(
    name="Sprite 500ml",
    quantity=40,
    price=2.50,
    category_id=2,
    reorder_threshold=10,
    product_code="spr-500",
    user_id=1
)
print("Added:", product_id)

# 1b — Update product
db.update_product(
    product_id,
    quantity=45,
    price=2.75,
    user_id=1
)
print("Updated!")

# 1c — Soft delete
db.delete_product(product_id, user_id=1)
print("Soft deleted!")

# Hard delete:
# db.delete_product(product_id, user_id=1, permanent=True)
