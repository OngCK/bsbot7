#---------------------------------------------------------------------------
# Deduce sentiment of the user message
# -------------------------------------
# Model: “distilbert-base-uncased-finetuned-sst-2-english”
#    - uses the DistilBERT architecture 
#    - has been fine-tuned on a dataset called SST-2 for the sentiment analysis task
#----------------------------------------------------------------------------

# ---------------------------
# Function: SentimentResult
# ---------------------------
# input:
#       user_text - text to be analysed for sentiment
# return:
#       sentiment_outcome - "POSITIVE" or "NEGATIVE"
#       sentiment_score - sentiment score value


from transformers import pipeline

def SentimentResult(user_text):

    # obtain the sentiment classification model
    nlp = pipeline("sentiment-analysis")

    # sentiment result
    result = nlp(user_text)[0]

    sentiment_outcome = result['label']
    sentiment_score = result['score']
    
    return sentiment_outcome,sentiment_score;