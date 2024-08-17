from decimal import Decimal
from apps.orders.models import PercentCashback

def get_bonus_percentages():
    percents = PercentCashback.objects.all().first()
    if not percents:
        percents = PercentCashback.objects.create(mobile_percent=5, web_percent=3)
    return percents.mobile_percent, percents.web_percent

def calculate_bonus_points(order_total, delivery_fee, order_source):
    mobile_percent, web_percent = get_bonus_percentages()
    total_order_amount = order_total - delivery_fee
    if order_source == 'mobile':
        bonus_percentage = mobile_percent
    elif order_source == 'web':
        bonus_percentage = web_percent
    else:
        bonus_percentage = Decimal('0.0')

    bonus_points = total_order_amount * (bonus_percentage / Decimal('100'))
    return bonus_points

def apply_bonus_points(user, bonus_points):
    if user.bonus is None:
        user.bonus = 0
    user.bonus += bonus_points
    user.save()
