from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(String(20), primary_key=True)
    name = Column(String(100))
    animal_type = Column(String(20))
#    tags = Column(String(100))
    created = Column(DateTime())
    
    def update(self, id=None, name=None, animal_type=None, tags=None, created=None):
        if name is not None:
            self.name = name
        if animal_type is not None:
            self.animal_type = animal_type
#        if tags is not None:
#            self.tags = tags
        if created is not None:
            self.created = created
        
    def dump(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])

