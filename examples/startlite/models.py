from dataclasses import dataclass


@dataclass
class HelloWorld:
    environment: str
    secret: str
    hello: str = "world"
