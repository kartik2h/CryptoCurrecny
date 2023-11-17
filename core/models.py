from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)


# About Model
class About(models.Model):
    short_description = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="about")

    class Meta:
        verbose_name = "About me"
        verbose_name_plural = "About me"

    def __str__(self):
        return "About me"


# Service Model
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Service name")
    description = models.TextField(verbose_name="About service")

    def __str__(self):
        return self.name


# Recent Work Model
class RecentWork(models.Model):
    title = models.CharField(max_length=100, verbose_name="Work title")
    image = models.ImageField(upload_to="works")

    def __str__(self):
        return self.title


# Client model
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Client name")
    description = models.TextField(verbose_name="Client say")
    image = models.ImageField(upload_to="clients", default="default.png")

    def __str__(self):
        return self.name

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
