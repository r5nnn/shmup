from .. import tools


class Title(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.next = "Options"