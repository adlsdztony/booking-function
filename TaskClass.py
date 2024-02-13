from db import users, log


class Task(dict):    
    def getUser(self):
        user = users.find_one({'name': self['username']})
        return user

    def getRoom(self):
        return self['room'][-2]
    
    def makeBookUrl(self):
        facility = self['Facility']
        date = self['date'].replace('-', '')
        session = self['times'][0]
        ftype = self['FacilityType']
        lib = self['Library']
        url = f'https://booking.lib.hku.hk/Secure/NewBooking.aspx?library={lib}&ftype={ftype}&facility={facility}&date={date}&session={session}'
        return url
    
    def changeState(self, state):
        condition = {'_id': self['_id']}
        self['state'] = state
        log.update_one(condition, {'$set': self})

    def setUp(self):
        raise NotImplementedError
    
    def getSessions(self):
        raise NotImplementedError
    
    def getFacility(self):
        raise NotImplementedError


class DiscussionRoom(Task):
    def setUp(self):
        self['FacilityType'] = '21'
        self['Floor'] = '3'
        self['Library'] = '3'
        self['Facility'] = self.getFacility()

    def getSessions(self):
        for t in self['times']:
            t = t[:4]
            if t[2] == '3':
                t = int(t) - 830
                yield int(t / 100)
            elif t[2] == '0':
                t = int(t) - 900
                yield int(t / 100)

    def getFacility(self):
        return str(int(self['room'][-1].split(' ')[-1]) + 125)
    

class SingleStudyRoom(Task):
    def setUp(self):
        self['FacilityType'] = '31'
        self['Floor'] = '4'
        self['Library'] = '3'
        self['Facility'] = self.getFacility()

    def getSessions(self):
        for t in self['times']:
            if t == '08301300':
                yield 0
            elif t == '13001800':
                yield 1
            elif t == '18002200':
                yield 2

    def getFacility(self):
        return str(int(self['room'][-1].split(' ')[-1]) - 24)



class StudyRoom(Task):
    def setUp(self):
        self['FacilityType'] = '29'
        self['Floor'] = '10'
        self['Library'] = '5'
        self['Facility'] = self.getFacility()

    def getSessions(self):
        for t in self['times']:
            s = int(t[:2])*2 + int(t[2] == '3')
            yield s - 4 if s >= 16 else s

    def getFacility(self):
        return str(int(self['room'][-1].split(' ')[-1]) + 256)

    

DIC = {
    'Discussion Room': DiscussionRoom, 
    'Single Study Room (3 sessions)': SingleStudyRoom,
    'Study Room': StudyRoom
    }


def createTask(task):
    if task['room'][-2] in DIC.keys():
        t = DIC[task['room'][-2]](task)
        t.setUp()
        return t
    else:
        raise NotImplementedError
    

if __name__ == "__main__":
    task = log.find_one({'date': '2023-02-28'})
    task = createTask(task)
    print(task.makeBookUrl())
    print(list(task.getSessions()))
    print(task.getFacility())