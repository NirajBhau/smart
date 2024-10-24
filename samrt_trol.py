import streamlit as st
import pandas as pd
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

# Sample product database (In a real application, this would come from a database)
products = {
    "product_id": [1, 2, 3],
    "product_name": ["Apple", "Banana", "Cherry"],
    "price": [30, 20, 50],
    "barcode": ["1234567890123", "1234567890124", "1234567890125"]  # Add barcode values
}
product_df = pd.DataFrame(products)

# Initialize cart
cart = []

# Function to add items to cart
def add_to_cart(product):
    cart.append(product)

# Function to calculate total
def calculate_total(cart):
    return sum(item['price'] for item in cart)

# Function to decode barcode from image
def decode_barcode(image):
    barcodes = decode(image)
    return [barcode.data.decode('utf-8') for barcode in barcodes]

# Streamlit UI
st.title("Smart Trolley Billing System")

# Use file upload for scanning
st.header("Upload Product Barcode Image")
image_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if image_file is not None:
    # Open the image
    image = Image.open(image_file)
    image = np.array(image)

    # Decode the barcode
    barcodes = decode_barcode(image)

    if barcodes:
        # Check if the scanned barcode corresponds to a product
        scanned_barcode = barcodes[0]  # Take the first barcode found
        product_row = product_df[product_df['barcode'] == scanned_barcode]
        
        if not product_row.empty:
            product = {
                "product_name": product_row['product_name'].values[0],
                "price": product_row['price'].values[0]
            }
            add_to_cart(product)
            st.success(f"{product['product_name']} added to cart!")
        else:
            st.error("Product not found.")
    else:
        st.error("No barcode detected.")

# Display product list
st.header("Available Products")
for index, row in product_df.iterrows():
    st.write(f"**{row['product_name']}** - ₹{row['price']}")
    if st.button(f"Add {row['product_name']} to Cart"):
        add_to_cart({"product_name": row['product_name'], "price": row['price']})
        st.success(f"{row['product_name']} added to cart!")

# Display cart
st.header("Your Cart")
if cart:
    for item in cart:
        st.write(f"{item['product_name']} - ₹{item['price']}")
    total = calculate_total(cart)
    st.write(f"**Total: ₹{total}**")
else:
    st.write("Your cart is empty.")
