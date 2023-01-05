from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from website import db, ma, app

Base = declarative_base()


class Address(Base):
     __tablename__ = "address"

     id = Column(Integer, primary_key=True)
     email_address = Column(String, nullable=False)
     def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class Auditable(Base):
    __abstract__ = True
    id = Column(Integer(), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False)


class Translatable(Auditable, Base):
    __abstract__ = True
    name_en_us = Column(String)
    name_ru_ru = Column(String)
    name_uz_crl = Column(String)
    name_uz_uz = Column(String)


class Groups(Translatable, Base):
    __tablename__ = "groups"
    number = Column(Integer)


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base.metadata.create_all(bind=engine)


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    photo_url = db.Column(db.String(length=1024), nullable=False, unique=True)
    name = db.Column(db.String(length=1024), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    phone = db.Column(db.String(length=60), nullable=False, unique=True)
    provider_id = db.Column(db.String(length=1024), nullable=False)
    uid = db.Column(db.String(length=1024), nullable=False, unique=True)
    email_verified = db.Column(db.Boolean(), nullable=False)

    created_date = db.Column(db.DateTime(), default=db.func.now())
    login_date = db.Column(db.DateTime(), nullable=False)
    login_count = db.Column(db.Integer(), nullable=True, default=1)
    logout_date = db.Column(db.DateTime(), nullable=False)
    logout_count = db.Column(db.Integer(), nullable=True, default=0)
    active = db.Column(db.Boolean(), nullable=False)
    chat_user_relation = relationship("ChatUserRelation", back_populates="user")

    @property
    def serializable(self):
        return {
            self.id,
            self.name
        }

    def toDict(self):
        return dict(
            id=self.id,
            photo_url=self.photo_url,
            name=self.name,
            email=self.email,
            phone=self.phone,
            provider_id=self.provider_id,
            uid=self.uid,
            email_verified=self.email_verified,
            active=self.active,
        )


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Boolean())
    created_by = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())
    last_modified_by = db.Column(db.Integer())
    last_modified_date = db.Column(db.DateTime())
    is_deleted = db.Column(db.Boolean(), default=False)
    chat_user_relation = relationship("ChatUserRelation", back_populates="chat")
    chat_message = relationship("ChatMessage", back_populates="chat")


class ChatMessage(db.Model):
    __tablename__ = "chat_message"
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey('chat.id'))
    chat = relationship("Chat", back_populates="chat_message")
    type = db.Column(db.Boolean())
    text = db.Column(db.String(length=1024))
    file_name = db.Column(db.String(length=1024))
    sender_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer())
    created_date = db.Column(db.DateTime())
    last_modified_by = db.Column(db.Integer())
    last_modified_date = db.Column(db.DateTime())
    is_seen = db.Column(db.Boolean(), default=False)
    is_deleted = db.Column(db.Boolean(), default=False)
    text_type = db.Column(db.String(20))
    parent_id = db.Column(db.Integer(), db.ForeignKey("chat_message.id"))

    def toDict(self):
        return dict(
            id=self.id,
            type=self.type,
            text=self.text,
            file_name=self.file_name,
            sender_id=self.sender_id,
            chat_id=self.chat_id,
            created_by=self.created_by,
            created_date=self.created_date,
            last_modified_by=self.last_modified_by,
            last_modified_date=self.last_modified_date,
            is_seen=self.is_seen,
            is_deleted=self.is_deleted,
            text_type=self.text_type,
            parent_id=self.parent_id,
        )


class ChatUserRelation(db.Model):
    __tablename__ = "chat_user_relation"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = relationship("Users", back_populates="chat_user_relation")
    chat_id = db.Column(db.Integer(), db.ForeignKey('chat.id'))
    chat = relationship("Chat", back_populates="chat_user_relation")
    count_new_message = db.Column(db.Integer(), default=0)
    role = db.Column(db.Boolean())
    title = db.Column(db.String(length=1024))
    is_deleted = db.Column(db.Boolean(), default=False)

    @property
    def serializable(self):
        return {
            self.id,
            self.count_new_message,
            self.role,
            self.title,
            self.user_id,
            self.chat_id,
            self.is_deleted,
        }

    def toDict(self):
        return dict(
            id=self.id,
            count_new_message=self.count_new_message,
            role=self.role,
            title=self.title,
            user_id=self.user_id,
            chat_id=self.chat_id,
            is_deleted=self.is_deleted,
        )


class ChatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chat
        include_fk = True


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class ChatUserRelationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatUserRelation
        include_fk = True
    user = ma.Nested(UserSchema)
    chat = ma.Nested(ChatSchema)


