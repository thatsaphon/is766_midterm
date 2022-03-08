from datetime import date
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from mongoengine import *
from bs4 import BeautifulSoup
import requests

connect(
    host="mongodb+srv://is766:HTZIetTwHD4tkQjn@is766cluster0.dpa1z.mongodb.net/is766db?retryWrites=true&w=majority"
)
app = FastAPI()

# Ingredient, Item, Recipe และ Menu


class IngredientIn(BaseModel):
    user: Optional[str]
    vendor: Optional[str]
    title: str
    slug: Optional[str]
    summary: Optional[str]
    type: Optional[str]
    cooking: Optional[str]
    sku: Optional[str]
    price: Optional[float]
    quantity: Optional[float]
    unit: Optional[str]
    recipe: Optional[str]
    instructions: Optional[str]
    content: Optional[str]


class Ingredient(Document):
    user = StringField()
    vendor = StringField()
    title = StringField(required=True)
    slug = StringField()
    summary = StringField()
    type = StringField()
    cooking = StringField()
    sku = StringField()
    price = FloatField()
    quantity = FloatField()
    unit = StringField()
    recipe = StringField()
    instructions = StringField()
    created = StringField()
    updated = StringField()
    content = StringField()


class ItemIn(BaseModel):
    user: Optional[str]
    vendor: Optional[str]
    title: str
    slug: Optional[str]
    summary: Optional[str]
    type: Optional[str]
    cooking: Optional[str]
    sku: Optional[str]
    price: Optional[float]
    quantity: Optional[float]
    unit: Optional[str]
    recipe: Optional[str]
    instructions: Optional[str]
    content: Optional[str]


class Item(Document):
    user = StringField()
    vendor = StringField()
    title = StringField(required=True)
    slug = StringField()
    summary = StringField()
    type = StringField()
    cooking = StringField()
    sku = StringField()
    price = FloatField()
    quantity = FloatField()
    unit = StringField()
    recipe = StringField()
    instructions = StringField()
    created = StringField()
    updated = StringField()
    content = StringField()


class RecipeIn(BaseModel):
    item: str
    ingredient: str
    quantity: float
    unit: Optional[str]
    instructions: Optional[str]


class Recipe(Document):
    item = StringField(required=True)
    ingredient = StringField(required=True)
    quantity = FloatField(required=True)
    unit = StringField()
    instructions = StringField()


class MenuIn(BaseModel):
    user: Optional[str]
    title: str
    slug: Optional[str]
    summary: Optional[str]
    type: Optional[str]
    content: Optional[str]


class Menu(Document):
    user = StringField()
    title = StringField(required=True)
    slug = StringField()
    summary = StringField()
    type = StringField()
    created = StringField()
    updated = StringField()
    content = StringField()


@app.get("/ingredients/")
def get_all_ingredients():
    ingredients = []
    for rec in Ingredient.objects:
        ingredients.append(
            {
                "user": rec.user,
                "vendor": rec.vendor,
                "title": rec.title,
                "slug": rec.slug,
                "summary": rec.summary,
                "type": rec.type,
                "cooking": rec.cooking,
                "sku": rec.sku,
                "price": rec.price,
                "quantity": rec.quantity,
                "unit": rec.unit,
                "recipe": rec.recipe,
                "instructions": rec.instructions,
                "created": rec.created,
                "updated": rec.updated,
                "content": rec.content,
            }
        )
    return{
        "ingredients": ingredients
    }


@app.get("/ingredients/{ingredient_title}")
def get_ingredient_by_title(ingredient_title: str):
    ingredient = Ingredient.objects(title=ingredient_title)

    if len(ingredient) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "ingredient not found"
            }
        )

    return {
        "user": ingredient[0].user,
        "vendor": ingredient[0].vendor,
        "title": ingredient[0].title,
        "slug": ingredient[0].slug,
        "summary": ingredient[0].summary,
        "type": ingredient[0].type,
        "cooking": ingredient[0].cooking,
        "sku": ingredient[0].sku,
        "price": ingredient[0].price,
        "quantity": ingredient[0].quantity,
        "unit": ingredient[0].unit,
        "recipe": ingredient[0].recipe,
        "instructions": ingredient[0].instructions,
        "created": ingredient[0].created,
        "updated": ingredient[0].updated,
        "content": ingredient[0].content,
    }


@app.post("/ingredients/")
def add_new_ingredient(ingredient_in: IngredientIn):
    ingredientDoc = Ingredient(title=ingredient_in.title)
    ingredientDoc.user = ingredient_in.user
    ingredientDoc.vendor = ingredient_in.vendor
    ingredientDoc.slug = ingredient_in.slug
    ingredientDoc.summary = ingredient_in.summary
    ingredientDoc.type = ingredient_in.type
    ingredientDoc.cooking = ingredient_in.cooking
    ingredientDoc.sku = ingredient_in.sku
    ingredientDoc.price = ingredient_in.price
    ingredientDoc.quantity = ingredient_in.quantity
    ingredientDoc.unit = ingredient_in.unit
    ingredientDoc.recipe = ingredient_in.recipe
    ingredientDoc.instructions = ingredient_in.instructions
    ingredientDoc.created = date.today().strftime("%d/%m/%Y")
    ingredientDoc.updated = date.today().strftime("%d/%m/%Y")
    ingredientDoc.content = ingredient_in.content
    ingredientDoc.save()
    return{
        "message": "new ingredient was added"
    }


