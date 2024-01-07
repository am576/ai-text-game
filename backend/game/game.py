class Game:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def initRules(self):
        pass

    def generatePlot(self):
        pass

    class Plot:
        def __init__(self, name, description):
            self.name = name
            self.description = description

        def addOpenning(self):
            # Ex: You are a survivor of the nuclear war. You live in a big Russian city that had been partially destroyed by nuclear war.
            # In the previous life you were a taxi driver. Your family was killed in the first minutes of the strike. Now you have nothing to lose.
            # You will survive at any cost.
            pass

        def addPlotComponent(self):
            #This could be a location, a character, an important event that AI should be aware of and be able to incorporate to the story.
            pass

        def addDirection(self):
            pass

        def addGoal(self):
            # Goal of the game, where the AI will be crafting the story towards.
            # It may be vague like "Find what happened to yor dad"
            # Or mo specific like "Survive for 100 days"
            pass

        