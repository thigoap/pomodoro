from browser import document, timer, bind

_timer = None
x_time = 0 # 0 = break time / 1 = working time
status = 0 # 0 = initial or finished a cycle / 1 = running
session = 0

@bind(document['stst'], 'click')
def pomodoro_stst(e):
    global state, status, sessions, _timer
    state = document['stst'].value
    if state == 'running': #stop pomodoro
        document['stst'].text = 'continue'
        document['stst'].value = 'stoped'
        document['stst'].classList.add('bg-green-600')
        document['stst'].classList.remove('bg-red-500')
        document['reset'].classList.remove('hidden')    
        timer.clear_interval(_timer)
    else: #start pomodoro
        set_current_time(status)
        status = 1 # running
        document['stst'].text = 'stop'
        document['stst'].value = 'running'
        document['stst'].classList.add('bg-red-500')
        document['stst'].classList.remove('bg-green-600')
        document['inputs'].classList.add('hidden')
        document['reset'].classList.add('hidden')
        sessions = document['sessions'].text
        _timer = timer.set_interval(update_clock, 1000)

@bind(document['reset'], 'click')
def pomodoro_reset(e):
    global x_time, status, session
    document['work'].text = '%02i'%5
    document['pause'].text = '%02i'%1
    document['sessions'].text = '%02i'%2
    document['mins'].text = document['work'].text
    document['secs'].text = '%02i'%0
    document['inputs'].classList.remove('hidden') 
    document['stst'].classList.remove('bg-red-500')
    document['stst'].classList.add('bg-green-600')
    document['stst'].text = 'start'
    document['stst'].value = 'initial'
    document['reset'].classList.add('hidden')
    document['x_session'].text = ''
    x_time = 0
    status = 0
    session = 0
    timer.clear_interval(_timer)

def update_clock():
    global state, mins, secs, status, session, sessions, x_time
    if int(mins) == 0 and int(secs) == 0:
        if x_time == 1: # finished a working cycle
            document['mins'].text = document['pause'].text
        else:
            document['mins'].text = document['work'].text
        if session == int(sessions) and x_time == 0:
            document['status'].text = 'Pomodoro finished'
            pomodoro_reset(state)
        else:
            timer.clear_interval(_timer)
            document['stst'].value = 'stoped'
            status = 0
            pomodoro_stst(state)
    else:
        secs = int(secs) - 1
        if int(mins) == 0 and int(secs) == 0:
            document['audio'].play()               
        if secs < 0:
            secs = 59
            mins = int(mins) - 1
            document['mins'].text = '%02i'%mins
        document['secs'].text = '%02i'%secs

def set_current_time(status):
    global mins, secs, x_time, session
    if status == 0: # intial or finished a cycle
        if x_time == 1: # finished a working cycle
            mins = document['pause'].text
            x_time = 0
            document['status'].text = 'break time'
        else: # finished a break cycle
            mins = document['work'].text 
            x_time = 1 
            session += 1   
            document['status'].text = 'work time'    
    else: # running
        mins = document['mins'].text
    secs = document['secs'].text
    document['x_session'].text = session

@bind(document['workup'], 'click')
@bind(document['breakup'], 'click')
@bind(document['sessionup'], 'click')
def up(e):
    if e.target.id == 'workup':
        if int(document['work'].text) < 60:
            new = int(document['work'].text) + 1
            document['work'].text = '%02i'%new
            document['mins'].text = '%02i'%new
    elif e.target.id == 'breakup':
        if int(document['pause'].text) < 60:
            new = int(document['pause'].text) + 1
            document['pause'].text = '%02i'%new
    else:
        if int(document['sessions'].text) <= 11:
            new = int(document['sessions'].text) + 1
            document['sessions'].text = '%02i'%new

@bind(document['workdown'], 'click')
@bind(document['breakdown'], 'click')
@bind(document['sessiondown'], 'click')
def down(e):
    if e.target.id == 'workdown':
        if int(document['work'].text) > 2:
            new = int(document['work'].text) - 1
            document['work'].text = '%02i'%new
            document['mins'].text = '%02i'%new
    elif e.target.id == 'breakdown':
        if int(document['pause'].text) > 1:
            new = int(document['pause'].text) - 1
            document['pause'].text = '%02i'%new
    else:
        if int(document['sessions'].text) > 1:
            new = int(document['sessions'].text) - 1
            document['sessions'].text = '%02i'%new