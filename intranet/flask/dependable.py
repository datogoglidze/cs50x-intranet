from dependency_injector import containers, providers

from intranet.in_memory.users import UserInMemoryRepository
from intranet.in_memory.users_details import UsersDetailsInMemoryRepository


class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserInMemoryRepository)
    user_details_repository = providers.Singleton(UsersDetailsInMemoryRepository)
