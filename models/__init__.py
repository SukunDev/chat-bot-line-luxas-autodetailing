from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .line_user import LineUser
from .keyword import Keyword
from .rich_menu import RichMenu
from .setting import Setting
from .product import Product
from .pelanggan import Pelanggan