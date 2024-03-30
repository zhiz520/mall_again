from haystack import indexes
from apps.goods.models import SKU


class SKUIndexView(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SKU
    
    def index_queryset(self, using=None):
        return SKU.objects.all()
    

