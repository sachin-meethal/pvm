from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem


MENU_DATA = {

    "Breakfast": [
        ("Puttu", 20),
        ("Kadala Curry", 40),
        ("Green Peas Curry", 40),
        ("Appam", 12),
        ("Egg Curry", 45),
        ("Idiyappam", 12),
        ("Vegetable Curry", 50),
        ("Idli/set", 40),
        ("Sambar", 25),
        ("Poori/masala", 65),
        ("Masala Curry", 40),
        ("Dosa", 20),
        ("Masala Dosa", 60),
        ("Ghee Roast", 70),
        ("Chapathi", 12),
        ("Porotta", 13),
        ("Omelette", 25),
        ("Boiled Egg", 12),
    ],

    "Meals": [
        ("Veg Meals", 80),
        ("Meals + Omelette", 110),
        ("Meals + Fish Fry", 180),
        ("Meals + Chicken Curry", 150),
        ("Meals + Beef Fry", 170),
    ],

    "Biriyani": [
        ("Chicken Biriyani", 150),
        ("Beef Biriyani", 160),
        ("Egg Biriyani", 100),
        ("Veg Biriyani", 120),
        ("Kuzhimanthi", 180),
    ],

    "Alfaham": [
        ("Quarter Alfaham", 130),
        ("Half Alfaham", 260),
        ("Full Alfaham", 490),
        ("Shawarma Plate", 130),
        ("Shawarma Roll", 100),
    ],

    "Beef": [
        ("Beef Fry", 140),
        ("Beef Roast", 130),
        ("Beef Curry", 130),
    ],

    "Chicken": [
        ("Chicken Curry", 120),
        ("Chicken Fry", 140),
        ("Chicken Roast", 130),
        ("Chilli Chicken", 180),
    ],

    "Fish": [
        ("Fish Curry", 90),
        ("Fish Fry", 100),
        ("King Fish Fry", 220),
    ],

    "Tea & Coffee": [
        ("Tea", 13),
        ("Black Tea", 12),
        ("Coffee", 18),
        ("Black Coffee", 12),
        ("Milk Tea", 13),
        ("Lemon Tea", 15),
    ],

    "Juices": [
        ("Lime Juice", 25),
        ("Mint Lime", 30),
        ("Watermelon Juice", 50),
        ("Mango Juice", 70),
        ("Grape Juice", 70),
        ("Mixed Fruit Juice", 90),
        ("Fresh Lime Soda", 40),
    ],

    "Soft Drinks": [
        ("Mineral Water", 20),
        ("Pepsi", 35),
        ("Coca Cola", 35),
        ("Sprite", 35),
        ("Fanta", 40),
    ],

    "Snacks": [
        ("Banana Fry", 13),
        ("Parippu Vada", 13),
        ("Uzhunnu Vada", 12),
        ("Samosa", 20),
        ("Egg Puffs", 25),
        ("Veg Cutlet", 20),
    ],
}


class Command(BaseCommand):
    help = "Insert default menu items"

    def handle(self, *args, **kwargs):

        for category_name, items in MENU_DATA.items():

            category, _ = Category.objects.get_or_create(
                name=category_name
            )

            for name, price in items:

                MenuItem.objects.get_or_create(
                    category=category,
                    name=name,
                    defaults={
                        "price": price,
                        "available": True,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Menu imported successfully.")
        )
