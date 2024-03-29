import datetime
from haystack import indexes
from apps.goods.models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引类"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        return SKU.objects.all()
    