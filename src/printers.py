import requests

from jobs import Job


class Printer():
    """
    A generic interface to a printer.
    Handels the API calls to octoprint.
    """


    def __init__(self, name, hostname, api_key, location, printer_type, material_type, material_colour):
        self.name               = name
        self.url                = 'http://' + hostname
        self.headers            = {'X-Api-Key': api_key}
        self.location           = location
        self.printer_type       = printer_type
        self.material_type      = material_type
        self.material_colour    = material_colour
        self.currently_printing = None

    def api_get(self, endpoint):
        r = requests.get(self.url + endpoint, headers=self.headers)
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
            return {"state": {
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
    def simple_status(self):
        full_stat = self.status()
        return full_stat['state']['text']

    def can_make(self, job: Job):
        # TODO: Check that this works with a functional printer

        # Check the material and colour are correct
        if (self.material_type != job.material or self.material_colour != job.colour):
            return False

        # Get the printer status
        stat = self.status()

        if (stat['state']['text'] == 'Offline'):
            return False

        if (stat['state']['flags']['printing'] == True):
            return False

        if (stat['state']['flags']['ready'] == False):
            return False

        return True

    def local_files(self):
        # TODO: this  is not safe if the printer is offline
        return self.api_get('/api/files/local')

        # {'files': []}

    def upload_file(self, filename):
        files = {'file': open(filename, 'rb')}
        requests.post(self.url + '/api/files/local', headers=self.headers, files=files)

    def make(self, job: Job):
        """
        Sends the required files and settings to the printer
        """

        self.upload_file(job.filename)
        requests.post(self.url+'/api/files/local/'+job.filename.split('/')[-1], headers=self.headers, json={"command": "select", "print":"true"})
        self.currently_printing = job

    def cancel(self):
        requests.post(self.url+'/api/job', headers=self.headers, json={"command": "cancel"})
