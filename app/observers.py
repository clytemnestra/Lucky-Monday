from abc import abstractmethod


class CommandOutput:
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notifyObserver(self, observer_notify, data):
        for observer in self.observers:
            if observer == observer_notify:
                observer.update(data)

    def notifyObservers(self, data):
        for observer in self.observers:
            observer.update(data)


class CommandObserver:
    @abstractmethod
    def update(self, data):
        return


class CommandLogger(CommandObserver):
    def update(self, data):
        #todo add logging
        print(data)
        pass


class CommandPrinter(CommandObserver):
    def update(self, data: str):
        print(data)
