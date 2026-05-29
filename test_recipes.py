import pytest
from HW_2_OOP_Testing_Git import Ingredient, Recipe, ShoppingList

# Ingredient

def test_ingredient_init():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"

def test_ingredient_init_with_negative_quantity():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", -500, "г")

def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_eq_same():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 1000, "г")
    assert (ingredient1 == ingredient2) == True

def test_ingredient_eq_different_name():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Крахмал", 500, "г")
    assert (ingredient1 == ingredient2) == False

def test_ingredient_eq_different_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 500, "кг")
    assert (ingredient1 == ingredient2) == False

# Recipe

def test_recipe_init():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    assert recipe.title == "Чудо рецепт"
    assert recipe.ingredients == [ingredient1, ingredient2]

def test_recipe_add_ingredient_new():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    ingredient3 = Ingredient("Сахар", 50, "г")
    recipe.add_ingredient(ingredient3)
    assert ingredient3 in recipe.ingredients

def test_recipe_add_ingredient_old():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    ingredient3 = Ingredient("Мука", 50, "г")
    recipe.add_ingredient(ingredient3)
    assert recipe.ingredients[0].quantity == 550

def test_recipe_scale_is_new():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    new_recipe = recipe.scale(2)
    assert recipe.ingredients[0].quantity == 500

def test_recipe_scale_multiplies():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    new_recipe = recipe.scale(2)
    assert new_recipe.ingredients[0].quantity == 1000
    assert new_recipe.ingredients[1].quantity == 400

def test_recipe_scale_negative_ratio():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    with pytest.raises(ValueError, match="Множитель должен быть положительным"):
        recipe.scale(-2)

def test_recipe_len():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    ingredient3 = Ingredient("Мука", 50, "г")
    recipe.add_ingredient(ingredient3)
    assert len(recipe.ingredients) == 2

# ShoppingList

def test_shopping_list_add_recipe():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    assert len(shopping_list._items) == 2
    assert len(shopping_list._items[0]) == 2
    assert len(shopping_list._items[1]) == 2
    assert shopping_list._items[0][1] == "Чудо рецепт"
    assert shopping_list._items[1][1] == "Чудо рецепт"
    assert shopping_list._items[0][0].quantity == 1000
    assert shopping_list._items[1][0].quantity == 400

def test_shopping_list_add_recipe_with_negative_portions():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        shopping_list.add_recipe(recipe, -2)

def test_shopping_list_remove_recipe():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    shopping_list.remove_recipe("Чудо рецепт")
    assert len(shopping_list._items) == 0

def test_shopping_list_remove_recipe_unknown():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    shopping_list.remove_recipe("Плохой рецепт")
    assert len(shopping_list._items) == 2

def test_shopping_list_get_list():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe1 = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list = ShoppingList()
    
    shopping_list.add_recipe(recipe1, 1)
    ingredient3 = Ingredient("Мука", 500, "г")
    ingredient4 = Ingredient("Водка", 200, "мл")
    recipe2 = Recipe("Плохой рецепт", [ingredient3, ingredient4])
    shopping_list.add_recipe(recipe2, 1)
    
    sh_list = shopping_list.get_list()
    print(sh_list)
    assert len(sh_list) == 3
    assert sh_list[0].name == "Вода"
    assert sh_list[0].quantity == 200
    assert sh_list[1].name == "Водка"
    assert sh_list[1].quantity == 200
    assert sh_list[2].name == "Мука"
    assert sh_list[2].quantity == 1000

def test_shopping_list_add():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Вода", 200, "мл")
    recipe1 = Recipe("Чудо рецепт", [ingredient1, ingredient2])
    shopping_list1 = ShoppingList()
    shopping_list1.add_recipe(recipe1, 1)
    
    ingredient3 = Ingredient("Мука", 500, "г")
    ingredient4 = Ingredient("Водка", 200, "мл")
    recipe2 = Recipe("Плохой рецепт", [ingredient3, ingredient4])
    shopping_list2 = ShoppingList()
    shopping_list2.add_recipe(recipe2, 1)

    shopping_list = shopping_list1 + shopping_list2
    assert len(shopping_list._items) == 4
    for ingredient in [ingredient1, ingredient2]:
        assert (ingredient, "Чудо рецепт") in shopping_list._items
    for ingredient in [ingredient3, ingredient4]:
        assert (ingredient, "Плохой рецепт") in shopping_list._items
        
    assert len(shopping_list1._items) == 2
    for ingredient in [ingredient1, ingredient2]:
        assert (ingredient, "Чудо рецепт") in shopping_list1._items
        
    assert len(shopping_list2._items) == 2
    for ingredient in [ingredient3, ingredient4]:
        assert (ingredient, "Плохой рецепт") in shopping_list2._items
    