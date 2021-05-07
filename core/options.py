from dataclasses import dataclass


@dataclass
class AMQPOptions:
    host: str = "localhost"


@dataclass
class InstaloaderOptions:
    instagram_username: str
    instagram_password: str


@dataclass
class MinioOptions:
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str
    ssl: bool
    region: str
