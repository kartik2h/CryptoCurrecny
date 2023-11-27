from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)
    volume_change_24h = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_1h = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_7d = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_30d = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_60d = models.DecimalField(max_digits=6, decimal_places=2)
    percent_change_90d = models.DecimalField(max_digits=6, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap_dominance = models.DecimalField(max_digits=5, decimal_places=2)
    fully_diluted_market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        managed = False

    def __str__(self):
        return self.name
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Client model
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Client name")
    description = models.TextField(verbose_name="Client say")
    image = models.ImageField(upload_to="clients", default="default.png")

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.user.username}"

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # This method calculates the total for this order item
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product.name)


class Feedback(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    FIRST_VISIT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    first_visit = models.CharField(max_length=3, choices=FIRST_VISIT_CHOICES)

    FOUND_NEEDED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    found_needed = models.CharField(max_length=3, choices=FOUND_NEEDED_CHOICES)

    REASON_CHOICES = [
        ('social media', 'Social Media'),
        ('advertising', 'Advertising'),
        ('google search', 'Google Search'),
        ('friend', 'Friend'),
    ]
    reason = models.CharField(max_length=15, choices=REASON_CHOICES)

    EASE_OF_USE_CHOICES = [
        ('veryEasy', 'Very Easy'),
        ('easy', 'Easy'),
        ('average', 'Average'),
        ('difficult', 'Difficult'),
        ('veryDifficult', 'Very Difficult'),
    ]
    ease_of_use = models.CharField(max_length=15, choices=EASE_OF_USE_CHOICES)

    LIKELIHOOD_TO_RETURN_CHOICES = [
        ('extremelyLikely', 'Extremely Likely'),
        ('veryLikely', 'Very Likely'),
        ('moderatelyLikely', 'Moderately Likely'),
        ('slightlyLikely', 'Slightly Likely'),
        ('unlikelyToReturn', 'Unlikely to Return'),
    ]
    likelihood_to_return = models.CharField(max_length=20, choices=LIKELIHOOD_TO_RETURN_CHOICES)

    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)