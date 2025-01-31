# core/container.py
from dependency_injector import containers, providers
from core.data.mongo_handler import MongoDBHandler

class Container(containers.DeclarativeContainer):
    user_handler = providers.Singleton(MongoDBHandler, collection_name='users')
    product_handler = providers.Singleton(MongoDBHandler, collection_name='products')
    marchand_handler = providers.Singleton(MongoDBHandler, collection_name='marchands')
    fournisseur_handler = providers.Singleton(MongoDBHandler, collection_name='fournisseurs')
    category_handler = providers.Singleton(MongoDBHandler, collection_name='categories')
    client_handler = providers.Singleton(MongoDBHandler, collection_name='clients')
    admin_handler = providers.Singleton(MongoDBHandler, collection_name='admins')
    coupon_handler = providers.Singleton(MongoDBHandler, collection_name='coupons')
    code_promo_handler = providers.Singleton(MongoDBHandler, collection_name='code_promo')
    marche_handler = providers.Singleton(MongoDBHandler, collection_name='marches')
    