import streamlit as st
import pandas as pd
import os

from database.db_connection import get_connection
from main import run_pipeline

st.set_page_config(
    page_title="Lumina & Co.",
    page_icon="📦",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
def get_inventory():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            product_id,
            product_name,
            stock_quantity,
            reorder_level
        FROM products
        """
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def restock_inventory(
    product_name,
    quantity
):
    

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET stock_quantity =
            stock_quantity + %s
        WHERE product_name = %s
        """,
        (
            quantity,
            product_name
        )
    )
    
    
    
    conn.commit()

    cursor.close()
    conn.close()



def save_uploaded_file(uploaded_file):

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_path = os.path.join(
        "data",
        uploaded_file.name
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return file_path


def validate_uploaded_file(df):

    errors = []

    required_columns = [
        "product_id",
        "quantity_sold"
    ]

    for column in required_columns:

        if column not in df.columns:

            errors.append(
                f"Missing column: {column}"
            )

    if len(df) == 0:

        errors.append(
            "File contains no records"
        )

    try:

        df["quantity_sold"] = pd.to_numeric(
            df["quantity_sold"]
        )

    except Exception:

        errors.append(
            "quantity_sold must contain only numbers"
        )

    if "quantity_sold" in df.columns:

        negative_rows = df[
            df["quantity_sold"] < 0
        ]

        if len(negative_rows) > 0:

            errors.append(
                "quantity_sold cannot be negative"
            )

    return errors


def validate_product_ids(df):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id
        FROM products
        """
    )

    valid_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    invalid_ids = []

    for product_id in df["product_id"]:

        if product_id not in valid_ids:

            invalid_ids.append(
                product_id
            )

    return invalid_ids   
    
def show_home():
    st.image(
        "images/logo.png",
        use_container_width=True
    )

    st.subheader("About Us")

    st.write("""
    Lumina & Co. is an Inventory Automation
    Platform designed to streamline
    inventory tracking, sales processing,
    low-stock monitoring, automated alerts,
    and reporting.
    """)

    st.image(
        "images/hero.png",
        use_container_width=True
    )

    st.markdown("---")

st.subheader(
    "🚀 Platform Features"
)

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
        📤 **Sales Upload**

        Upload and validate
        daily sales files.
        """
    )

    st.info(
        """
        📦 **Inventory Management**

        Monitor stock levels
        in real time.
        """
    )

with col2:

    st.info(
        """
        ⚠ **Automated Alerts**

        Receive low stock
        email notifications.
        """
    )

    st.info(
        """
        📊 **Reporting**

        Generate inventory
        and sales reports.
        """
    )
    
    st.subheader("Contact Us")

    st.write("""
    📍 Pune, Maharashtra, India

    📧 inventory@luminaandco.com

    📞 +91-9665069762
    """)
    


def show_upload_sales():

    if "processed" not in st.session_state:

        st.session_state.processed = False

    st.title(
        "📤 Upload Sales"
    )

    uploaded_file = st.file_uploader(
        "Upload Sales CSV",
        type=["csv"],
        key="sales_upload"
    )

    if uploaded_file:

        df = pd.read_csv(
            uploaded_file
        )

        st.success(
            f"{uploaded_file.name} uploaded successfully!"
        )

        errors = validate_uploaded_file(
            df
        )

        invalid_ids = validate_product_ids(
            df
        )

        for pid in invalid_ids:

            errors.append(
                f"Product ID {pid} not found"
            )

        if len(errors) == 0:

            st.success(
                "Validation Passed!"
            )

            if st.button(
                "🚀 Run Inventory Processing"
            ):

                save_uploaded_file(
                    uploaded_file
                )

                with st.spinner(
                    "Processing inventory..."
                ):

                    run_pipeline()

                st.session_state.processed = True

        else:

            st.error(
                "Validation Failed!"
            )

            for error in errors:

                st.error(error)

        if st.session_state.processed:

            st.success(
                "Inventory processing completed!"
            )

            st.balloons()

        st.subheader(
            "Uploaded Data Preview"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    
def show_inventory():

    st.title(
        "📋 Current Inventory"
    )

    inventory = get_inventory()

    inventory_df = pd.DataFrame(
        inventory,
        columns=[
            "Product ID",
            "Product Name",
            "Current Stock",
            "Reorder Level"
        ]
    )

    st.dataframe(
        inventory_df,
        use_container_width=True
    )

def show_restock():

    st.title(
        "📦 Restock Inventory"
    )

    inventory = get_inventory()

    inventory_df = pd.DataFrame(
        inventory,
        columns=[
            "Product ID",
            "Product Name",
            "Current Stock",
            "Reorder Level"
        ]
    )

    selected_product = st.selectbox(
        "Select Product",
        inventory_df["Product Name"]
    )

    restock_quantity = st.number_input(
        "Restock Quantity",
        min_value=1,
        step=1
    )

    if st.button(
        "Update Inventory"
    ):

        restock_inventory(
            selected_product,
            restock_quantity
        )

        st.success(
            f"{selected_product} restocked successfully!"
        )
    

left_col, divider_col, right_col = st.columns(
    [1.2, 0.05, 4]
)

with divider_col:
    st.markdown(
        """
        <div style="
            border-left:1px solid #444;
            height:100vh;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )
    
with left_col:

    st.image(
        "images/logo.png",
        use_container_width=True
    )

    st.markdown("---")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"

    if st.button("📤 Upload Sales"):
        st.session_state.page = "Upload"

    if st.button("📋 Show Inventory"):
        st.session_state.page = "Inventory"

    if st.button("📦 Restock Inventory"):
        st.session_state.page = "Restock"
        
with right_col:

    if st.session_state.page == "Home":
        show_home()

    elif st.session_state.page == "Upload":
        show_upload_sales()

    elif st.session_state.page == "Inventory":
        show_inventory()

    elif st.session_state.page == "Restock":
        show_restock()