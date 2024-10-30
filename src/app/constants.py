from dataclasses import dataclass as dc


@dc(frozen=True)
class BasicEnum:
    pass


class EnvironmentEnum(BasicEnum):
    LOCAL = 'LOCAL'
    DEV = 'DEV'
    PROD = 'PROD'


class EnvironmentGroups:
    DEVELOPMENT = {
        EnvironmentEnum.LOCAL,
        EnvironmentEnum.DEV,
    }
    OPERATIONAL = {EnvironmentEnum.PROD}


class EnvironmentHandler:

    enum_choices = ('LOCAL', 'DEV', 'PROD')

    @staticmethod
    def get_environment_name(name):
        name = name.upper()
        if name not in EnvironmentHandler.enum_choices:
            raise ValueError(f'not a valid environment name {name}')
        return name
