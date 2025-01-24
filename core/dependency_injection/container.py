# core/container.py
from dependency_injector import containers, providers
from core.data.mongo_handler import MongoDBHandler

class Container(containers.DeclarativeContainer):
    user_handler = providers.Singleton(MongoDBHandler, collection_name='users')
    product_handler = providers.Singleton(MongoDBHandler, collection_name='products')
    