import os

from click import echo
from dependency_injector import containers, providers
from dotenv import load_dotenv

from intranet.in_memory.documents import DocumentInMemoryRepository
from intranet.in_memory.news import NewsInMemoryRepository
from intranet.in_memory.users import UserInMemoryRepository
from intranet.in_memory.users_details import UsersDetailsInMemoryRepository
from intranet.mssql.documents import DocumentMssqlRepository
from intranet.mssql.news import NewsMssqlRepository
from intranet.mssql.user_details import UserDetailsMssqlRepository
from intranet.mssql.users import UserMssqlRepository


class Container(containers.DeclarativeContainer):
    load_dotenv()

    if "DB_HOST" in os.environ:
        echo("Using MsSQL repository")
    else:
        echo("Using In-Memory repository")

    user_repository = providers.Singleton(
        lambda: UserMssqlRepository()
        if "DB_HOST" in os.environ
        else UserInMemoryRepository()
    )

    user_details_repository = providers.Singleton(
        lambda: UserDetailsMssqlRepository()
        if "DB_HOST" in os.environ
        else UsersDetailsInMemoryRepository()
    )

    news_repository = providers.Singleton(
        lambda: NewsMssqlRepository()
        if "DB_HOST" in os.environ
        else NewsInMemoryRepository()
    )

    document_repository = providers.Singleton(
        lambda: DocumentMssqlRepository()
        if "DB_HOST" in os.environ
        else DocumentInMemoryRepository()
    )
