from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .line_user import LineUser
from .keyword import Keyword
from .product import Product
from .rekomendasi_product import RekomendasiProduct
from .pelanggan import Pelanggan
from .transaksi import Transaksi, StatusPembayaran, StatusTransaksi