import json
from os.path import isfile
from pathlib import Path
from typing import Any
from django.core.management import BaseCommand
from jsonschema import validate

from restaurant.models import Restaurant, Menu, Food
FILE = 'file'

class Command(BaseCommand):
    help = "Create restaurant from file"
    food_type_map = {
            'main': Food.FoodType.MAIN,
            'side': Food.FoodType.SIDE,
            'drink': Food.FoodType.DRINK,
            'dessert': Food.FoodType.DESSERT,
        }

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "address": {"type": "string"},
            "phone": {"type": "string"},
            "logo": {"type": "string"},
            "message": {"type": "string"},
            "menus": {   
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "foods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "price": {"type": "number"},
                                    "description": {"type": "string"},
                                    "photo": {"type": "string"},
                                    "food_type": {"type": "string"},
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    def add_arguments(self, parser):
        parser.add_argument(FILE, nargs="+", type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options[FILE] is None:
            print("No file specified")
            return None

        if len(options[FILE]) > 1:
            print("Only one file allowed")
            return None

        file_path = Path(options[FILE][0])
        if not isfile(file_path):
            print("File not found")
            return None

        if options[FILE][0].split('.')[-1] != 'json':
            print("Only json files allowed")
            return None

        with open(file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            validate(instance=data, schema=self.schema)

            logo = Path(data['logo'])
            if not isfile(file_path.parent / logo):
                print("Logo file not found")
                return None

            for menu in data['menus']:
                for food in menu['foods']:
                    food_image = Path(food['photo'])
                    if not isfile(file_path.parent / food_image):
                        print(f"{food['name']} photo file not found")
                        return None

            name = data['name']
            address = data['address']
            phone = data['phone']
            message = data['message']
            rest = Restaurant.objects.create(
                name=name,
                address=address,
                phone=phone,
                message=message
            )

            with open(file_path.parent / logo, 'rb') as logo_file:
                rest.logo.save(
                    str(logo).split('/')[-1].split('.')[0],
                    logo_file, # type: ignore
                    save=True
                )

            for menu in data['menus']:
                menu_name = menu['name']
                menu_obj = Menu.objects.create(restaurant=rest, name=menu_name)

                for food in menu['foods']:
                    food_name = food['name']
                    food_price = food['price']
                    food_description = food['description']
                    food_image = Path(food['photo'])
                    food_type = self.food_type_map[food['food_type']]
                    food_obj = Food.objects.create(
                        menu=menu_obj,
                        name=food_name,
                        price=food_price,
                        description=food_description,
                        food_type=food_type
                    )

                    with open(file_path.parent / food_image, 'rb') as food_image_file:
                        food_obj.photo.save(
                            str(food_image).split('/')[-1].split('.')[0],
                            food_image_file, # type: ignore
                            save=True
                        )
                    print(f"Food {food_obj.name} created successfully")
                print(f"Menu {menu_obj.name} created successfully")

            print(f"Restaurant {rest.name} created successfully")
