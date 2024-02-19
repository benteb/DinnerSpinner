from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Select,Static
from textual import  on
from json import load
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
import random

class DinnerSpinner(App):

    CSS_PATH = "layout.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container(id="app-grid"):
            with Vertical(id="top-left"):
                yield Horizontal(Label("How many dinners?"), Select(((str(number), number) for number in range(1, 15)), id="num_of_dinners"))
                yield Vertical(id="dinner_requests")
            yield Vertical(id="dinner_list")
            yield Button(label="Spin!", id="generate_button")

        self.dinners_avail = load(open("dinners.json", "r"))
        self.tags = load(open("tags.json", "r"))
        self.dinners = []
        self.saved_dinners = []
        self.dinner_layer = False

    @on(Select.Changed)
    def on_select(self, event: Select.Changed) -> None:
        if event.select.id == "num_of_dinners":
            self.set_special_requests(event.select.value)

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "generate_button":
            self.on_generate_button_pressed()

        if event.button.id.startswith("save_"):
            self.save_button_pressed(event)

        if event.button.id.startswith("dinner_"):
            self.show_dinner(event.button.id.split("_")[1])

        if event.button.id == "exit_dinner":
            dinner_layer = self.query_one("#dinner_layer")
            dinner_layer.remove()


    def show_dinner(self, idx):
            
            dinner = self.dinners[int(idx)]

            ingredients = "\n".join([f"{a['amount']} {a['unit']} {a['name']}" for a in dinner.ingredients])

            instructions = "\n\n".join([f"{idx + 1}. {instruction}" for idx, instruction in enumerate(dinner.instructions)])


            self.mount(Container(
                Container(Label(f"{dinner.name}"), id='dinner_header'),
                Container(Button("x", id='exit_dinner'), id="exit_dinner_container"), 
                VerticalScroll(Static(ingredients)), 
                VerticalScroll(Static(instructions), id='instructions'), id="dinner_layer"
            ))


    def set_special_requests(self, num_of_dinners):

        container = self.query_one("#dinner_requests")
        container.remove_children()

        for dinner in range(num_of_dinners):
            container.mount(Horizontal(Label(f"Dinner {dinner + 1}"), Select(((tag, tag) for tag in self.tags.keys()), id=f"request_{dinner}")))

    def on_generate_button_pressed(self):
        dinner_requests = self.query_one("#dinner_requests")
        dinner_list = self.query_one("#dinner_list")
        
        updated_dinners = []

        for idx, request in enumerate(dinner_requests.children):

            if request.children[1].value == Select.BLANK:
                tag = "whatever"
            else:
                tag = request.children[1].value

            dinner = self.get_dinner(tag)

            try:
                curr_dinner = self.dinners[idx]
                if curr_dinner.saved:
                    updated_dinners.append(curr_dinner)
                else:
                    updated_dinners.append(Dinner(idx, dinner, self.dinners_avail[dinner]))
            except IndexError:
                updated_dinners.append(Dinner(idx, dinner, self.dinners_avail[dinner]))


        dinner_list.remove_children()

        for idx, dinner in enumerate(updated_dinners):
            if dinner.saved:
                dinner_list.mount(Horizontal(Label(f"Dinner {idx + 1}: "), Button(dinner.name, id=f"dinner_{idx}", classes="dinner_button"),  Button("Saved!", id=f"save_{idx}", classes="saved_button")))
            else:
                dinner_list.mount(Horizontal(Label(f"Dinner {idx + 1}: "), Button(dinner.name, id=f"dinner_{idx}", classes="dinner_button"),  Button("Save?", id=f"save_{idx}", classes="save_button")))

        print(updated_dinners)


        self.dinners = updated_dinners

    def save_button_pressed(self, event):

        idx = int(event.button.id.split("_")[1])

        if "Saved" in event.button.label:
            event.button.label = "Save?"
            event.button.remove_class("saved_button")
            self.dinners[idx].saved = False
        else:
            event.button.label = "Saved!"
            event.button.add_class("saved_button")
            self.dinners[idx].save()

    def get_dinner(self, tag):

        if tag == "whatever":
            return random.choice(list(self.dinners_avail.keys()))
        
        filtered_recipes = {name: details for name, details in self.dinners_avail.items() if tag in details["tags"]}

        return random.choice(list(filtered_recipes.keys()))

class Dinner:
    def __init__(self, idx, name, dinner_dict):
        self.name = name
        self.ingredients = dinner_dict["ingredients"]
        self.instructions = dinner_dict["instructions"]
        self.serving_tip = dinner_dict["serving_tip"]
        self.servings = dinner_dict["servings"]
        self.tags = dinner_dict["tags"]
        self.stars = dinner_dict["stars"]
        self.times_made = dinner_dict["times_made"]
        self.idx = idx
        self.saved = False

    def save(self):
        self.saved = True

if __name__ == "__main__":
    app = DinnerSpinner()
    app.run()