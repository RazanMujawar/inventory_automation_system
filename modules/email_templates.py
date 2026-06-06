def get_email_template(title, body, color):

    html = f"""
    <html>

    <body style="
        font-family: Arial, sans-serif;
        background-color:#f4f4f4;
        padding:20px;
    ">

        <div style="
            max-width:700px;
            margin:auto;
            background:white;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 2px 10px rgba(0,0,0,0.1);
        ">

            <div style="
                background:{color};
                color:white;
                padding:20px;
                text-align:center;
            ">

                <h1>Lumina & Co.</h1>
                <p>Inventory Automation Platform</p>

            </div>

            <div style="padding:30px;">

                <h2>{title}</h2>

                {body}

            </div>

            <div style="
                background:#f8f9fa;
                padding:15px;
                text-align:center;
                font-size:12px;
                color:#666;
            ">

                Lumina & Co.<br>
                Pune, Maharashtra, India<br>
                inventory@luminaandco.com

            </div>

        </div>

    </body>

    </html>
    """

    return html

def get_alert_email(product_name,
                    current_stock,
                    reorder_level):

    body = f"""
    <p>
        A product has fallen below its reorder threshold.
    </p>

    <table border="1"
           cellpadding="10"
           cellspacing="0">

        <tr>
            <th>Product</th>
            <td>{product_name}</td>
        </tr>

        <tr>
            <th>Current Stock</th>
            <td>{current_stock}</td>
        </tr>

        <tr>
            <th>Reorder Level</th>
            <td>{reorder_level}</td>
        </tr>

    </table>

    <p>
        Please replenish inventory as soon as possible !.
    </p>
    """

    return get_email_template(
        "⚠ Inventory Reorder Alert",
        body,
        "#dc3545"
    )

def get_low_stock_summary_email(
    low_stock_html
):

    body = f"""

    <p>
        The following products require
        replenishment:
    </p>

    {low_stock_html}

    <br>

    <p>
        Please review inventory levels.
    </p>

    """

    return get_email_template(
        "⚠ Low Stock Products",
        body,
        "#dc3545"
    )

  
def get_summary_email(
    processing_date,
    processed_file,
    files_processed,
    sales_records,
    low_stock_count,
    low_stock_html
):

    body = f"""

    <p>
        Daily inventory processing completed successfully.
    </p>

    <table border="1"
        cellpadding="10"
        cellspacing="0">

        <tr>
            <th>Processing Date</th>
            <td>{processing_date}</td>
        </tr>

        <tr>
            <th>Processed File</th>
            <td>{processed_file}</td>
        </tr>

        <tr>
            <th>Files Processed</th>
            <td>{files_processed}</td>
        </tr>

        <tr>
            <th>Sales Records Loaded</th>
            <td>{sales_records}</td>
        </tr>

        <tr>
            <th>Low Stock Products</th>
            <td>{low_stock_count}</td>
        </tr>

    </table>


    <br>

    <h3>Low Stock Products</h3>

    {low_stock_html}

    <br>

    <p>
        Reports Generated:
    </p>

    <ul>
        <li>Inventory Report</li>
        <li>Sales Summary Report</li>
        <li>Low Stock Report</li>
    </ul>

    <div style="
    background:#d1e7dd;
    color:#0f5132;
    padding:15px;
    border-radius:5px;
    font-weight:bold;
    margin-top:15px;
    ">

    ✅ Processing Completed Successfully

    </div>

    """

    return get_email_template(
        "📊 Daily Inventory Processing Report",
        body,
        "#198754"
    )

def get_reminder_email():

    body = """
    
    <p>
        This is a reminder to upload today's sales file
        before the automated inventory processing begins.
    </p>

    <table border="1"
           cellpadding="10"
           cellspacing="0">

        <tr>
            <th>Submission Deadline</th>
            <td>09:00 PM</td>
        </tr>

        <tr>
            <th>Expected Format</th>
            <td>sales_YYYYMMDD.csv</td>
        </tr>

        <tr>
            <th>Upload Location</th>
            <td>data/ folder</td>
        </tr>

    </table>

    <br>

    <p>
        Please ensure today's sales records are uploaded
        before processing begins.
    </p>

    """

    return get_email_template(
        "📊 Daily Sales Submission Reminder",
        body,
        "#0d6efd"
    )