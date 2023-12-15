from django.db import models

# Create your models here.
class Restaurant(models.Model):
    """Model representing a Restaurant."""
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.name)

class Menu(models.Model):
    """Model representing a Menu of a Restaurant."""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.name) 

class Food(models.Model):
    """Model representing a Food item."""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    class FoodType(models.TextChoices):
        """Enums for the types of Food possible."""
        MAIN = "MN", "Main"
        SIDE = "SD", "Side"
        DRINK = "DK", "Drink"
        DESSERT = "DS", "Dessert"

    food_type = models.CharField(
        max_length=2,
        choices=FoodType.choices,
        default=FoodType.MAIN,
    )

    def __str__(self) -> str:
        return str(self.name)