@app.put("/ingredients/{ingredient_title}")
def edit_ingredient(ingredient_title: str, ingredient_in: IngredientIn):
    ingredient = Ingredient.objects(title=ingredient_title)
    if len(ingredient) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "ingredient not found"
            }
        )

    ingredientDoc = Ingredient(title=ingredient_in.title)
    ingredientDoc.user = ingredient_in.user
    ingredientDoc.vendor = ingredient_in.vendor
    ingredientDoc.slug = ingredient_in.slug
    ingredientDoc.summary = ingredient_in.summary
    ingredientDoc.type = ingredient_in.type
    ingredientDoc.cooking = ingredient_in.cooking
    ingredientDoc.sku = ingredient_in.sku
    ingredientDoc.price = ingredient_in.price
    ingredientDoc.quantity = ingredient_in.quantity
    ingredientDoc.unit = ingredient_in.unit
    ingredientDoc.recipe = ingredient_in.recipe
    ingredientDoc.instructions = ingredient_in.instructions
    ingredientDoc.created = ingredient[0].created
    ingredientDoc.updated = date.today().strftime("%d/%m/%Y")
    ingredientDoc.content = ingredient_in.content

    ingredient[0].delete()
    ingredientDoc.save()
    return {
        "message": "The ingredient was updated."
    }


@app.get("/items/")
def get_all_items():
    items = []
    for rec in Item.objects:
        items.append(
            {
                "user": rec.user,
                "vendor": rec.vendor,
                "title": rec.title,
                "slug": rec.slug,
                "summary": rec.summary,
                "type": rec.type,
                "cooking": rec.cooking,
                "sku": rec.sku,
                "price": rec.price,
                "quantity": rec.quantity,
                "unit": rec.unit,
                "recipe": rec.recipe,
                "instructions": rec.instructions,
                "created": rec.created,
                "updated": rec.updated,
                "content": rec.content,
            }
        )
    return{
        "items": items
    }


@app.get("/items/{item_title}")
def get_ingredient_by_title(item_title: str):
    item = Item.objects(title=item_title)
    if len(item) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "item not found"
            }
        )
    return {
        "user": item[0].user,
        "vendor": item[0].vendor,
        "title": item[0].title,
        "slug": item[0].slug,
        "summary": item[0].summary,
        "type": item[0].type,
        "cooking": item[0].cooking,
        "sku": item[0].sku,
        "price": item[0].price,
        "quantity": item[0].quantity,
        "unit": item[0].unit,
        "recipe": item[0].recipe,
        "instructions": item[0].instructions,
        "created": item[0].created,
        "updated": item[0].updated,
        "content": item[0].content,
    }


@app.post("/items/")
def add_new_item(item_in: ItemIn):
    itemDoc = Item(title=item_in.title)
    itemDoc.user = item_in.user
    itemDoc.vendor = item_in.vendor
    itemDoc.slug = item_in.slug
    itemDoc.summary = item_in.summary
    itemDoc.type = item_in.type
    itemDoc.cooking = item_in.cooking
    itemDoc.sku = item_in.sku
    itemDoc.price = item_in.price
    itemDoc.quantity = item_in.quantity
    itemDoc.unit = item_in.unit
    itemDoc.recipe = item_in.recipe
    itemDoc.instructions = item_in.instructions
    itemDoc.created = date.today().strftime("%d/%m/%Y")
    itemDoc.updated = date.today().strftime("%d/%m/%Y")
    itemDoc.content = item_in.content
    itemDoc.save()
    return{
        "message": "new item was added"
    }


@app.put("/items/{item_title}")
def edit_ingredient(item_title: str, item_in: ItemIn):
    item = Item.objects(title=item_title)
    if len(item) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "item not found"
            }
        )

    itemDoc = Item(title=item_in.title)
    itemDoc.user = item_in.user
    itemDoc.vendor = item_in.vendor
    itemDoc.slug = item_in.slug
    itemDoc.summary = item_in.summary
    itemDoc.type = item_in.type
    itemDoc.cooking = item_in.cooking
    itemDoc.sku = item_in.sku
    itemDoc.price = item_in.price
    itemDoc.quantity = item_in.quantity
    itemDoc.unit = item_in.unit
    itemDoc.recipe = item_in.recipe
    itemDoc.instructions = item_in.instructions
    itemDoc.created = item[0].created
    itemDoc.updated = date.today().strftime("%d/%m/%Y")
    itemDoc.content = item_in.content

    item[0].delete()
    itemDoc.save()
    return {
        "message": "The item was updated."
    }


@app.get("/recipe/")
def get_all_recipes():
    recipes = []
    for rec in Recipe.objects:
        recipes.append(
            {
                "item": rec.item,
                "ingredient": rec.ingredient,
                "quantity": rec.quantity,
                "unit": rec.unit,
                "instructions": rec.instructions,
            }
        )
    return{
        "recipes": recipes
    }


