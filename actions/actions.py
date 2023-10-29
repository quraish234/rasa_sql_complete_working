# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
#from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, UserUtteranceReverted 
import mysql.connector

class SaveChatToMySQL(Action):
    def name(self):
        return "action_save_chat_to_mysql"

    def run(self, dispatcher, tracker, domain):
        # Initialize variables
        user_id = tracker.sender_id
        timestamp = tracker.latest_message.get('time', None)
        message = ""
        bot_response = ""

        # Iterate through tracker events to capture user messages and bot responses
        # Iterate through tracker events to capture user messages and the last bot response
        for event in reversed(tracker.events):
            if event.get("event") == "user":
                message = event.get("text", "")
                break  # Stop when the last user message is found
            elif event.get("event") == "bot":
                bot_response = event.get("text", "")

        # Insert the data into the MySQL database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="qrasa",
            password="killmw234",
            database="rasa"
            
        )
        cursor = conn.cursor()

        insert_query = "INSERT INTO chat_history (user_id, timestamp, message, response) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, timestamp, message, bot_response))
        conn.commit()

        cursor.close()
        conn.close()

        return []
