from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class User(BaseModel):
    id:int
    name:str='ypy'
    age:int
    #等价于date|None
    date_join:Optional[date]
    departments:List[str]

user=User(id=1,name="ypy",age=22,date_join="2026-07-21",departments=['技术部','产品部']) # type: ignore
print(user.model_dump())

