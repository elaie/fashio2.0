from django.db import models


class Product(models.Model):
    product_from = models.CharField(max_length=200,blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    users = models.CharField(max_length=600, blank=True)
    def get_my_list(self):
        return self.users.split(",")

    def set_my_list(self, value):
        self.users = ",".join(value)

    my_list_items = property(get_my_list, set_my_list)
    def __str__(self):
        return self.name