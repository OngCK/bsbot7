#---------------------------------------------------------------------------
# Save user's feedback and sentiment result
# ------------------------------------------
# - for actual implementation, the data is to be stored into a database
# - as illustration purpose, 
#   we save the data to an excel file to simulate saving to the database
# - the excel file name is feedback_data.xlsx
# ----------------------------------------------------------------------------

# ---------------------------
# Function: DataStoreFeedback
# ---------------------------
# input:
#       user_message,sentiment_outcome,sentiment_score
# return:
#       null


import pandas as pd
from datetime import datetime

def DataStoreFeedback(user_message,sentiment_outcome,sentiment_score):
    
    # get current date and time
    date_time = datetime.now()

    # read feedback data from excel file
    df_feedback_data = pd.read_excel("feedback_data.xlsx")

    # create new record row    
    new_row = {'date_time':date_time,'user_message':user_message, 'sentiment_outcome':sentiment_outcome , 'sentiment_score': sentiment_score}

    # append new row to feedback_data    
    df_feedback_data = df_feedback_data.append(new_row,ignore_index=True)
    
    # output to excel file
    df_feedback_data.to_excel("feedback_data.xlsx",index=False)
