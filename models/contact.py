from dataclasses import dataclass

# class Contact:
#     def __init__(self, name,last_name,phone,email,address,description):
#         self.name = name
#         self.last_name = last_name
#         self.phone = phone
#         self.email = email
#         self.address = address
#         self.description = description

@dataclass
class Contact:
    name:str
    last_name:str
    phone:str
    email:str
    address:str
    description:str

        
