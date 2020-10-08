## greet
* greet
  - utter_what_to_chat

## say goodbye
* goodbye
  - utter_goodbye

## feedback - from button
* greet
  - utter_what_to_chat
* chat_feedback
  - feedback_form
  - Form{"name":"feedback_form"}
  - action_deactivate_form
* chat_end
  - utter_chat_end

## feedback - end
* end_feedback
  - utter_end_feedback

## feedback - to cso
* transfer_to_cso
  - utter_transfer_to_cso
  - action_transfer_to_cso

## shopping - from button
* greet
  - utter_what_to_chat
* chat_shopping
  - question_form
  - Form{"name":"question_form"}
  - action_deactivate_form
* chat_end
  - utter_chat_end

## chat end
* chat_end
  - utter_chat_end

## product review summary - from button
* greet
  - utter_what_to_chat
* chat_product_review_summary
  - utter_get_product
* get_product_review_selection
  - action_get_product_asin
  - utter_get_review_type
* chat_end
  - utter_chat_end

## view good review - from button
* review_type_good
  - action_slotset_product_review_type_good
  - action_get_product_review_summary

## view bad review - from button
* review_type_bad
  - action_slotset_product_review_type_bad
  - action_get_product_review_summary

## view all review - from button
* review_type_all
  - action_slotset_product_review_type_all
  - action_get_product_review_summary

