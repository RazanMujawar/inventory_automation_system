import os
from modules.load_sales import load_sales
from modules.update_inventory import update_inventory
from modules.generate_alerts import generate_alerts
from modules.load_to_sales_table import load_to_sales_table
from modules.file_handler import move_to_processed
from modules.logger import logger
from modules.reports import generate_reports

def run_pipeline():

    files = [
        f for f in os.listdir("data")
        if f.endswith(".csv")
    ]
    print(f"Found {len(files)} files")
    if len(files) == 0:
        print("No files to process. Exiting.")
        return
    
    for file in files:
        
        try:
                logger.info(f"Processing file: {file}")
                
                file_path = os.path.join("data", file)
                    
                sales_df = load_sales(file_path)
                
                logger.info("Sales file loaded")
                
                load_to_sales_table(sales_df)
                
                logger.info("Sales data inserted into sales table")
                
                
                for _, row in sales_df.iterrows():

                    product_id = int(row["product_id"])
                    quantity = int(row["quantity_sold"])

                    update_inventory(product_id, quantity)
                    
                logger.info("Inventory updated")

                generate_alerts()
                
                logger.info("Alerts generated")

                move_to_processed(file_path)
                
                generate_reports()

                logger.info(f"{file} moved to processed folder")

                print(f"{file} processed successfully!")

        except Exception as e:

            logger.error(
                f"Error processing {file}: {str(e)}"
            )

            print(e)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()