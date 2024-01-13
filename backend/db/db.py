#TODO refactoring: look up for Eloquent-like ORM for MongoDB

class db:
    def __init__(self, connection):
        self.db = connection
        self.Adventure = self.Adventure(self)
        self.History = self.History(self)

    

    class History:
        def __init__(self, parent):
            self.parent = parent
            self.collection = self.parent.db.games_history

        def addToHistory(self, role, content):
            new_message = self.collection.insert_one({'role': role, 'content': content})
            return new_message.inserted_id
    """ [
        {
            adventure_id: string,
            history: 
            [
                {
                    role: 'user' | 'assistant',
                    content: string
                },
                {
                    role: 'user' | 'assistant',
                    content: string
                }        
            ]
        },
        {
            adventure_id: string,
            history: 
            [
                {
                    role: 'user' | 'assistant',
                    content: string
                },
                {
                    role: 'user' | 'assistant',
                    content: string
                }        
            ]
        },
    ] """

    