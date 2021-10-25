from rest_framework.test import APISimpleTestCase
from hangers.utils import calculate_difference


# SF : 37.760154, -122.450575
# NY : 40.712498, -74.006886
# Distance: 4132km

# Twente Field: 52.241476, 6.849384
# Kennis Park:  52.237973, 6.840168

class TestUtils(APISimpleTestCase):

    def setUp(self):
        pass

    def test_calculate_difference_big(self):
        z = calculate_difference((37.760154, -122.450575), (40.712498, -74.006886))

    def test_calculate_difference_smol(self):
        z = calculate_difference((52.241476, 6.849384), (52.237973, 6.840168))
