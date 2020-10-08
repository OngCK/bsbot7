# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


from typing import Any, Dict, List, Text, Union
  
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

import pandas as pd

#---------------------------------------------------------------------
# import customised functions from py files
#---------------------------------------------------------------------
from get_sentiment import SentimentResult
from get_product_review_summary import ProductReviewSummary
# from get_answer import Answer
from data_store_feedback import DataStoreFeedback
from data_store_product_review_summary import DataStoreProductReviewSummary
# from data_store_question_answer import DataStoreQuestionAnswer

#-------------------------------------------------------------------------------------
# Handle actions for feedback form 
# -------------------------------------
# Required slot to be input via the form: feedback
# Upon submitted the form (ie, once the required slot is filled up),
#   call customised function get_sentiment.SentimentResult to obtain
#   the sentiment outcome of the user feedback  
#---------------------------------------------------------------

class FeebbackForm(FormAction):

    def name(self) -> Text:
        """ unique form ID """

        return "feedback_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """ list of slots that the form has to fill """

        return ["feedback"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
             
        return {  
           "feedback":[self.from_text()]
        }

 
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        """ what to do after slots are filled """

        # retrieve user feedback from slot
        feedback = tracker.get_slot('feedback')
        print ("feedback - ", feedback)

        # call customised function get_sentiment.SentimentResult
        # to derive the sentiment result
        # input: text of user's feedback
        # return: sentiment_outcome :- 'POSITIVE' or 'NEGATIVE'
        #         sentiment_score 
        sentiment_outcome, sentiment_score = SentimentResult(feedback)
        print ("call sentiment")

        # for testing display... will remove for implementation
        output_test = "Sentiment is {}".format(sentiment_outcome)
        print ("sentiment out- ",output_test)

        # call customised function data_store_feedback.DataStoreFeedback
        # to store the data to database
        DataStoreFeedback(feedback,sentiment_outcome,sentiment_score)

        # response message with selection button, depending on the sentiment outcome
        if sentiment_outcome == 'NEGATIVE':
            message = output_test + " / " + "Would you like to talk to our staff to handle your case?"
            buttons = [{"title": "Yes, please", "payload": '/transfer_to_cso'}, {"title":"No, I am done", "payload": '/end_feedback'}]
            dispatcher.utter_button_message(message, buttons)
        else: 
            message = output_test + " / " + "Got it. More feedback?"
            buttons = [{"title": "Yes, more feedback", "payload": '/chat_feedback'}, {"title":"No, I am done", "payload": '/end_feedback'}]
            dispatcher.utter_button_message(message, buttons)
        
        # clear slots when return
        return [AllSlotsReset()]
    
#------------------------------------------------------------------------------
# Action: Transfer the user to customer service office
# ----------------------------------------------------
# As the actual implementation of the transfer is out-of-scope of this project,
# the action only display a dummy message to similuate the action
#------------------------------------------------------------------------------
class ActionTransferToCSO(Action):

    def name(self) -> Text:
        return "action_transfer_to_cso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="(transferred)")

        return []



#---------------------------------------------------------------------------
# Get product ASIN and Store to the slot
# -------------------------------------
# The slot, product_asin, will be used by action_get_product_review_summary
#--------------------------------------------------------------------------
class ActionGetProductASIN(Action):

    def name(self) -> Text:
        return "action_get_product_asin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # feed in the message input by user (product selected by user)
        product = tracker.latest_message["text"]
        # change to upper case
        product = product.upper()

        # get the ASIN of the product from excel 
        df_product_review_asin = pd.read_excel("product_review_asin.xlsx")
        df_product_review_asin_row = df_product_review_asin.loc[df_product_review_asin["Product"] == product]
        product_asin = df_product_review_asin_row.iloc[0]['ASIN']

        print ("product_asin -", product_asin)
      
        # store into the slot
        return [SlotSet("asin", product_asin)] 


#--------------------------------------------------------------------------
# Store review tye 'good' to the slot
# The slot, review_type, will be used by action_get_product_review_summary
# -------------------------------------------------------------------------
class ActionSlotsetProductReviewTypeGood(Action):

    def name(self) -> Text:
        return "action_slotset_product_review_type_good"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("review_type", "good")] 


#--------------------------------------------------------------------------
# Store review tye 'bad' to the slot
# The slot, review_type, will be used by action_get_product_review_summary
# -------------------------------------------------------------------------
class ActionSlotsetProductReviewTypeBad(Action):

    def name(self) -> Text:
        return "action_slotset_product_review_type_bad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("review_type", "bad")] 


#--------------------------------------------------------------------------
# Store review tye 'all' to the slot
# The slot, review_type, will be used by action_get_product_review_summary
# -------------------------------------------------------------------------
class ActionSlotsetProductReviewTypeAll(Action):

    def name(self) -> Text:
        return "action_slotset_product_review_type_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("review_type", "all")] 


#-------------------------------------------------------------------------------------
# Get product review summary
# -------------------------------------
# Call customised get_product_review_summary.ProductReviewSummary function 
# input: product ASIN 
# return: product review summary
#-----------------------------------------------------------------
class ActionGetProductReviewSummary(Action):

    def name(self) -> Text:
        return "action_get_product_review_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get product ASIN and review type from slots
        product_asin = tracker.get_slot('asin')
        product_review_type = tracker.get_slot('review_type')

        print ("get slot asin - ",product_asin)
        print ("review type - ",product_review_type)

        # set the value of sentiment selection which is required as an input
        # for customised function get_product_review_summary.ProductReviewSummary
        if product_review_type == 'good':
            sentiment_selection = 'good'
        elif product_review_type == 'bad':
            sentiment_selection = 'bad'
        else:
            sentiment_selection = 'all'

        # call customised function get_product_review_summary.ProductReviewSummary
        # to derive the product review summary
        product_review_summary = ProductReviewSummary(product_asin,sentiment_selection)

        print ("summary - ", product_review_summary)

        # call customised function data_store_summary.DataStoreSummary
        # to store the data to database
        DataStoreProductReviewSummary(product_asin,sentiment_selection,product_review_summary)

        # response message with selection button   
        if product_review_type == 'good':
            message = "Below is the summary of good reviews of the product: " + "\n" + product_review_summary
            buttons = [{"title": "View Bad Reviews", "payload": '/review_type_bad'}, {"title": "View All Reviews", "payload": '/review_type_all'}, {"title":"I Am Done", "payload": '/chat_end'}]
        elif product_review_type == 'bad':
            message = "Below is the summary of bad reviews of the product: " + "\n" + product_review_summary
            buttons = [{"title": "View Good Reviews", "payload": '/review_type_good\n'}, {"title": "View All Reviews", "payload": '/review_type_all'}, {"title":"I Am Done", "payload": '/chat_end'}]
        else: 
            message = "Below is the summary of all reviews of the product: " + "\n" + product_review_summary
            buttons = [{"title": "View Good Reviews", "payload": '/review_type_good'}, {"title": "View Bad Reviews", "payload": '/review_type_bad'}, {"title":"I Am Done", "payload": '/chat_end'}]
        
        dispatcher.utter_button_message(message, buttons)
        
        return [] 


#-------------------------------------------------------------------------------------
# Handle actions for question form 
# -------------------------------------
# Required slot to be input via the form: question
# Upon submitted the form (ie, once the required slot is filled up),
#   call customised function get_answer.Answer to obtain the answer
#---------------------------------------------------------------
class QuestionForm(FormAction):

    def name(self) -> Text:
        """ unique form ID """

        return "question_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """ list of slots that the form has to fill """

        return ["product","question"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where the first match will be picked"""
    
        return {
            "product":[self.from_text()],
            "question":[self.from_text()]
        }
          
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        """ what to do after slots are filled """

        # retrieve user product from slot
        product = tracker.get_slot('product')
        # change to upper case
        product = product.upper()
        print ("product - ", product)

        # retrieve user question from slot
        question = tracker.get_slot('question')
        print ("question - ", question)
       
        # get the context of the product from excel 
        df_product_context = pd.read_excel("product_context.xlsx")
        df_product_context_row = df_product_context.loc[df_product_context["Product"] == product]
        context = df_product_context_row.iloc[0]['Context']

        print ("context -", context)

        #------------------------------------------------
        # call customised function get_answer.Answer
        # to deduce the answer based on the question
        # input: question
        # return: answer
        #-------------------------------------------------
        # answer = Answer(question)
      
        # for testing display
        answer = "This is my BS answer!"

        # call customised function excel_data_store_answer.DataStoreAnswer
        # to store the data to database
        # DataStoreQuestionAnswer(question,answer)

        # button selection to ask more question or end the chat
        message = answer + "\n" + "..... Do you want to ask more question for this product?"
        buttons = [{"title": "Yes, more question", "payload": '/chat_shopping'}, {"title":"No, I am done", "payload": '/chat_end'}]
        dispatcher.utter_button_message(message, buttons)

        # clear slots when return
        return [AllSlotsReset()]
    

