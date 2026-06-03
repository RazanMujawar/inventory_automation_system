from modules.load_sales import load_sales
from modules.update_inventory import update_inventory
from modules.generate_alerts import generate_alerts

def run_pipeline():

    sales_df = load_sales()

    for _, row in sales_df.iterrows():

        product_id = int(row["product_id"])
        quantity = int(row["quantity_sold"])

        update_inventory(product_id, quantity)

    generate_alerts()

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()