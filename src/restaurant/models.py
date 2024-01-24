from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4

# Create your models here.
class Restaurant(models.Model):
    """Model representing a Restaurant."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='restaurant/logos', blank=True)
    message = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.name)

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Menu(models.Model):
    """Model representing a Menu of a Restaurant."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0),
                                   validators=PERCENTAGE_VALIDATOR)

    def __str__(self) -> str:
        return str(self.name)

class Food(models.Model):
    """Model representing a Food item."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2,
                default=Decimal("1.99"), # Decimal needs to be a string or it will have imprecision
                validators=[MinValueValidator(Decimal("0.00"))])
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='restaurant/food_photos', blank=True)
    hidden = models.BooleanField(default=False)

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
