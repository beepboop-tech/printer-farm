import requests

from jobs import Job

class Printer():
    """
    A generic interface to a printer.
    Handels the API calls to octoprint.
    """

    def __init__(self, hostname, api_key, location, printer_type, material_type, material_colour):
        self.url             = 'http://' + hostname
        self.headers         = {'X-Api-Key': api_key}
        self.location        = location
        self.printer_type    = printer_type
        self.material_type   = material_type
        self.material_colour = material_colour

    def api_get(self, endpoint):
        r = requests.get(self.url+endpoint, headers = self.headers)
        if (r.status_code == 200):
            return r.json()
        else:
            return None


    def status(self):
        # TODO: Should this use a physical button?
        stat = self.api_get('/api/printer?exclude=sd')
        if (stat is not None):
            return stat
        else:
            return   {"state": {
                          "text": "Offline",
                          "flags": {
                              "operational": 'false',
                              "paused": 'false',
                              "printing": 'false',
                              "sdReady": 'false',
                              "error": 'false',
                              "ready": 'false',
                              "closedOrError": 'false'
                              }
                          }
                    }


    def can_make(self, job: Job):
        # TODO: Check that this works with a functional printer

        # Check the material and colour are correct
        if (self.material_type != job.material or self.material_colour != job.colour):
            return False

        # Get the printer status
        stat = self.status()

        if (stat['state']['text'] == 'Offline'):
            return False

        if (stat['state']['printing'] == 'true'):
            return False

        if (stat['state'['ready']] == 'false'):
            return False

        return True

    def local_files(self):
        # TODO: this  is not safe if the printer is offline
        return self.api_get('/api/files/local')

    def upload_file(self, filename):
        # TODO check that the file exists
        files = {'file': open(filename, 'rb')}
        print(requests.post(self.url+'/api/files/local', headers = self.headers, files=files ).json())


    def make(self, job: Job):
        """
        Sends the required files and settings to the printer
        """
        pass



p = Printer('10.11.12.166', 'B5A36115A3DC49148EFC52012E7EBCD9', 'q', 'r', 'PLA', 'black')
print(p.upload_file('test_upload.g'))
