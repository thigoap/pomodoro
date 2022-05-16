from browser import document, timer, bind

_timer = None
x_time = 0 # 0 = break time / 1 = working time
status = 0 # 0 = initial or finished a cycle / 1 = running
session = 1
auto = 0

@bind(document['stBtn'], 'click')
def pomodoro_stst(e):
    global status, sessions, _timer
    if document['stBtn'].value == 'RUNNING': # stop pomodoro    
        btn_to_start()
        timer.clear_interval(_timer)
    else: # start pomodoro
        set_current_time(status)
        status = 1 # running
        btn_to_stop()
        disable_btns()
        document['rstBtn'].disabled = True
        sessions = document['sessions'].text
        _timer = timer.set_interval(update_clock, 100)

@bind(document['rstBtn'], 'click')
def pomodoro_reset(e):
    global x_time, status, session
    document['work'].text = '%02i'%25
    document['pause'].text = '%02i'%5
    document['sessions'].text = '%02i'%5
    document['mins'].text = document['work'].text
    document['secs'].text = '%02i'%0
    btn_to_start()
    enable_btns()
    document['rstBtn'].disabled = True
    document['stBtn'].text = 'start'
    document['stBtn'].value = 'INITIAL'
    document['x_session'].text = ''
    document['status'].text = ''
    x_time = 0
    status = 0
    session = 1
    timer.clear_interval(_timer)

@bind(document['toggleBtn'], 'click')
def auto_on_off(e):
    global auto
    auto = 0 if auto == 1 else 1

def update_clock():
    global mins, secs, status, session, sessions, x_time, auto
    if int(mins) == 0 and int(secs) == 0: 
        if session == int(sessions) and x_time == 0: # finished everything
            pomodoro_reset(status)
            document['status'].text = 'Pomodoro finished'
        else: # finished a cycle
            timer.clear_interval(_timer)
            document['stBtn'].value = 'STOPPED'
            status = 0
            if x_time == 1: # finished a working cycle
                document['mins'].text = document['pause'].text
                document['status'].text = 'break time '
            else: # finished a break cycle
                document['mins'].text = document['work'].text
                document['status'].text = 'work time '
                session += 1
                document['x_session'].text = '#'+str(session)
            if auto == 1:
                pomodoro_stst(status)
            else:
                btn_to_start()
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
            document['status'].text = 'break time '
        else: # finished a break cycle
            mins = document['work'].text 
            x_time = 1   
            document['status'].text = 'work time '    
    else: # running
        mins = document['mins'].text
    secs = document['secs'].text
    document['x_session'].text = '#'+str(session)

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
        if int(document['sessions'].text) < 20:
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

@bind(document['btn15'], 'click')
@bind(document['btn30'], 'click')
@bind(document['btn45'], 'click')
def set_new_param(e):
    if e.target.id == 'btn15':
        document['work'].text = 15
        document['mins'].text = 15
    elif e.target.id == 'btn30':
        document['work'].text = 30
        document['mins'].text = 30
    elif e.target.id == 'btn45':
        document['work'].text = 45
        document['mins'].text = 45

@bind(document['btn3'], 'click')
@bind(document['btn5'], 'click')
@bind(document['btn10'], 'click')
@bind(document['btns3'], 'click')
@bind(document['btns5'], 'click')
@bind(document['btns10'], 'click')
def set_new_param(e):
    if e.target.id == 'btn3':
        document['pause'].text = '%02i'%3
    elif e.target.id == 'btn5':
        document['pause'].text = '%02i'%5
    elif e.target.id == 'btn10':
        document['pause'].text = 10
    elif e.target.id == 'btns3':
        document['sessions'].text = '%02i'%3
    elif e.target.id == 'btns5':
        document['sessions'].text = '%02i'%5
    elif e.target.id == 'btns10':
        document['sessions'].text = 10

@bind(document['setBtn'], 'click')
def show_modal(e):
    document['modal-container'].classList.remove('hidden')

@bind(document['closeBtn'], 'click')
def hide_modal(e):
    document['modal-container'].classList.add('hidden')


def btn_to_stop():
    document['stBtn'].text = 'stop'
    document['stBtn'].value = 'RUNNING'
    document['stBtn'].classList.add('bg-red-500')
    document['stBtn'].classList.add('hover:bg-red-400')
    document['stBtn'].classList.remove('bg-green-600')
    document['stBtn'].classList.remove('hover:bg-green-500') 

def btn_to_start():
    document['stBtn'].text = 'continue'
    document['stBtn'].value = 'STOPPED'
    document['stBtn'].classList.add('bg-green-600')
    document['stBtn'].classList.add('hover:bg-green-500')
    document['stBtn'].classList.remove('bg-red-500')
    document['stBtn'].classList.remove('hover:bg-red-400')  
    document['rstBtn'].disabled = False

def disable_btns():
    document['workup'].disabled = True
    document['workdown'].disabled = True
    document['breakup'].disabled = True
    document['breakdown'].disabled = True
    document['sessionup'].disabled = True
    document['sessiondown'].disabled = True
    document['btn15'].disabled = True
    document['btn30'].disabled = True
    document['btn45'].disabled = True
    document['btn3'].disabled = True
    document['btn5'].disabled = True
    document['btn10'].disabled = True
    document['btns3'].disabled = True
    document['btns5'].disabled = True
    document['btns10'].disabled = True
    document['toggleBtn'].disabled = True
    document['btn15'].classList.remove('cursor-pointer')
    document['btn30'].classList.remove('cursor-pointer')
    document['btn45'].classList.remove('cursor-pointer')
    document['btn3'].classList.remove('cursor-pointer')
    document['btn5'].classList.remove('cursor-pointer')
    document['btn10'].classList.remove('cursor-pointer')
    document['btns3'].classList.remove('cursor-pointer')
    document['btns5'].classList.remove('cursor-pointer')
    document['btns10'].classList.remove('cursor-pointer')
    document['toggleBtnCursor'].classList.remove('cursor-pointer') 
    document['msg'].classList.remove('hidden')
    document['modal'].classList.remove('h-52')
    document['modal'].classList.add('h-56')


def enable_btns():
    document['workup'].disabled = False
    document['workdown'].disabled = False
    document['breakup'].disabled = False
    document['breakdown'].disabled = False
    document['sessionup'].disabled = False
    document['sessiondown'].disabled = False
    document['btn15'].disabled = False
    document['btn30'].disabled = False
    document['btn45'].disabled = False
    document['btn3'].disabled = False
    document['btn5'].disabled = False
    document['btn10'].disabled = False
    document['btns3'].disabled = False
    document['btns5'].disabled = False
    document['btns10'].disabled = False
    document['toggleBtn'].disabled = False
    document['btn15'].classList.add('cursor-pointer')
    document['btn30'].classList.add('cursor-pointer')
    document['btn45'].classList.add('cursor-pointer')
    document['btn3'].classList.add('cursor-pointer')
    document['btn5'].classList.add('cursor-pointer')
    document['btn10'].classList.add('cursor-pointer')
    document['btns3'].classList.add('cursor-pointer')
    document['btns5'].classList.add('cursor-pointer')
    document['btns10'].classList.add('cursor-pointer')
    document['toggleBtnCursor'].classList.add('cursor-pointer')
    document['msg'].classList.add('hidden')
    document['modal'].classList.add('h-52')
    document['modal'].classList.remove('h-56')