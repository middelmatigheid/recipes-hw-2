from copy import deepcopy

class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(quantity)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        for ingr in self.ingredients:
            if ingr == ingredient:
                ingr.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return ratio > 0

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Множитель должен быть положительным")
        new_recipe = Recipe(self.title, deepcopy(self.ingredients))
        for ingr in new_recipe.ingredients:
            ingr.quantity *= ratio
        return new_recipe

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"{self.title}"
        for ingr in self.ingredients:
            result += f"\n - {ingr}"
        return result

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        recipe = recipe.scale(portions)
        for ingredient in recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        ind = 0
        while ind < len(self._items):
            item = self._items[ind]
            if item[1] == title:
                self._items[ind], self._items[-1] = self._items[-1], self._items[ind]
                self._items.pop()
            else:
                ind += 1

    def get_list(self):
        ingredients = {}
        for item in self._items:
            ingredient = item[0]
            ingredients[(ingredient.name, ingredient.unit)] = ingredients.get((ingredient.name, ingredient.unit), 0) + ingredient.quantity
        result = []
        for name, unit in ingredients:
            result.append(Ingredient(name, ingredients[(name, unit)], unit))
        return sorted(result, key = lambda x: x.name)

    def __add__(self, other):
        items = deepcopy(self._items) + deepcopy(other._items)
        shopping_list = ShoppingList()
        shopping_list._items = items
        return shopping_list

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        recipe = super().scale(ratio)
        new_dietary_recipe = DietaryRecipe(self.title, self.diet_type, deepcopy(recipe.ingredients))
        return new_dietary_recipe

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"
        