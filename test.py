from sqlalchemy_enum34 import Enum


class MyEnum(Enum):
    a = 'aaa'
    b = 124


print(MyEnum.a)
print(MyEnum.b)
if MyEnum.b == 124:
    print(MyEnum.b)

