from django.forms import ModelForm
from shopbase.models import GameProduct

class GameProductForm(ModelForm):
    class Meta:
        model = GameProduct
        fields= ('__all__')