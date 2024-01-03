import json
from sqlalchemy import create_engine, Column, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class History:
    Base = declarative_base()
    def __init__(self):
        engine = create_engine('sqlite:///db/history.db', echo=True)

        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.Base = declarative_base()

    class Message(Base):
            __tablename__ = 'history'

            id = Column(Integer, primary_key=True)
            role = Column(Enum('user', 'assistant'))
            content = Column(Text)

    def addToHistory(self, role, content):
        new_message = self.Message(role=role, content=content)
        self.session.add(new_message)
        self.session.commit()
        self.session.close()


    def getHistory(self):
        messages = self.session.query(self.Message).all()
        json_data = {
            "model": "dolphin",
            "messages": []
        }

        for message in messages:
            json_data["messages"].append({
                "id": message.id,
                "role": message.role,
                "content": message.content
        })
        return json_data

    class Adventure(Base):
            __tablename__ = 'adventures'

            id = Column(Integer, primary_key=True)
            type = Column(Text)
            name = Column(Text)
            description = Column(Text)

    def addAdventure(self, type, name, description):
        new_adventure = self.Adventure(type=type, name=name, description=description)
        self.session.add(new_adventure)
        self.session.commit()
        self.session.close()


    
        