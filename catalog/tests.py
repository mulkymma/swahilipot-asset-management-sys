'''from django.test import TestCase
'''



from django.test import TestCase
from .models import Asset, Employee, AssetAssignment, UsageHistory, Maintenance

class AssetModelTest(TestCase):
    def test_create_asset(self):
        asset = Asset.objects.create(name='Test Laptop', category='Laptop', location='Office', condition='New')
        self.assertEqual(asset.name, 'Test Laptop')

# Similarly, create tests for Employee, AssetAssignment, UsageHistory, and Maintenance
