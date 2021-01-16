from abc import ABC, abstractmethod   
# # class Compressor(ABC):
# #     @abstractmethod
# #     def compress(self):
# #         pass

# # class Filter:
# #     @abstractmethod
# #     def filter(self):
# #         pass




# # class BW(Filter):
# #     def filter(self):
# #         print("BW filter applied")

# # class Zip(Compressor):
# #     def compress(self):
# #         print("Zip compression")


# # class ImageStorer:
# #     def ImageStorage(self, Storage):
# #         Storage.compress()

# #     def ChangeColor(self, Filter):
# #         Filter.filter()




# # class AuditTrail:
# #     def record(self):
# #         print("Record")

# # class Task(AuditTrail, ABC):
# #     def execute(self):
# #         self.record()
# #         self.doExecute()
    
# #     @abstractmethod
# #     def doExecute(self):
# #         pass

# # class TransferMoneyTask(Task):
# #     def doExecute(self):
# #         print("Transfer money")
    

# # class Observer(ABC):
# #     @abstractmethod
# #     def update(self):
# #         pass

# # class Spreadsheet(Observer):
# #     def update(self):
# #         print("Spread sheet notified")

# # class Subject:
# #     observers = []
# #     def addObserver(self, observer):
# #         self.observers.append(observer)
    
# #     def removeObserver(self, observer):
# #         self.observers.remove(observer)

# #     def notifyObservers(self):
# #         for x in range(len(self.observers)):
# #             self.observers[x].update()


# # class Graph(Observer):
# #     def update(self):
# #         print("Graph notified")
        
# # class NumberStorer(Subject):
# #     def changeNumber(self, number):
# #         self.notifyObservers()


# # class UIControl:
# #     owner = DialogBox()
# #     def __init__(self, owner):
# #         self.owner = owner
# # class oneTimer(Observer):
# #     def update(self, saveButton, titleTextBox)
# #         isEmpty = (content == None)
# #         saveButton.setEnabled(not isEmpty)
# #         titleTextBox.setContent(self.articlesListBox.content)
# #         saveButton.setEnabled(True)
# # class ArticlesDialogBox:
# #     articlesListBox = ListBox()
# #     titleTextBox = TextBox()
# #     saveButton = Button()
# #     def __init__
# #     def sim(self):
# #         self.articlesListBox.setSelection("Articles 1")
# #         print("Button" + self.saveButton.isEnabled)
# #         print("Textbox" + self.titleTextBox.content)
# #     def changed(self, control):
# #         if control == self.articlesDialogBox:
         
# #         elif control == self.titleTextBox:
# #             content = self.titleTextBox.content
         

# # class ListBox(UIControl):
# #     content = ""
# #     def __init__(self, owner):
# #         self.owner = owner
# #     def setSelection(self, selection):
# #         self.content = selection
# #         self.owner.changed(self)




    









# # # class Observer(ABC):
# # #     @abstractmethod
# # #     def update(self):
# # #         pass

                                                                                                                
# # # class Subject(Observer):
# # #     observers = []
# # #     def addObserver(self, observer):
# # #         self.observers.append(observer)
# # #     def notify(self):
# # #         for x in range(len(self.observers))
# # #             self.observers[x].update()
 

# # # class GameObject(ABC):
# # #     @abstractmethod
# # #     def get_x_coordinate(self):
# # #         pass
# # #     @abstractmethod
# # #     def get_y_coordinate(self):
# # #         pass
# # #     @abstractmethod
# # #     def change_x_coordinate(self):
# # #         pass
# # #     @abstractmethod
# # #     def change_y_coordinate(self):
# # #         pass
    

# # # class DialogBox(ABC):
# # #     @abstractmethod changed


# # class Observer(ABC):
# #     @abstractmethod
# #     def update(self):
# #         pass


# # class UIControl:
# #     observers = []
# #     def addObserver(self, observer):
# #         self.observers.append(observer)

# #     def notifyObservers(self):
# #         for x in range(len(self.observers)):
# #             self.observers[x].update()

