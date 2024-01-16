from db.models import Adventure, History

class Game:
    def __init__(self, adventure_id):
        self.adventure_id = adventure_id
        self.history = History(adventure_id)
        self.adventure = Adventure()
        self.adventure.set_created(adventure_id)

    @staticmethod
    def load(adventure_id):
        return Game(adventure_id)

    def addToHistory(self, role, content):
        self.history.add(role, content)

    def getHistory(self):
        return self.history.getAll()
    
    def generateScenario(self):
        pass

    """ scenario = {
            world : {
                description : "",
                places: [
                
                ],
                characters: [
                    
                ],
                events: [
                    
                ]
            },
            story : {
                opening : "",
                plotShort: "",
                plotFull: "",
            }
    }"""