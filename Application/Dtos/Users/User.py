from Domain.Entities.User import User as UserDomainEntity








class User() : 

    Id:str
    Email:str
    RegistrationDate:str

    def __init__(self, user:UserDomainEntity) :
        self.Id = user.Id
        self.Email = user.Email
        self.RegistrationDate = user.RegistrationDate