# # class button(UIControl):
# #     isEnabled = False
# #     def setEnabled(self, enabled):
# #         self.isEnabled = enabled
# #         self.notifyObservers()

# # class TextBox(UIControl):
# #     content = ""
# #     def setContent(self, content):
# #         self.content = content
# #         self.notifyObservers()

# from abc import ABC, abstractmethod
# import pygame

# # Up is down. Down is up.
# # No spaces between functions in a class
# screenWidth = 800
# screenHeight = 1250
# nameOfGame = "robowars"
# win = pygame.display.set_mode((screenWidth, screenHeight))
# pygame.display.set_caption(f'{nameOfGame}')
# background = (0, 0, 0)



# # class Observer(ABC):
# #     @abstractmethod
# #     def update(self):
# #         pass

                                                                                                                
# # class Subject(Observer):
# #     observers = []
# #     def addObserver(self, observer):
# #         self.observers.append(observer)
# #     def notify(self):
# #         for x in range(len(self.observers))
# #             self.observers[x].update()
 

# # class GameObject(ABC):
# #     @abstractmethod
# #     def get_x_coordinate(self):
# #         pass
# #     @abstractmethod
# #     def get_y_coordinate(self):
# #         pass
# #     @abstractmethod
# #     def change_x_coordinate(self):
# #         pass
# #     @abstractmethod
# #     def change_y_coordinate(self):
# #         pass
    

  
# class Character:
#     characterColor = (250, 0, 0)
#     x_coordinate = 50
#     y_coordinate = 50
#     length = (screenWidth / 100) * 5
#     height = (screenHeight / 100) * 5
#     movement = screenWidth / 550
#     movementDown = 5
#     jumped = 0
#     moveDown = True
#     onPlatform = True
#     moveLeft = True
#     moveRight = True
#     grabBall = False
#     jumpTime = 0
#     maxJump = 0
#     jumping = False
#     canJump = True
#     def getHeight(self):
#         return self.height
#     def get_x_coordinate(self):
#         return self.x_coordinate
#     def get_y_coordinate(self):
#         return self.y_coordinate
#     def change_x_coordinate(self, x_coordinate):
#         self.x_coordinate = x_coordinate
#     def change_y_coordinate(self, y_coordinate):
#         self.y_coordinate = y_coordinate
#     def getLength(self):
#         return self.length
#     def jump(self):
#         jumpPower = 0
# #         if self.jumped <= self.maxJump:
# #             self.y_coordinate -= 5
# #             self.jumped += 5
# #         if self.jumped >= self.maxJump:
# #             self.jumped = 0
# #             self.maxJump = 0
# #             self.jumping = False
# #             # self.y_coordinate = 0
# #             self.jumpTime = 0
# #         if self.jumpTime < 5:
# #             self.maxJump = 150
# #         elif self.jumpTime < 9:
# #             self.maxJump = 200
# #         elif self.jumpTime < 12:
# #             self.maxJump = 250
# #     def controls(self):
# #         self.movements()
# #     def setCharacterCoordinates(self, x_coordinate, y_coordinate):
# #         self.y_coordinate = y_coordinate
# #         self.x_coordinate = x_coordinate
    



# # class Platform:
# #     platformColor = (80, 21, 46)
# #     x_coordinate = 0
# #     y_coordinate = 600
# #     length = 1000
# #     width = 200
# #     def get_x_coordinate(self):
# #         return self.x_coordinate
# #     def get_y_coordinate(self):
# #         return self.y_coordinate
# #     def change_x_coordinate(self, x_coordinate):
# #         self.x_coordinate = x_coordinate
# #     def change_y_coordinate(self, y_coordinate):
# #         self.y_coordinate = y_coordinate





