from .models import Category
from .views import get_basket

def all_categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}

def number(request):
    basket = get_basket(request)
    number = basket.lineitem_set.count()
    return {'number': number, 'basket_total': basket.total()}
