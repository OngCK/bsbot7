#---------------------------------------------------------------------------
# Save product review summary requested by user
# ------------------------------------------
# - for actual implementation, the data is to be stored into a database
# - as illustration purpose, 
#   we save the data to an excel file to simulate saving to the database
# - the excel file name is product_review_summary_data.xlsx
# ----------------------------------------------------------------------------

# ---------------------------
# Function: DataStoreProductReviewSummary
# ---------------------------
# input:
#       product_asin,product_review_summary
# return:
#       null


import pandas as pd
from datetime import datetime

def DataStoreProductReviewSummary(product_asin,sentiment_selection,product_review_summary):
    
    # get current date and time
    date_time = datetime.now()

    # read product review summary data from excel file
    df_product_review_summary_data = pd.read_excel("product_review_summary_data.xlsx")
    
    # create new record row    
    new_row = {'date_time':date_time,'product_asin':product_asin, 'sentiment_selection':sentiment_selection,'product_review_summary':product_review_summary}
     
    # append new row to feedback_data    
    df_product_review_summary_data = df_product_review_summary_data.append(new_row,ignore_index=True)
 
    # output to excel file
    df_product_review_summary_data.to_excel("product_review_summary_data.xlsx",index=False)