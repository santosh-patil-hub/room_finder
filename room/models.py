# room/models.py

from django.db import models
from django.conf import settings

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('1rk', '1RK'),
        ('1bhk', '1BHK'),
        ('2bhk', '2BHK'),
        ('3bhk', '3BHK'),
        ('hostel', 'Hostel'),
        ('pg', 'PG'),
        ('cot', 'Cot-based'),
    ]

    ELECTRIC_BILL_CHOICES = [
        ('tenant', 'Tenant'),
        ('owner', 'Owner'),
    ]

    AVAILABLE_FOR_CHOICES = [
        ('boys', 'Boys Only'),
        ('girls', 'Girls Only'),
        ('family', 'Family Only'),
        ('both', 'Both'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 1. Title
    title = models.CharField(max_length=255, help_text="House, apartment, or building name")

    # 2. Address
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    colony = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6)
    house_no = models.CharField(max_length=50)
    floor_no = models.CharField(max_length=10)

    # 3. Facilities
    has_24h_water = models.BooleanField(default=False)
    has_cold_water = models.BooleanField(default=False)
    has_hot_water = models.BooleanField(default=False)
    separate_bathroom = models.BooleanField(default=False)
    has_rooftop = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)

    # 4. Electric bill payer
    electric_bill_payer = models.CharField(max_length=10, choices=ELECTRIC_BILL_CHOICES)

    # 5. Room partners
    room_partner_count = models.PositiveIntegerField(default=1)

    # 6. Room type
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)

    # 7. Advance deposit
    advance_deposit = models.DecimalField(max_digits=10, decimal_places=2)

    # 8. Rent per month
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    # 9. Who can rent
    available_for = models.CharField(max_length=10, choices=AVAILABLE_FOR_CHOICES)

    # 10. Availability
    is_available = models.BooleanField(default=True, help_text="Is the room currently available?")


    # 11. Created date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city}"
