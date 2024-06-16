from django.test import TestCase
from goods.models import Categories
# Create your tests here.
class CategoriesModelTest(TestCase):
    def test_create_item(self):
        # Создание нового элемента
        category = Categories.objects.create(name="Test category", slug="test-category")
        # Проверка, что элемент был создан успешно
        self.assertEqual(category.name, "Test category")
        self.assertEqual(category.slug, "test-category")
        # Проверка, что элемент существует в базе данных
        self.assertTrue(Categories.objects.filter(name="Test category").exists())