import json
from typing import Dict, Optional, Tuple

from django.db import models

class Item(models.Model):
    """
    Item
    
    name - Name of item
    sku - Sku of item
    imgUrl - url of item img
    info - addictional info of item
    (task) - ManyToMany field  -> Task
    """

    name:str = models.CharField(max_length=25, blank=False)
    sku:str = models.CharField(max_length=30, blank=False, unique=True)
    imgUrl:str = models.CharField(max_length=256, blank=False)
    # info = ArrayField(ArrayField(models.CharField(max_length=256), default=list), default=list)
    infoStr = models.CharField(max_length=1026, blank=True, null=True)

    

    @property
    def info(self) -> Dict[str, Tuple[str, str]]:
        return json.loads(self.infoStr)

    def setInfo(self, data: Dict[str, Tuple[str, str]]) -> None:
        self.infoStr = json.dumps(data)
        self.save()
    
    @classmethod
    def createFromProduct(cls, product, data: Optional[Dict[str, Tuple[str, str]]]={}):
        new_item = cls(
            name=product.name,
            sku=product.sku,
            imgUrl=product.imgUrl
        )
        new_item.setInfo(data)
        new_item.save()

        return new_item

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.sku)


    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['name']
    