@app.get("/recipes/{recipe_item}/{recipe_ingredient}")
def get_recipe_by_item_and_ingredient(recipe_item: str, recipe_ingredient: str):
    recipe = Recipe.objects(item=recipe_item, ingredient=recipe_ingredient)
    if len(recipe) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "recipe not found"
            }
        )

    return {
        "item": recipe[0].item,
        "ingredient": recipe[0].ingredient,
        "quantity": recipe[0].quantity,
        "unit": recipe[0].unit,
        "instructions": recipe[0].instructions,
    }


@app.post("/recipes/")
def add_new_recipe(recipe_in: RecipeIn):
    recipeDoc = Recipe(item=recipe_in.item)
    recipeDoc.ingredient = recipe_in.ingredient
    recipeDoc.quantity = recipe_in.quantity
    recipeDoc.unit = recipe_in.unit
    recipeDoc.instructions = recipe_in.instructions
    recipeDoc.save()
    return{
        "message": "new recipe was added"
    }


@app.put("/recipes/{recipe_item}/{recipe_ingredient}")
def edit_recipe(recipe_item: str, recipe_ingredient: str, recipe_in: RecipeIn):
    recipe = Recipe.objects(item=recipe_item, ingredient=recipe_ingredient)
    if len(recipe) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "recipe not found"
            }
        )

    recipeDoc = Recipe(item=recipe_in.item)
    recipeDoc.ingredient = recipe_in.ingredient
    recipeDoc.quantity = recipe_in.quantity
    recipeDoc.unit = recipe_in.unit
    recipeDoc.instructions = recipe_in.instructions

    recipe[0].delete()
    recipeDoc.save()
    return {
        "message": "The recipe was updated."
    }


@app.get("/menus/")
def get_all_menus():
    menus = []
    for rec in Menu.objects:
        menus.append(
            {
                "user": rec.user,
                "title": rec.title,
                "slug": rec.slug,
                "summary": rec.summary,
                "type": rec.type,
                "created": rec.created,
                "updated": rec.updated,
                "content": rec.content,
            }
        )
    return{
        "menus": menus
    }


@app.get("/menus/{menu_title}")
def get_menu_by_title(menu_title: str):
    menu = Menu.objects(title=menu_title)
    if len(menu) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "menu not found"
            }
        )

    return {
        "user": menu[0].user,
        "title": menu[0].title,
        "slug": menu[0].slug,
        "summary": menu[0].summary,
        "type": menu[0].type,
        "created": menu[0].created,
        "updated": menu[0].updated,
        "content": menu[0].content,
    }


@app.post("/menus/")
def add_new_menu(menu_in: MenuIn):
    print("test")
    print(menu_in.title)
    menuDoc = Menu(title=menu_in.title)
    menuDoc.user = menu_in.user
    menuDoc.slug = menu_in.slug
    menuDoc.summary = menu_in.summary
    menuDoc.type = menu_in.type
    menuDoc.created = date.today().strftime("%d/%m/%Y")
    menuDoc.updated = date.today().strftime("%d/%m/%Y")
    menuDoc.content = menu_in.content
    menuDoc.save()
    return{
        "message": "new menu was added"
    }


@app.put("/menus/{menu_title}")
def edit_recipe(menu_title: str, menu_in: MenuIn):
    menu = Menu.objects(title=menu_title)
    if len(menu) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "menu not found"
            }
        )

    menuDoc = Menu(title=menu_in.title)
    menuDoc.user = menu_in.user
    menuDoc.title = menu_in.title
    menuDoc.slug = menu_in.slug
    menuDoc.summary = menu_in.summary
    menuDoc.type = menu_in.type
    menuDoc.created = menu[0].created
    menuDoc.updated = date.today().strftime("%d/%m/%Y")
    menuDoc.content = menu_in.content

    menu[0].delete()
    menuDoc.save()
    return {
        "message": "The recipe was updated."
    }


@app.get("/wongnai/{restaurant_code}")  # ตัวอย่าง 5290th 3569NH 9379vL
def get_from_wongnai(restaurant_code: str = Path(..., title="The ID of the item to get")):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    r = requests.get(
        'https://www.wongnai.com/restaurants/{}'.format(restaurant_code), headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    menus = []
    menu_bar = soup.find_all("div", "CarouselBox-sc-138w5u6 jnHREM")
    if len(menu_bar) == 0:
        return JSONResponse(
            status_code=404,
            content={
                "message": "restaurant not found"
            }
        )
    for menu in menu_bar[0].find_all("div", "Item-sc-1g4cvri iJMJdE"):
        data = {}
        for name in menu.find_all("div", "sc-bdfBQB dkNout bd16 bd14-mWeb mb-2 mb-0-mWeb"):
            data['name'] = name.string
        for image in menu.find_all("img"):
            data['image'] = image['src']
        for price in menu.find_all("span", "ml-auto md14 md12-mWeb"):
            data['price'] = price.string
        menus.append(data)
    return{"menus": menus}
