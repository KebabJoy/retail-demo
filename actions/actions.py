from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3

# change this to the location of your SQLite file
path_to_db = "actions/example.db"


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]

        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe)

        # retrieve sqlite row
        data_row = cursor.fetchone()

        if data_row:
            # provide in stock message
            dispatcher.utter_message(response="utter_in_stock")
            connection.close()

            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(response="utter_no_stock")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]


class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_open_feedback")
        dispatcher.utter_message(response="utter_survey_end")
        return [SlotSet("survey_complete", True)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # convert tuple to list
            data_list = list(data_row)

            # respond with order status
            dispatcher.utter_message(response="utter_order_status", status=data_list[5])
            connection.close()
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response="utter_no_order")
            connection.close()
            return []


class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("cancelled"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm cancellation
            dispatcher.utter_message(response="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response="utter_no_order")
            connection.close()
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = ["returning", (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm return
            dispatcher.utter_message(response="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response="utter_no_order")
            connection.close()
            return []


class GiveName(Action):
    def name(self) -> Text:
        return "action_give_name"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        evt = BotUttered(
            text="my name is bot? idk",
            metadata={
                "nameGiven": "bot"
            }
        )

        return [evt]


class SubmitReview(Action):
    def name(self) -> Text:
        return "action_submit_review"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        text = tracker.get_slot("review_text")

        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO reviews (email, text) VALUES(?,?)", [email, text])
        connection.commit()
        connection.close()

        dispatcher.utter_message(response="utter_review_submitted")
        slots_to_reset = ["review_text"]
        return [SlotSet(slot, None) for slot in slots_to_reset]


class ReserveInventory(Action):
    def name(self) -> Text:
        return "action_reserve_inventory"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        color = tracker.get_slot("color")
        size = tracker.get_slot("size")
        email = tracker.get_slot("email")

        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users INNER JOIN roles ON(users.role_id=roles.id) WHERE email=?", (email,))
        data_row = cursor.fetchone()

        if list(data_row)[5] == 'seller':
            cursor.execute("INSERT INTO inventory (size, color) VALUES(?,?)", [size, color])
            connection.commit()
            connection.close()
            dispatcher.utter_message(response="utter_item_reserved")
        else:
            dispatcher.utter_message(response="utter_forbidden")

        slots_to_reset = ["size", "color"]
        return [SlotSet(slot, None) for slot in slots_to_reset]


class CreateSellerRequest(Action):
    def name(self) -> Text:
        return "action_create_seller_request"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users INNER JOIN roles ON(users.role_id=roles.id) WHERE email=?", (email,))
        data_row = list(cursor.fetchone())

        if data_row[5] == 'seller':
            dispatcher.utter_message(response="utter_already_seller")
        elif data_row[5] == 'admin':
            dispatcher.utter_message(response="utter_admins_not_allowed")
        else:
            cursor.execute("INSERT INTO seller_requests (user_id) VALUES(?)", [list(data_row)[0]])
            connection.commit()
            connection.close()
            dispatcher.utter_message(response="utter_seller_request_submitted")


        return []
