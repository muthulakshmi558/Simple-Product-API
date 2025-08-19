
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory product store
products = []


# --------------------
# Home Route
# --------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "status": 200,
        "message": "🛒 Welcome to Simple Product API",
        "endpoints": {
            "GET /products": "List all products",
            "POST /products": "Add new product",
            "PUT /products/<id>": "Update product",
            "DELETE /products/<id>": "Delete product"
        }
    }


# --------------------
# Create Product
# --------------------
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data or not data.get("name") or "price" not in data or "in_stock" not in data:
        return jsonify({"status": 400, "message": "Fields 'name', 'price', 'in_stock' are required"}), 400

    try:
        price = float(data["price"])
        if price <= 0:
            return jsonify({"status": 400, "message": "Price must be a number greater than 0"}), 400
    except ValueError:
        return jsonify({"status": 400, "message": "Price must be a valid number"}), 400

    product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": price,
        "in_stock": bool(data["in_stock"])
    }
    products.append(product)

    return jsonify({"status": 201, "message": "Product added successfully", "data": product}), 201


# --------------------
# Get All Products
# --------------------
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"status": 200, "count": len(products), "data": products}), 200


# --------------------
# Update Product
# --------------------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"status": 404, "message": "Product not found"}), 404

    data = request.get_json()
    if "name" in data:
        product["name"] = data["name"]

    if "price" in data:
        try:
            price = float(data["price"])
            if price <= 0:
                return jsonify({"status": 400, "message": "Price must be > 0"}), 400
            product["price"] = price
        except ValueError:
            return jsonify({"status": 400, "message": "Price must be a valid number"}), 400

    if "in_stock" in data:
        product["in_stock"] = bool(data["in_stock"])

    return jsonify({"status": 200, "message": "Product updated", "data": product}), 200


# --------------------
# Delete Product
# --------------------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"status": 404, "message": "Product not found"}), 404

    products = [p for p in products if p["id"] != product_id]

    return jsonify({"status": 200, "message": "Product deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
