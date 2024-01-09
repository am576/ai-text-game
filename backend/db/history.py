import json
from sqlalchemy import create_engine, Column, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import shutil

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
            character_description = Column(Text)
            avatar_description = Column(Text)
    
    

    def addAdventure(self, name, description, character_description, avatar_description, world_preview, avatar_preview):
        # if len(type) > 64:
            # raise ValueError("Type exceeds maximum length of 64 characters")
        if len(name) > 64:
            raise ValueError("Name exceeds maximum length of 64 characters")
        if description is not None and len(description) > 1024:
            raise ValueError("Description exceeds maximum length of 1024 characters")
        if len(character_description) > 1024:
            raise ValueError("Character description exceeds maximum length of 1024 characters")
        if len(avatar_description) > 1024:
            raise ValueError("Avatar description exceeds maximum length of 120 characters")
        
        new_adventure = self.Adventure(type='type', name=name, description=description, character_description=character_description, avatar_description=avatar_description)
        self.session.add(new_adventure)
        self.session.commit()
        self.saveAdventurePreviews(new_adventure.id, world_preview, avatar_preview)
        self.session.close()
        
        
    def saveAdventurePreviews(self, adventure_id, world_preview, avatar_preview):
        adventure_path = f'../frontend/src/assets/adventures/{adventure_id}'
        os.makedirs(adventure_path, exist_ok=True)

        preview_destination = os.path.join(adventure_path, 'preview.png')
        avatar_destination = os.path.join(adventure_path, 'avatar.png')

        shutil.copy(world_preview, preview_destination)
        shutil.copy(avatar_preview, avatar_destination)

        

    def getAdventures(self):
        adventures = self.session.query(self.Adventure).all()
        adventures_json = []

        for adventure in adventures:
            adventure_dict = {
                'id': adventure.id,
                'name': adventure.name,
                'description': adventure.description,
                'character_description': adventure.character_description,
                'avatar_description': adventure.avatar_description,
                'created': self.userAdventureExists(adventure.id)
            }
            adventures_json.append(adventure_dict)

        return adventures_json

    class UserAdventure(Base):
            __tablename__ = 'user_adventures'

            id = Column(Integer, primary_key=True)
            # user_id = Column(Integer)
            adventure_id = Column(Integer)

    def userAdventureExists(self, adventure_id):
        user_adventure = self.session.query(self.UserAdventure).filter_by(adventure_id=adventure_id).first()
        return True if user_adventure else False

    def close(self):
         self.session.close()
        