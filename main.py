from multiprocessing.dummy import connection
import os
from modules.load_sales import load_sales
from modules.update_inventory import update_inventory
from modules.generate_alerts import generate_alerts
from modules.load_to_sales_table import load_to_sales_table
from modules.file_handler import move_to_processed
from modules.logger import logger
from modules.reports import generate_reports
from modules.get_low_stock_products import get_low_stock_products
from modules.send_email import send_summary_email
from datetime import datetime
from zoneinfo import ZoneInfo
from modules.email_templates import get_reminder_email
from dotenv import load_dotenv
load_dotenv()
from database.db_connection import get_connection
import streamlit as st
from datetime import datetime
import pandas as pd



def run_pipeline():
    connection = get_connection()

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
                    update_inventory(connection, product_id, quantity) 
                
                logger.info("Inventory updated")

                generate_alerts()
                
                logger.info("Alerts generated")

                move_to_processed(file_path)
                
                generate_reports()
                
                low_stock_products = (
                    get_low_stock_products()
                )

                processing_date = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y %I:%M %p")
                
                send_summary_email(
                processing_date=processing_date,
                processed_file=file,
                files_processed=1,
                sales_records=len(sales_df),
                low_stock_products=low_stock_products
            )

                logger.info(f"{file} moved to processed folder")

                print(f"{file} processed successfully!")
                
                total_products_sold = sales_df["quantity_sold"].sum()
                connection.commit()
                connection.close()        
                
                
                history = pd.DataFrame
                "File Name": file
                "Units Sold": total_products_sold
                "Processed At":datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y %I:%M %p")
                print("Pipeline completed successfully!")
                
                history.to_csv(
                "history.csv",
                mode="a",
                header=not os.path.exists("history.csv"),
                index=False)
                print("History record saved")
                
        except Exception as e:

            logger.error(
                f"Error processing {file}: {str(e)}"
            )
   
if __name__ == "__main__":
    run_pipeline()