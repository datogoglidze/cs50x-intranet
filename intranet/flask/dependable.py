from dependency_injector import containers, providers

from intranet.in_memory.news import NewsInMemoryRepository
from intranet.in_memory.users_details import UsersDetailsInMemoryRepository
from intranet.mssql.users import UserMssqlRepository


class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserMssqlRepository)
    user_details_repository = providers.Singleton(UsersDetailsInMemoryRepository)
    news_repository = providers.Singleton(NewsInMemoryRepository)
