from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from decimal import Decimal, InvalidOperation

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # ---- Input Validation ----
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        # Decimal use kar rahe hain for financial accuracy
        price = Decimal(str(data['price']))
        if price < 0:
            return jsonify({"error": "Price cannot be negative"}), 400
    except (InvalidOperation, ValueError):
        return jsonify({"error": "Invalid price format"}), 400

    # ---- Atomic Transaction ----
    try:
        # Hum single commit use karenge taaki data inconsistent na ho
        with db.session.begin():
            # Check for duplicate SKU
            if Product.query.filter_by(sku=data['sku']).first():
                return jsonify({"error": "SKU already exists"}), 409

            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=price,
                warehouse_id=data['warehouse_id']
            )
            db.session.add(product)
            db.session.flush()  # ID generate karne ke liye

            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)

        return jsonify({"message": "Product created", "id": product.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
