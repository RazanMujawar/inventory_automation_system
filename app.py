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
from modules.add_product import (
    add_product,
    product_exists
)
from modules.add_category import (
    add_category,
    category_exists,
    get_categories
)
from modules.manage_product import (
    get_products,
    get_product_details,
    update_product,
    product_exists_except_current
)
from modules.audit_log import (
    add_audit_log,
    get_audit_logs
)

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
            category,
            price,
            stock_quantity,
            reorder_level
        FROM products
        WHERE status='Active'
        ORDER BY product_name
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

def validate_inactive_products(df):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name
        FROM products
        WHERE status='Inactive'
    """)

    inactive_products = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    inactive_found = []

    for pid in df["product_id"]:

        if pid in inactive_products:

            inactive_found.append(
                (
                    pid,
                    inactive_products[pid]
                )
            )

    return inactive_found
 
def show_home():
    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.image(
        "images/logo.png",
        width=550
    )
    st.markdown("---")
    (
    total_products,
    total_stock,
    low_stock,
    open_alerts
    ) = get_report_data()

    history_df = pd.read_csv("history.csv")

    history_df["Processed At"] = pd.to_datetime(
        history_df["Processed At"],
        format="%d-%b-%Y %I:%M %p"
    )

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    today_history = history_df[
        history_df["Processed At"].dt.date == today
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📦 Products",
            total_products
        )

    with col2:
        st.metric(
            "📈 Total Stock",
            total_stock
        )

    with col3:
        st.metric(
            "🚨 Open Alerts",
            open_alerts
        )

    with col4:
        st.metric(
            "📂 Files Today",
            len(today_history)
        )
    
    st.markdown("---")

    st.subheader("📖 About Lumina & Co.")

    st.write("""
    Lumina & Co. is an Inventory Automation Platform
    designed to automate sales processing, inventory
    tracking, low-stock monitoring, audit logging,
    and Power BI reporting.

    The platform validates uploaded sales files,
    updates inventory automatically, generates alerts,
    maintains activity history, and provides real-time
    business insights through interactive dashboards.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.image(
        "images/hero.png",
        width=800
    )
    st.markdown("---")
    
    left, right = st.columns(2)
    with left:

        st.subheader("🛠 Technology Stack")

        st.markdown("""
            - 🐍 Python

            - 🌐 Streamlit

            - 🗄️ MySQL

            - 📊 Power BI

            - 🐼 Pandas

            - 📧 SMTP Email

            - 🔄 ETL Pipeline

            - 📝 Audit Logs
        """)
    
    with right:

        st.subheader("📜 Recent Activity")
        logs = get_audit_logs()
        if logs:

            recent_logs = pd.DataFrame(logs).head(2)

            for _, row in recent_logs.iterrows():

                st.markdown(
                    f"""
        **{row['action_type']}**

        {row['description']}

        <small>{row['created_at']}</small>

        ---
        """,
                    unsafe_allow_html=True
                )

        else:

            st.info("No recent activity.")
        
    
    st.markdown("---")  
    

    st.subheader(
        "🚀 Platform Features" 
    )
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown("""
            <div style="text-align:center; line-height:1.5; font-size:22px;">

            <b>📤 Upload Sales File</b>

            <div style="font-size:24px;">↓</div>

            <b>✅ Validate Data</b>

            <div style="font-size:24px;">↓</div>

            <b>📦 Update Inventory</b>

            <div style="font-size:24px;">↓</div>

            <b>🚨 Generate Alerts</b>

            <div style="font-size:24px;">↓</div>

            <b>📑 Generate Reports</b>

            <div style="font-size:24px;">↓</div>

            <b>📊 Power BI Dashboard</b>

            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        """
    <div style='text-align:center;color:gray;font-size:14px;'>

    Inventory Automation Platform • Version 1.0

    Built with ❤️ using Python • Streamlit • MySQL • Power BI

    © 2026 Lumina & Co. by Razan Mujawar

    </div>
    """,
        unsafe_allow_html=True
    )
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
                inactive_products = validate_inactive_products(df)

                for pid, name in inactive_products:

                    errors.append(
                        f"Inactive Product: {name} (ID: {pid})"
                    )
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
                "Category",
                "Price",
                "Current Stock",
                "Reorder Level"
            ]
    )

    styled_df = inventory_df.style.apply(
    highlight_stock,
    axis=1
)

    st.dataframe(styled_df,width="stretch", hide_index=True)
    low_stock_items = inventory_df[inventory_df["Current Stock"]<=inventory_df["Reorder Level"]]

    if not low_stock_items.empty:

        products = ", ".join(
            low_stock_items["Product Name"]
        )

        st.warning(
            f"⚠ Low Stock Products: {products}"
        )
        

def show_add_product():

    st.title("➕ Add Product")
    if "product_added" in st.session_state:

        st.success(st.session_state.product_added)

        del st.session_state.product_added

    col1, col2 , col3= st.columns([2,2,1])

    with col1:

        category = st.selectbox(
            "Category",
            get_categories()
        )

    with col2:

        new_category = st.text_input(
        "Create New Category",
        key="new_category")
        
    with col3:
        st.write("")
        st.write("")
        if st.button(
            "➕ Add Category",
            key="add_category_btn"
        ):

            new_category = " ".join(
                new_category.strip().split()
            )

            if new_category == "":

                st.error(
                    "Enter category name"
                )

            elif len(new_category) > 100:

                st.error(
                    "Maximum 100 characters"
                )

            elif category_exists(
                new_category
            ):

                st.error(
                    "Category already exists"
                )

            else:

                add_category(
                    new_category
                )
                add_audit_log(
                    "CREATE_CATEGORY",
                    f"Created new category '{new_category}'."
                )
                st.success("Category Added!")

                del st.session_state["new_category"]

                st.rerun()
    
    left, right = st.columns(2)

    with left:

        product_name = st.text_input(
            "Product Name"
        )

    with right:

        price = st.number_input(
            "Price",
            min_value=0.0,
            step=1.0
        )

    left, right = st.columns(2)

    with left:

        stock_quantity = st.number_input(
            "Initial Stock Quantity",
            min_value=0
        )

    with right:

        reorder_level = st.number_input(
            "Reorder Level",
            min_value=0
        )

    left, center, right = st.columns([2,1,2])
    with center:

        if st.button("➕ Add Product",key="add_product_submit"):

            if product_name.strip() == "":
                st.error(
                    "Product name is required"
                )
            elif len(product_name) > 100:
                st.error(
                    "Product name cannot exceed 100 characters"
                )
                
            elif product_exists(product_name):
                st.error(
                    "Product already exists"
                )
            elif price <= 0:
                st.error(
                    "Price must be greater than 0"
                )

            elif reorder_level <= 0:
                st.error(
                    "Reorder level must be greater than 0"
                )
            else:

                product_id = add_product(
                    product_name,
                    category,
                    price,
                    stock_quantity,
                    reorder_level
                )
                add_audit_log(
                    "ADD_PRODUCT",
                    f"Added Product ID {product_id} - '{product_name}' in category '{category}' with price ₹{price:.2f}."
                )
                

            st.session_state.product_added = (f"✅ Product added successfully! Product ID: {product_id}")
            st.cache_data.clear()
            st.rerun()



def show_manage_products():

    st.title("🛠 Manage Products")
    products = get_products()
    
    if st.session_state.get(
    "product_updated",
    False):

        st.success(
            "✅ Product updated successfully!"
        )

        st.session_state.product_updated = False
    
    if not products:
        st.warning("No products found.")
        return
    
    
    
    product_options = {
        f"{pid} - {name}": pid
        for pid, name in products
    }

    selected = st.selectbox(
        "Select Product",
        list(product_options.keys())
    )
    
    product_id = product_options[selected]

    product = get_product_details(product_id)
        
    if product["status"] == "Active":

            st.success("🟢 Current Status : Active")

    else:

            st.error("🔴 Current Status : Inactive")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.text_input(
                "Product ID",
                value=product["product_id"],
                disabled=True
            )
    with right: 
        product_name = st.text_input(
            "Product Name",
            value=product["product_name"]
        )
    with left: 
        categories = get_categories()

        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(product["category"])
        )
    with right: 
        price = st.number_input(
            "Price",
            min_value=0.01,
            value=float(product["price"])
        )
    with left:
        stock_quantity = st.number_input(
            "Stock Quantity",
            value=int(product["stock_quantity"]),
            disabled=True
        )
    with right:
        reorder_level = st.number_input(
            "Reorder Level",
            min_value=1,
            value=int(product["reorder_level"])
        )
    with left: 
        status = st.selectbox(
        "Status",
        ["Active", "Inactive"],
        index=0 if product["status"] == "Active" else 1
        )
    with right: 
        st.write("")
        st.write("")
        if st.button(
            "💾 Save Changes",
            key="update_product_btn"
        ):

            product_name = " ".join(
                product_name.strip().split()
            )

            if product_name == "":

                st.error("Product name is required.")

            elif len(product_name) > 100:

                st.error(
                    "Maximum 100 characters allowed."
                )

            elif product_exists_except_current(
                product_name,
                product_id
            ):

                st.error(
                    "Product already exists."
                )

            else:
                
                old_name = product["product_name"]
                old_category = product["category"]
                old_price = product["price"]
                old_reorder = product["reorder_level"]
                old_status = product["status"]

                changes = []

                if old_name != product_name:
                    changes.append(
                        f"Name: {old_name} → {product_name}"
                    )

                if old_category != category:
                    changes.append(
                        f"Category: {old_category} → {category}"
                    )

                if old_price != price:
                    changes.append(
                        f"Price: ₹{old_price} → ₹{price}"
                    )

                if old_reorder != reorder_level:
                    changes.append(
                        f"Reorder Level: {old_reorder} → {reorder_level}"
                    )

                if old_status != status:
                    changes.append(
                        f"Status: {old_status} → {status}"
                    )

                if not changes:

                    st.info("No changes detected.")

                    return

                update_product(
                    product_id,
                    product_name,
                    category,
                    price,
                    reorder_level,
                    status
                )
                
                description = (
                    f"Product ID: {product_id}\n"
                    f"Product: {old_name}\n\n"
                    + "\n".join(changes)
                )

                add_audit_log(
                    "UPDATE_PRODUCT",
                    description
                )

                st.cache_data.clear()

                st.session_state.product_updated = True

                st.rerun()
        
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
            "Reorder Level",
            "Price",
            "Category"
        ]
    )
    
    left, right = st.columns(2)

    with left:
        selected_product = st.selectbox(
            "Select Product",
            inventory_df["Product Name"]
        )
    with right:
        restock_quantity = st.number_input(
            "Restock Quantity",
            min_value=1,
            step=1
        )
        
    left, center, right = st.columns([2,1,2])
    with center:
        if st.button("Update Inventory"):

            restock_inventory(
                selected_product,
                restock_quantity
            )
            add_audit_log("RESTOCK_PRODUCT",f"Restocked '{selected_product}' by {restock_quantity} units.")
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
    
    
    history_df = pd.read_csv("history.csv")

    history_df["Processed At"] = pd.to_datetime(
        history_df["Processed At"],
        format="%d-%b-%Y %I:%M %p"
    )

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    today_history = history_df[
        history_df["Processed At"].dt.date == today
    ]
    col1, col2, col3 = st.columns(3)

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
    with col3:
        st.metric(
            "⚠ Low Stock Items",
            low_stock
        )
    col4, col5, col6= st.columns(3)
    with col6:
        st.metric(
            "🚨 Open Alerts",
            open_alerts
        )
        
    with col4:
        st.metric(
            "📤 Files Processed Today",
            len(today_history)
        )

    with col5:
        st.metric(
            "📊 Units Sold Today",
            int(today_history["Units Sold"].sum())
        )    
        inventory = get_inventory()
        
    with st.expander("📂 View Today's Processed Files"):

        if today_history.empty:

            st.info(
                "No files processed today."
            )

        else:

            st.dataframe(
                today_history[
                    [
                        "File Name",
                        "Units Sold",
                        "Processed At"
                    ]
                ],
                hide_index=True,
                width="stretch"
            )
            
    inventory_df = pd.DataFrame(
        inventory,
        columns=[
            "Product ID",
            "Product Name",
            "Category",
            "Price",
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
    ], hide_index=True
)
    
    st.markdown("---")

def show_history():

    st.title("📜 Audit Logs")

    logs = get_audit_logs()

    if not logs:

        st.info("No audit logs available.")
        return

    logs_df = pd.DataFrame(logs)

    logs_df = logs_df.rename(
        columns={
            "log_id": "Log ID",
            "action_type": "Action",
            "description": "Description",
            "created_at": "Timestamp"
        }
    )

    logs_df = logs_df[
        [
            "Log ID",
            "Action",
            "Description",
            "Timestamp"
        ]
    ]

    st.dataframe(
        logs_df,
        width="stretch",
        hide_index=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        today = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).date()

        today_logs = pd.to_datetime(
            logs_df["Timestamp"]
        ).dt.date == today

        st.metric(
            "Today's Activities",
            today_logs.sum()
        )
   

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
            height:250vh;
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

    if st.button("➕ Add Product"):
        st.session_state.page = "Add Product"
        
    if st.button("🛠 Manage Products"):
        st.session_state.page = "Manage Products"
    
    if st.button("📦 Restock Inventory"):
        st.session_state.page = "Restock"
        
    if st.button("📑 Reports"):
        st.session_state.page = "Reports"
    
    if st.button("📜 Audit Logs"):
        st.session_state.page = "Audit Logs"
    
    st.link_button(
        "📊 Open Power BI Dashboard",
        "https://app.powerbi.com/view?r=eyJrIjoiM2RkYTU1MDgtMmZlZC00MzAwLWE1NzQtYTA4ZTRjZTU5Mjk3IiwidCI6IjkzNjgyYTAyLTNmNjQtNDllNi1hYjY5LTU5NTAxNWJiNTllYyJ9"
    )

    

    
        
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
        
    elif st.session_state.page == "Add Product":
        show_add_product()
    
    elif st.session_state.page == "Manage Products":
        show_manage_products() 
        
    elif st.session_state.page == "Restock":
        show_restock()
        
    elif st.session_state.page == "Reports":
        show_reports()
    
    elif st.session_state.page == "Audit Logs":
        show_history()
            
    elif st.session_state.page == "Power BI Dashboard":
        show_reports()
    