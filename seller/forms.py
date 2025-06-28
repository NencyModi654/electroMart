from django import forms
from seller.models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model=Seller
        fields=['seller_name','shop_license']
