import webbrowser
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from database.db_connection import get_connection
from main import run_pipeline
from reports.reports import get_report_data
from dotenv import load_dotenv
load_dotenv()
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Lumina & Co.",
    page_icon="📦",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "Home"
 
 
@st.cache_data(ttl=60)    
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
    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.image(
        "images/logo.png",
        width=550
    )
    st.subheader("About Us")

    st.write("""
    Lumina & Co. is an Inventory Automation
    Platform designed to streamline
    inventory tracking, sales processing,
    low-stock monitoring, automated alerts,
    and reporting.
    """)

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.image(
        "images/hero.png",
        width=800
    )
    st.markdown("---")

    st.subheader(
        "🚀 Platform Features" 
    )

    st.markdown("""


    **1. 📤 Sales Upload**

    &nbsp;&nbsp;&nbsp;&nbsp; - Upload and validate daily sales files.

    <br>

    **2. 📦 Inventory Management**

    &nbsp;&nbsp;&nbsp;&nbsp; - Monitor stock levels in real time.

    <br>

    **3. ⚠ Automated Alerts**

    &nbsp;&nbsp;&nbsp;&nbsp; - Receive low stock notifications.

    <br>

    **4. 📊 Power BI Dashboard**

    &nbsp;&nbsp;&nbsp;&nbsp; - Visualize inventory and sales analytics.
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.subheader("🔄 How It Works")
    st.markdown("""

        1. Upload 
        
        2. Validate

        3. Update

        4. Alerts
        
        5. Reports
        """)

    
    st.markdown("---")
    
    st.subheader("System Information")

    st.write("""
        
    - **Database**      : MySQL
    
    - **Analytics**     : Power BI
    
    - **Alerts**        : Email Notifications
    
    - **Deployment**    : Streamlit
    
    - **Refresh Times** : 9AM | 12PM | 3PM | 6PM | 9PM
        """)
    
def show_upload_sales():

    if "processed" not in st.session_state:
        st.session_state.processed = False

    st.title("📤 Upload Sales")
    if "last_run" in st.session_state:

        st.info(f"✅ Last inventory processing completed at {st.session_state['last_run']}")
    col1, col2 = st.columns([2,3])

    with col1:

        st.subheader("Upload Today's Sales")

        uploaded_file = st.file_uploader(
            "Choose Sales CSV File",
            type=["csv"],
            key="sales_upload"
        )
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)

            except Exception:

                st.error(
        """
        ❌ Invalid File

        Unable to read the uploaded file.

        Please upload a valid CSV file.
        """
)

                return

            st.success(
                f"{uploaded_file.name} uploaded successfully!"
            )

            errors = validate_uploaded_file(df)

            if "product_id" in df.columns:

                invalid_ids = validate_product_ids(df)

                for pid in invalid_ids:
                    errors.append(
                        f"Product ID {pid} not found"
                    )

            if len(errors) == 0:

                st.success(
                    "Validation Passed!"
                )

                if st.button("🚀 Run Inventory Processing"):
                    save_uploaded_file(uploaded_file)
                    
                    status_box = st.empty()  # reserve a spot on screen
                    
                    with st.spinner("Processing inventory..."):
                        run_pipeline()
                    
                    st.cache_data.clear()
                    
                    status_box.success("✅ Inventory processing completed successfully!")
                    st.balloons()
                    st.stop()  # ← stops Streamlit from rerunning further

                                    

            else:

                st.error(
                    """
                    ❌ No Relevant Sales Data Found

                    Required columns:
                    • product_id
                    • quantity_sold

                    Please upload a valid sales file.
                    """
                )

                for error in errors:
                    st.error(error)

    with col2:
        st.subheader("Uploaded Data Preview")
        if uploaded_file:
            st.dataframe(df,width="stretch", hide_index = True)
        


def highlight_stock(row):

    stock = row["Current Stock"]
    reorder = row["Reorder Level"]
    
    if stock < reorder:
        return [
    "background-color:#f8d7da; color:#111111"
] * len(row)

    elif stock <= reorder + 5:
        return [
    "background-color:#fff3cd; color:#111111"
] * len(row)

    else:
        return [
    "background-color:#d1e7dd; color:#111111"
] * len(row)
        
        
def show_inventory():

    st.title(
        "📋 Current Inventory"
    )

    inventory = get_inventory()

    st.caption("""
    🟢 Healthy Stock
    🟡 Near Reorder Level
    🔴 Below Reorder Level
    """)
    
    inventory_df = pd.DataFrame(
        inventory,
        columns=[
            "Product ID",
            "Product Name",
            "Current Stock",
            "Reorder Level"
        ]
    )

    styled_df = inventory_df.style.apply(
    highlight_stock,
    axis=1
)

    st.dataframe(styled_df,width="stretch")
    low_stock_items = inventory_df[inventory_df["Current Stock"]<=inventory_df["Reorder Level"]]

    if not low_stock_items.empty:

        products = ", ".join(
            low_stock_items["Product Name"]
        )

        st.warning(
            f"⚠ Low Stock Products: {products}"
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

    if st.button("Update Inventory"):

        restock_inventory(
            selected_product,
            restock_quantity
        )

        st.cache_data.clear()

        st.success(
            f"{selected_product} restocked successfully!"
        )

def show_reports():

    st.title(
        "📑 Reports"
    )

    (
        total_products,
        total_stock,
        low_stock,
        open_alerts
    ) = get_report_data()
    
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📦 Total Products",
            total_products
        )

    with col2:
        st.metric(
            "📈 Total Stock",
            total_stock
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "⚠ Low Stock Items",
            low_stock
        )

    with col4:
        st.metric(
            "🚨 Open Alerts",
            open_alerts
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

    styled_df = inventory_df.style.apply(
    highlight_stock,
    axis=1
)    
    st.subheader(" 🚨 Product that need to be Reordered")
    low_stock_items = inventory_df[inventory_df["Current Stock"]<=inventory_df["Reorder Level"]]

    st.dataframe(
    low_stock_items[
        [
            "Product Name",
            "Current Stock",
            "Reorder Level"
        ]
    ]
)
    
    st.markdown("---")

def show_history():

    st.title("📜 Processing History")

    if not os.path.exists("history.csv"):
        st.info("No processing history available.")
        return

    try:

        history_df = pd.read_csv(
            "history.csv"
        )

        st.dataframe(
            history_df,
            hide_index=True,
            width="stretch"
        )

    except Exception:

        st.warning(
            "No history records found."
        )
        return
    
    col1, col2 = st.columns(2)

    with col1:

        today = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y")

        today_files = history_df[history_df["Processed At"].str.contains(today)]

        st.metric("Today's Files Processed",len(today_files))

    with col2:
        st.metric("Today's Units Sold",history_df["Units Sold"].sum())

    

def get_next_refresh():

    now = datetime.now()

    refresh_hours = [
        9,
        12,
        15,
        18,
        21
    ]

    for hour in refresh_hours:

        refresh_time = now.replace(
            hour=hour,
            minute=0,
            second=0,
            microsecond=0
        )

        if refresh_time > now:

            return refresh_time

    return (
        now + timedelta(days=1)
    ).replace(
        hour=9,
        minute=0,
        second=0,
        microsecond=0
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
        "images/logo without sub.png",
        width=180
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
        
    if st.button("📑 Reports"):
        st.session_state.page = "Reports"
    
    st.link_button(
        "📊 Open Power BI Dashboard", https://app.powerbi.com/view?r=eyJrIjoiM2RkYTU1MDgtMmZlZC00MzAwLWE1NzQtYTA4ZTRjZTU5Mjk3IiwidCI6IjkzNjgyYTAyLTNmNjQtNDllNi1hYjY5LTU5NTAxNWJiNTllYyJ9
    )

    if st.button("📜 History"):
        st.session_state.page = "History"

    next_refresh = get_next_refresh()

    remaining = (
        next_refresh -
        datetime.now()
    )

    hours = remaining.seconds // 3600

    minutes = (
        remaining.seconds % 3600
    ) // 60

    st.info(
        f"""
        📊 Next Power BI Refresh
        
        ⏱ {hours}h {minutes}m
        
        9AM  •  12PM  •  3PM  •  6PM  •  9PM"""
    )
        
with right_col:

    if st.session_state.page == "Home":
        show_home()

    elif st.session_state.page == "Upload":
        show_upload_sales()

    elif st.session_state.page == "Inventory":
        show_inventory()

    elif st.session_state.page == "Restock":
        show_restock()
        
    elif st.session_state.page == "Reports":
        show_reports()
        
    elif st.session_state.page == "Power BI Dashboard":
        show_reports()
    elif st.session_state.page == "History":
        show_history()