# # class Ball:
# #     color = (0, 0, 250)
# #     x_coordinate = 90
# #     y_coordinate = 90
# #     length = 10
# #     height = 10
# #     def getHeight(self):
# #         return self.height
# #     def getLength(self):
# #         return self.length
# #     def get_x_coordinate(self):
# #         return self.x_coordinate
# #     def get_y_coordinate(self):
# #         return self.y_coordinate
# #     def change_x_coordinate(self, x_coordinate):
# #         self.x_coordinate = x_coordinate
# #     def change_y_coordinate(self, y_coordinate):
# #         self.y_coordinate = y_coordinate
# #     def update(self):
# #         pass


# # class CollisionsFinder:
# #     def onPlatform(self, platform, character):
# #         characterCoordinate = character.get_y_coordinate() + character.getHeight() 
# #         platformCoordinate = platform.get_y_coordinate()
# #         return (characterCoordinate >= platformCoordinate)


# # class PhysicsEngine:
# #     gravityPull = 2
# #     def setGravity(self, gravity):
# #         self.gravity = gravity
# #     def gravity(self, Platform, Object):
# #         collisions = CollisionsFinder()
# #         onSolidObject = collisions.onPlatform(Platform, Object)
# #         if not onSolidObject:
# #             object_y_coordinate = Object.get_y_coordinate() + self.gravityPull
# #             Object.change_y_coordinate(object_y_coordinate)
# #     def movementPossible(self, Platform, Character):
# #         collisions = CollisionsFinder()
# #         onSolidObject = collisions.onPlatform(Platform, Character)
# #         if onSolidObject:
# #             Character.onPlatform = True
# #             Character.moveDown = False
# #         else:
# #             Character.onPlatform = False
# #             Character.moveDown = True
# #     def boundaries(self, Object):
# #         if Object.get_x_coordinate() <= 0:
# #             Object.moveLeft = False
# #         else:
# #             Object.moveLeft = True
# #         if Object.get_x_coordinate() >= screenWidth - Object.getLength():
# #             Object.moveRight = False
# #         else:
# #             Object.moveRight = True

# # class Interactions:
# #     def interactions(self, character, ball):
# #         if character.grabBall:
# #             self.grabBall(character, ball)
# #     def grabBall(self, charcter, ball):
# #         ball_y_coordinate = charcter.get_y_coordinate() + (charcter.getHeight() / 2)
# #         ball_x_coordinate = charcter.get_x_coordinate() - 10
# #         ball.change_y_coordinate(ball_y_coordinate)
# #         ball.change_x_coordinate(ball_x_coordinate)


# # ball = Ball()
# # doggo = Character()
# # run = True
# # platform1 = Platform()
# # physics = PhysicsEngine()
# # interactionsFinder = Interactions()
# # physics.gravity(platform1, doggo)
# # physics.gravity(platform1, ball)
# # physics.boundaries(doggo)
# # physics.boundaries(ball)
# # physics.movementPossible(platform1, doggo)
# # interactionsFinder.interactions(doggo, ball)
 

# # pygame.quit()
# class HttpRequest:
#     username = ""
#     password = ""
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#     def getUsername(self):
#         return self.username
#     def getPassword(self):
#         return self.password
# class Handler(ABC):
#     next = Handler()
#     def __init__(self, next):
#         self.next = next
#     @abstractmethod
#     def handle(self, request):
#         if self.doHandle(request):
#             return
#         self.next.handle(request)
#     def doHandle(self, request):
#         pass


# class Authenticator(Handler):
#     def doHandle(self, request):
#         isValid = (request.getUsername() == "admin"
#          and request.getPassword() == "1234")
#         return not isValid


# class Compressor(Handler):
#     def doHandle(self, request):
#         print("compress")
#         return False

# class Logger(Handler):
#     def doHandle(self, request):
#         print("log")
#         return False


# class WebServer:
#     handler = Handler()
#     def __init__(self, handler):
#         self.handler = handler
#     def handle(self, request):
#         self.handler.handle(request)


class Operation(ABC):
    @abstractmethod
    def apply(self, heading):
        pass
    @abstractmethod
    def apply(self, anchor):
        pass

