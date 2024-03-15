import os
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from openai import OpenAI


####################################### CUSTOM FUNCTIONS
def generate_ai_response(prompt):
    client = OpenAI(api_key="")
    template = "You are a fertility expert with vast experience in fertility, pregnancy, and maternal health. A patient is asking you a question. Your answers should be simple and very short, just one paragraph"

    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  # Choose the engine appropriate for your use case
            prompt=f"{template}. {prompt}",
            temperature=0.5,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, but I couldn't generate a response at this time."


############################################ TIMING AND MENSTRUAL CYCLE ACTIONS
class ActionTimingCycle(Action):
    def name(self) -> Text:
        return "action_timing_cycle"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response("Tell me about timing and menstrual cycle for conceiving.")
        dispatcher.utter_message(ai_response)
        return []


############################################ BEHAVIORS ACTIONS
class ActionBehaviorsExercise(Action):
    def name(self) -> Text:
        return "action_behaviors_exercise"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What exercise and physical activity advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


class ActionBehaviorsStress(Action):
    def name(self) -> Text:
        return "action_behaviors_stress"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What stress management advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


class ActionBehaviorsSmoking(Action):
    def name(self) -> Text:
        return "action_behaviors_smoking"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What smoking & alcohol advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


class ActionBehaviorsVitamins(Action):
    def name(self) -> Text:
        return "action_behaviors_vitamins"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What vitamins to help advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


############################################ CONCEPTION FLOW WINDOW ACTIONS
class ActionConceptionDate(Action):
    def name(self) -> Text:
        return "action_conception_date"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        period_date = tracker.get_slot("period_date")
        period_duration = tracker.get_slot("period_duration")
        print(period_date)
        print(period_duration)
        ai_response = generate_ai_response(
            f"Give me the best estimate on conception for someone who's last period ended {period_date} and lasted for {period_duration} days")
        dispatcher.utter_message(ai_response)
        return []


############################################ NUTRITION CONCEIVE ACTIONS
class ActionNutritionFoodTypes(Action):
    def name(self) -> Text:
        return "action_nutrition_food_types"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What healthy food and nutrition advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


class ActionNutritionVitamins(Action):
    def name(self) -> Text:
        return "action_nutrition_vitamins"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        ai_response = generate_ai_response(
            "What vitamins to help advice can you give a person that is trying to conceive?")
        dispatcher.utter_message(ai_response)
        return []


class ActionNutritionRecipes(Action):
    def name(self) -> Text:
        return "action_nutrition_recipes"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        food = tracker.get_slot("available_food")
        nutrition_stage = tracker.get_slot("nutrition_stage")
        ai_response = generate_ai_response(
            f"What healthy recipes advice can you give a person that is {nutrition_stage} with the following available foods {food}")
        dispatcher.utter_message(ai_response)
        return []


class ActionNutritionMealPlans(Action):
    def name(self) -> Text:
        return "action_nutrition_meal_plans"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        food = tracker.get_slot("available_food")
        nutrition_stage = tracker.get_slot("nutrition_stage")
        meal_plans_time = tracker.get_slot("meal_plans_time")
        ai_response = generate_ai_response(
            f"What meal plan advice can you give a person that is {nutrition_stage} for {meal_plans_time} days with the following available foods {food}")
        dispatcher.utter_message(ai_response)
        return []


############################################ RESET SLOTS ACTION
class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return [
            SlotSet("period_date", None),
            SlotSet("period_duration", None),
            SlotSet("available_food", None),
            SlotSet("meal_plans_time", None),
        ]
