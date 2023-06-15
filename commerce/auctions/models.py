from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="UserBid")

    def __str__(self):
        return str(self.bid)

class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageurl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name='bidPrice')
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    watchList = models.ManyToManyField(User, blank=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="UserComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="listingComments")
    comments = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.owner} commented on {self.listing}"
    
