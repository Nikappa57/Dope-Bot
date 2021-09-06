import json
import requests
from typing import Any, Dict, List
from datetime import date, datetime, timedelta

from django.contrib.auth.models import User

from dope.models.task import Task
from dope.models.gateway import Suffix
from dope.utils.productModel import Product



def getProductFootLocker(gateway: Suffix, sku: str) -> Dict[str, Any]:
    # TODO
    productObj = Product(
        name='Product Name', 
        imgUrl='https://images.footlocker.com/content/dam/final/fleu-brand-logos/Reebok.jpg?wid=280&hei=280&fmt=png-alpha',
        relaseDate=datetime.now() + timedelta(days=3,),
        sku=sku
    )
    
    product = {
        "obj": productObj,
        "choices": {
            "size": (
                ("SIZECODE_21490814", "12"),
                ("SIZECODE_214923414", "13"),
                ("SIZECODE_1412412814", "14"),
            ),
            "style": (
                ("White Melange", "White Melange"),
                ("Particle Grey", "Particle Grey")
            ),
            "color": (
                ("White Melange", "White Melange"),
                ("Particle Grey", "Particle Grey")
            ),
        }
    }

    return product

def getDropListFootLocker(gateway: Suffix) -> List[Product]:
    session = requests.Session()

    session.headers.update({
        'Host': gateway.url, # it depends on which state you choose
        'User-Agent': 'FLEU/CFNetwork/Darwin',
        'Accept': '*/*',
        'Accept-Language': 'it-IT,it',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
    })

    response = session.get("https://{}/apigate/release-calendar".format(
        gateway.url
    ))

    today = date.today()
    maxDate = today + timedelta(days=14)

    def calendarFilter(product):
        dropDate = datetime.strptime(product['skuLaunchDate'], '%b %d %Y %H:%M:%S %Z%z').date()
        return dropDate > today and dropDate < maxDate and not product['onlyInStore']
    
    print(json.loads(response.text))
    calendar = json.loads(response.text)['releaseCalendarProducts']

    products = [Product(
        name=product['name'],
        sku=product['id'], 
        relaseDate=datetime.strptime(product['skuLaunchDate'], '%b %d %Y %H:%M:%S %Z%z').date(),
        imgUrl=product['image'],
        ) for product in list(filter(calendarFilter, calendar))]

    return products