

class Job():
    def __init__(self, filename, colour, material, user):
        self.filename = filename
        self.colour   = colour
        self.material = material
        self.user     = user
        self.location = 'Pending'
        self.time_remaining = 'Pending'
        self.printing_on = None
