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
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/")
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template("index.html", products=products)

@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (product_id) VALUES (%s)", (product_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for("index"))

@app.route("/cart")
def cart():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.name, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
    """)
    items = cursor.fetchall()
    cursor.close()
    return render_template("cart.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)
