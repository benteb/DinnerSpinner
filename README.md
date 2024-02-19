# DinnerSpinner

## A TUI for automated dinner planner. Doubles as a way to store (good) recipes. 

Ideas for further development:
- autogenerate shopping list
- filters (by stars, budget, time, ingredients, etc.)
- Favour dinners that has not been made in a while
- Some way of storing history of dinners made
- fun statistics 


### Dinners are stored in ```dinners.json`````` in the following format:

```json
{
    "name": "Dinner name",
    "ingredients": [
        {
            "name": "Ingredient name",
            "amount": "Amount",
            "unit": "Unit"
        }
    ],
    "instructions": [
        "Instruction 1",
        "Instruction 2"
    ],
    "serving_tip" : [
            "Serving tip 1", "Serving tip 2"],
        "servings" : 4, 
        "tags": [
            "salat",
            "vegetar",
            "tilbehør"
        ],
        "stars": 5,
        "times_made": 0
}
```

Tags used so far: {"fisk": 1, "kylling": 2, "rødt kjøtt": 3, "vegetar": 4, "suppe": 5, "salat": 6}
