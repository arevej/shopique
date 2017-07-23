from django import forms

class BuyerInfo(forms.Form):
    delivery_country = forms.CharField(label="Страна", max_length=100)
    delivery_city = forms.CharField(label="Город", max_length=100)
    delivery_address = forms.CharField(label="Адрес", max_length=100)
    buyer_name = forms.CharField(label="Имя", max_length=30)
    buyer_email =forms.EmailField(label="Email", max_length=50)
    buyer_number = forms.CharField(label="Номер телефона", max_length=15)
