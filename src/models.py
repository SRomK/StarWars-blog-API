from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


                              
planetsfavourites = db.Table('planetsfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True))

favourite_character= db.Table('favourite_character',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("people_id", db.Integer, db.ForeignKey("people.id"), primary_key=True))

class User(db.Model):
    __tablename__: 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(1000), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    have_user_planets = db.relationship('Planets', secondary = speciesfavourites, back_populates="have_user_planetsfav")

    have_char = db.relationship("People", secondary=favourite_character, back_populates="have_user")
                              
    

    def __repr__(self):
        return f'User is {self.username}, with {self.email} and {self.id}'
    

    def to_dict(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email,
            "planets": [planets.to_dict() for planets in self.have_user_planets],
            "characters": [people.to_dict() for people in self.have_char] 
        }

    def create(self):
       db.session.add(self)
       db.session.commit()


    @classmethod
    def get_by_email(cls, email):
        account = cls.query.filter_by(email=email).one_or_none()
        return account


    @classmethod
    def get_by_password(cls, password):
        secretPass = cls.query.filter_by(password=password).one_or_none()
        return secretPass

    @classmethod
    def get_all(cls):
        users = cls.query.all()
        return users
  

    @classmethod
    def get_by_id(cls, id):
        user_id = cls.query.get(id)
        return user_id





@classmethod
def get_by_id(cls, id):
    starship = cls.query.get(id)
    return starship
                              
    @classmethod
    def get_user_by_id(cls,id):
        user = cls.query.get(id)
        return user
    
    def add_fav_species(self,specie):
        self.have_user_species.append(specie)
        db.session.commit()
        return self.have_user_species
    
    def new_fav_people (self,people):
        self.have_char.append(people)
        db.session.commit()
        return self.have_char


class Planets(db.Model):
    __tablename__:"planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey("planets_details.id"), nullable=False)

    planets_have = db.relationship("PlanetsDetails", back_populates = "planets_have_details")
    have_user_speciesfav= db.relationship('User', secondary= speciesfavourites, back_populates="have_user_species")

    def __repr__(self):
        return f'Planets: {self.id}, name: {self.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    @classmethod    
    def get_all(cls):
        planets = cls.query.all()
        return planets

    @classmethod
    def get_by_id(cls, id):
        planets = cls.query.get(id)
        return planets
                              
class People(db.Model):
    __tablename__: "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("people_detail.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    people_has_details = db.relationship("PeopleDetail", back_populates="detail_has_character")
    have_user = db.relationship("User", secondary=favourite_character, back_populates="have_char")


    def __repr__(self):
        return f'People is {self.name}, url: {self.url}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def get_all(cls):
        character_list = cls.query.all()
        return character_list


    @classmethod
    def get_by_id(cls, id):
        character = cls.query.get(id)
        return character
       
                        
class PlanetsDetails(db.Model):
    __tablename__:"planets_details"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)

    planets_have_details = db.relationship('Planets', back_populates="planets_have")

    def __repr__(self):
        return f'PlanetsDetails is {self.classificacion}, name:{self.name}' 
        
    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name,
        }
    
    @classmethod
    def get_all_planetsdetails(cls):
        planetsdetails = cls.query.all()
        return planetsdetails
    
    @classmethod
    def get_by_id_planetsdetails(cls,id):
        planetsdetails = cls.query.get(id)
        return planetsdetails
   

class PeopleDetail(db.Model):
    __tablename__: "people_detail" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)

    detail_has_character = db.relationship("People", back_populates="people_has_details")


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "homeworld": self.homeworld
        }