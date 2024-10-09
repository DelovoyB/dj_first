from django.db import models
from django.urls import reverse


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Returns a string representation of the category object, which is its name.

        Returns:
            str: The name of the category.
        """
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='goods_images', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Categories, on_delete=models.PROTECT)

    class Meta:
        db_table = 'product'
        ordering = ('id',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """
        Returns a string representation of the product object, which is its name
        followed by quantity.

        Returns:
            str: The name of the product and the quantity.
        """
        return f'{self.name} Quantity - {self.quantity}'

    def get_absolute_url(self):
        """
        Returns the URL of the product detail page as a string.

        The URL is in the format of '/catalog/<product_slug>/' where <product_slug>
        is the slug of the product.

        Returns:
            str: The URL of the product detail page.
        """
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def sell_price(self):
        """
        Returns the selling price of the product as a float.

        If the product has a discount (discount > 0), it will return the selling price
        of the product, which is the price minus the discount. Otherwise, it will return
        the price as the selling price.

        Returns:
            float: The selling price of the product.
        """
        if self.discount > 0:
            return round(self.price - (self.price * self.discount / 100), 2)
        return self.price
