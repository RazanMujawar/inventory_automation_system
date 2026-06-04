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
        Please replenish inventory as soon as possible.
    </p>
    """

    return get_email_template(
        "⚠ Inventory Reorder Alert",
        body,
        "#dc3545"
    )