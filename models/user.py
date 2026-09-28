# class User:
#     def __init__(self,email,password):
#         self.email = email
#         self.password = password
from dataclasses import dataclass, field


@dataclass
class User:
    email:str
    password: str = field(repr=False)