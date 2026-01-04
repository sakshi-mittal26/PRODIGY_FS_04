from flask import Flask, render_template, redirect, url_for
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),   # MUST be localstore
    cursorclass=pymysql.cursors.DictCursor
)

# HOME → PRODUCT LIST
@app.route("/")
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template("index.html", products=products)

# ADD TO CART
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cart (product_id) VALUES (%s)",
        (product_id,)
    )
    conn.commit()
    cursor.close()
    return redirect(url_for("index"))

# VIEW CART
@app.route("/cart")
def view_cart():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.id, products.name, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
    """)
    cart_items = cursor.fetchall()
    cursor.close()
    return render_template("cart.html", cart_items=cart_items)

# REMOVE FROM CART
@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cart WHERE product_id = %s LIMIT 1",
        (product_id,)
    )
    conn.commit()
    cursor.close()
    return redirect(url_for("view_cart"))

if __name__ == "__main__":
    app.run(debug=True)
