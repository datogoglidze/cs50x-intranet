from dependency_injector import containers, providers

from intranet.in_memory.users import UserInMemoryRepository


class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserInMemoryRepository)
