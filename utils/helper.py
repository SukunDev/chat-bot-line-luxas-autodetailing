from typing import List
from models import Product
import locale

def format_uang(nilai):
    locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
    formatted_uang = locale.format_string("%.2f", nilai, grouping=True)
    
    return formatted_uang

def create_carousel_product(products: List[Product]):
    list_product = []
    for product in products:
        list_product.append({"type": "bubble","body": {"type": "box","layout": "vertical","contents": [{"type": "image","url": product.thumbnail,"size": "full","aspectMode": "cover","aspectRatio": "2:3","gravity": "top"},{"type": "box","layout": "vertical","contents": [{"type": "box","layout": "vertical","contents": [{"type": "text","text": product.name,"size": "xl","color": "#ffffff","weight": "bold"}]},{"type": "box","layout": "baseline","contents": [{"type": "text","text": f"{product.description}","color": "#ebebeb","size": "sm","flex": 0}],"spacing": "lg"},{"type": "box","layout": "baseline","contents": [{"type": "text","text": "Price","color": "#ebebeb","size": "sm","flex": 0},{"type": "text","text": f": Rp. {format_uang(product.price)}","color": "#ebebeb","size": "sm","flex": 0}],"spacing": "lg"},{"type": "box","layout": "vertical","contents": [{"type": "filler"},{"type": "box","layout": "baseline","contents": [{"type": "filler"},{"type": "icon","url": "https://developers-resource.landpress.line.me/fx/clip/clip14.png"},{"type": "text","text": "Pesan","color": "#ffffff","flex": 0,"offsetTop": "-2px"},{"type": "filler"}],"spacing": "sm"},{"type": "filler"}],"borderWidth": "1px","cornerRadius": "4px","spacing": "sm","borderColor": "#ffffff","margin": "xxl","height": "40px","action": {"type": "postback","data": f"pesan_product_{product.id}"}}],"position": "absolute","offsetBottom": "0px","offsetStart": "0px","offsetEnd": "0px","backgroundColor": "#03303Acc","paddingAll": "20px","paddingTop": "18px"},{"type": "box","layout": "vertical","contents": [{"type": "text","text": "SALE","color": "#ffffff","align": "center","size": "xs","offsetTop": "3px"}],"position": "absolute","cornerRadius": "20px","offsetTop": "18px","backgroundColor": "#ff334b","offsetStart": "18px","height": "25px","width": "53px"}],"paddingAll": "0px"}})
    return {"type": "carousel", "contents": list_product}