chat_user_relation_schema = ChatUserRelationSchema()
chat_user_relations_schema = ChatUserRelationSchema(many=True)


class ChatMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatMessage
        include_fk = True
    chat = ma.Nested(ChatSchema)


chat_message_schema = ChatMessageSchema()
chat_messages_schema = ChatMessageSchema(many=True)


class savollar(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    savol = db.Column(db.String(length=1024), nullable=False, unique=True)
    javob_a = db.Column(db.String(length=1024), nullable=False)
    javob_b = db.Column(db.String(length=1024), nullable=False)
    javob_c = db.Column(db.String(length=1024), nullable=False)
    javob_d = db.Column(db.String(length=1024), nullable=False)
    javob = db.Column(db.String(length=1024), nullable=False)
    bilet = db.Column(db.Integer(), nullable=False)
    rasm = db.Column(db.String(length=1024), nullable=False)


class ListTextValue:

    def __init__(self, old_value, new_value):
        self.old_value = old_value
        self.new_value = new_value


TextList = [ListTextValue(65, 1040), ListTextValue(66, 1041), ListTextValue(68, 1044), ListTextValue(69, 1045),
            ListTextValue(70, 1060), ListTextValue(71, 1043), ListTextValue(72, 1202), ListTextValue(73, 1048),
            ListTextValue(74, 1046), ListTextValue(75, 1050), ListTextValue(76, 1051), ListTextValue(77, 1052),
            ListTextValue(78, 1053), ListTextValue(79, 1054), ListTextValue(80, 1055), ListTextValue(81, 1178),
            ListTextValue(82, 1056), ListTextValue(83, 1057), ListTextValue(84, 1058), ListTextValue(85, 1059),
            ListTextValue(86, 1042), ListTextValue(87, 87), ListTextValue(88, 1061), ListTextValue(89, 1049),
            ListTextValue(90, 1047), ListTextValue(97, 1040), ListTextValue(98, 1041), ListTextValue(100, 1076),
            ListTextValue(101, 1077), ListTextValue(102, 1092), ListTextValue(103, 1075), ListTextValue(104, 1203),
            ListTextValue(105, 1080), ListTextValue(106, 1078), ListTextValue(107, 1082), ListTextValue(108, 1083),
            ListTextValue(109, 1084), ListTextValue(110, 1085), ListTextValue(111, 1086), ListTextValue(112, 1087),
            ListTextValue(113, 1179), ListTextValue(114, 1088), ListTextValue(115, 1089), ListTextValue(116, 1090),
            ListTextValue(117, 1091), ListTextValue(118, 1074), ListTextValue(119, 119), ListTextValue(120, 1093),
            ListTextValue(121, 1081), ListTextValue(122, 1079), ListTextValue(700, 1098), ListTextValue(96, 1098),
            ListTextValue(39, 1098), ListTextValue(1040, 65), ListTextValue(1041, 66), ListTextValue(1044, 68),
            ListTextValue(1045, 69), ListTextValue(1060, 70), ListTextValue(1043, 71), ListTextValue(1202, 72),
            ListTextValue(1048, 73), ListTextValue(1046, 74), ListTextValue(1050, 75), ListTextValue(1051, 76),
            ListTextValue(1052, 77), ListTextValue(1053, 78), ListTextValue(1054, 79), ListTextValue(1055, 80),
            ListTextValue(1178, 81), ListTextValue(1056, 82), ListTextValue(1057, 83), ListTextValue(1058, 84),
            ListTextValue(1059, 85), ListTextValue(1042, 86), ListTextValue(87, 87), ListTextValue(1061, 88),
            ListTextValue(1049, 89), ListTextValue(1047, 90), ListTextValue(1040, 97), ListTextValue(1041, 98),
            ListTextValue(1076, 100), ListTextValue(1077, 101), ListTextValue(1092, 102), ListTextValue(1075, 103),
            ListTextValue(1203, 104), ListTextValue(1080, 105), ListTextValue(1078, 106), ListTextValue(1082, 107),
            ListTextValue(1083, 108), ListTextValue(1084, 109), ListTextValue(1085, 110), ListTextValue(1086, 111),
            ListTextValue(1087, 112), ListTextValue(1179, 113), ListTextValue(1088, 114), ListTextValue(1089, 115),
            ListTextValue(1090, 116), ListTextValue(1091, 117), ListTextValue(1074, 118), ListTextValue(119, 119),
            ListTextValue(1093, 120), ListTextValue(1081, 121), ListTextValue(1079, 122), ListTextValue(1066, 0),
            ListTextValue(1098, 700), ListTextValue(1068, 0), ListTextValue(1100, 0), ListTextValue(1067, 0),
            ListTextValue(1099, 0)]
