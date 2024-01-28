from decimal import Decimal
from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

    def get_most_popular_foods(self):
        foods = Food.objects.filter(menu__restaurant=self)
        popular_foods = foods.order_by('-item__quantity').distinct()[:5]
        return popular_foods

    def get_total_sales(self) -> int:
        foods = Food.objects.filter(menu__restaurant=self)
        return sum(food.get_total_sales() for food in foods)

    def get_total_sales_amount(self) -> Decimal:
        foods = Food.objects.filter(menu__restaurant=self)
        return sum((food.get_total_sales_amount() for food in foods), Decimal(0))

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Promotion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, editable=False)
    menu = models.ManyToManyField('Menu')
    name = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0),
                                   validators=PERCENTAGE_VALIDATOR)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.name)

class Menu(models.Model):
    """Model representing a Menu of a Restaurant."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=200)

    def get_best_promotion(self) -> Promotion | None:
        return self.promotion_set.filter(active=True).order_by('-discount').first() # type: ignore

    def __str__(self) -> str:
        return str(self.name)

class Food(models.Model):
    """Model representing a Food item."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
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

    def get_price(self) -> Decimal:
        best_promotion = self.menu.get_best_promotion()  if self.menu else None
        return self.price if not best_promotion else self.price * (1 - best_promotion.discount / 100)
    
    def get_total_sales(self) -> int:
        return self.item_set.aggregate(models.Sum('quantity'))['quantity__sum'] or 0 # type: ignore
    
    def get_total_sales_amount(self) -> Decimal:
        return self.item_set.aggregate(models.Sum('price'))['price__sum'] or Decimal(0) # type: ignore

    def __str__(self) -> str:
        return str(self.name)
