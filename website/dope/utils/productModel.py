from datetime import datetime

class Product:
    def __init__(self, name:str, sku:str, relaseDate:datetime, imgUrl:str) -> None:
        self.name = name
        self.sku = sku
        self.relaseDate = relaseDate
        self.imgUrl = imgUrl