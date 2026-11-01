from pydantic import BaseModel, Field
class Student(BaseModel):
    id :int
    name :str=Field(min_length=2)
    age :int =Field(ge=5,le=100)
    email:str
    marks:float =Field(default=0,ge=0,le=100)