class HighlightOperation(Operation):
    def apply(self, anchor):
        print("highlight-anchor")
    def apply(self, heading):
        print("highlight-heading")
class HtmlNode(ABC):
    @abstractmethod
    def execute(self, operation):
        pass


class AnchorNode(HtmlNode):
    def execute(self, operation):
        operation.apply(self)


class HeadingNode(HtmlNode):
    def execute(self, operation):
        operation.apply(self)


class HtmlDoc:
    nodes = []
    def add(self, node):
        self.nodes.append(node)
    
    def execute(self, operation):
        try:
            for node in self.nodes:
                node.execute(operation)
        except TypeError:
            pass

class Component(ABC):
    @abstractmethod
    def render(self):
        pass

class Shape(Component):
    def render(self):
        print("shape rendered")


class Group(Component):
    composites = []
    index = 0

    def add(self, component):
        self.composites.append(component)
    
    def render(self):
        if self.index > 10:
            print('error')
            return
        self.index += 1
        for composite in self.composites:
            composite.render()

class Image:
    pass

class Filter(ABC):
    @abstractmethod
    def apply(self, image):
        pass


class VividFilter(Filter):
    def apply(self, image):
        print("Applying vivid")
    

class ImageView:
    image = Image()

    def __init__(self, image):
        self.image = image
    
    def apply(self, filter):
        filter.apply(self.image)

class Adapter(Filter):
    interface = Image()
    image = Image()
    def __init__(self, interface):
        self.interface = interface

    def apply(self, image):
        self.apply(image)

class Caramel:
    def render(self, image):
        print("caramel filter")

class Stream(ABC):
    @abstractmethod
    def write(self, data):
        pass

class CloudStream(Stream):
    def write(self, data):
        print("storing " + data)



class EncryptedCloudStream(Stream):
    stream = ""
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        data = self.encrypt(data)
        self.stream.write(data)
    
    def encrypt(self, data):
        return "&*)*@&1&&$"


class CompressedCloudStream(Stream):
    stream = ""
    def __init__(self, stream):
        self.stream = stream


    def write(self, data):
        data = self.compressed(data)
        self.stream.write(data)

    def compressed(self, data):
        return data[0: 1]


class Message:
    content = ""
    def getContent(self):
        return content
    
class NotificationServer:
    def connect(self, ipAddress):
        return Connection()
    
    def authenticated(self, appId, key):
        return AuthToken()
    
    def send(self, authToken, message, target):
        print("sending a message")
    
class Connection:
    def disconnect(self):
        pass

class AuthToken:
    pass


class RemoteControl:
    device = ""
    def __init__(self, device):
        self.device = device
    def turnOn(self):
        self.device.turnOn()
    def turnOff(self):
        self.device.turnOff()

class AdvancedRemoteControl(RemoteControl):
    device = ""
    def __init__(self, device):
        self.device = device
    
    def setChannel(self, number):
        self.device.setChannel()




class Device(ABC):
    @abstractmethod
    def turnOn(self):
        pass
    @abstractmethod
    def turnOff(self):
        pass
    @abstractmethod
    def setChannel(self, number):
        pass


class SonyTV(Device):
    def turnOn(self):
        print("Sony turn on")
    
    def turnOff(self):
        print("Sony turn off")
    
    def setChannel(self, number):
        print("sony channel number " + number)


    
class Proxy:
    pass

class Ebook:
    fileName = ""

    def __init__(self, fileName):
        self.fileName = fileName
        self.load()
    
    def load(self):
        print("loading ebook " + self.fileName)
    
    def show(self):
        print("showing ebook " + self.fileName)
    
    def getFileName(self):
        return self.fileName

class Library:
    ebooks = {}
    def add(self, ebook):
        self.ebooks[ebook.getFileName()] = ebook
    
    def openEbook(self, fileName):
        self.ebooks.get(fileName).show()
    

l = Library()
fileNames = ["a", "b", "c"]
for fileName in fileNames:
    e = Ebook(fileName)
    l.add(e)

l.openEbook("a")

