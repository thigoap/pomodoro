from browser import document, bind, html, confirm
from browser.local_storage import storage
import time
import json


@bind(document['newTaskBtn'], 'click')
def show_modal(e):
    document['modalAddTasksContainer'].classList.remove('hidden')
    document['task'].focus()

@bind(document['delTasksBtn'], 'click')
def del_all(e):
    if len(storage) > 0:
        document['modalDellAllTasksContainer'].classList.remove('hidden')

# tasks list buttons
def doneBtn(e):
    taskHTML = document[e.target.id[5:]]
    child = taskHTML.children[0].children[0]
    taskID = taskHTML.id
    taskObj = json.loads(storage[taskID])
    del document[e.target.id]
    if not taskObj['done']:
        child <= html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer min-w-min', src='./static/assets/img/tick-done.png')
        taskObj['done'] = True
        storage[taskID] = json.dumps(taskObj, ensure_ascii=False)
    else:
        child <= html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer min-w-min', src='./static/assets/img/tick.png')        
        taskObj['done'] = False
        storage[taskID] = json.dumps(taskObj, ensure_ascii=False)
    document[f'done_{taskID}'].bind('click', doneBtn)

def editBtn(e):
    global editTaskID
    task = document[e.target.id[5:]]
    document['modalEditTasksContainer'].classList.remove('hidden')
    document['taskToEdit'].focus()
    document['taskToEdit'].value = task.text
    editTaskID = task.id

def delBtn(e):
    del document[e.target.id[4:]]
    del storage[e.target.id[4:]]
    if len(storage) == 0:
        document['delTasksBtn'].disabled = True

# modal buttons
@bind(document['addBtn'], 'click')
def add_task(e):
    task = document['task'].value
    timestamp = time.time()
    if len(storage) == 0:
        document['delTasksBtn'].disabled = False
    if task.strip():
        mainDiv = divGenerator(timestamp, task)
        storage[str(timestamp)] = json.dumps({'id': timestamp, 'task': task, 'done': False}, ensure_ascii=False)
        document['tasksList'] <= mainDiv
        document['modalAddTasksContainer'].classList.add('hidden')
        document['task'].value = ''
        document[f'edit_{timestamp}'].bind('click', editBtn)
        document[f'del_{timestamp}'].bind('click', delBtn)
        document[f'done_{timestamp}'].bind('click', doneBtn)

@bind(document['task'], 'keypress')
def add_with_enter(e):
    if e.keyCode == 13:
        add_task(e)

@bind(document['editBtn'], 'click')
def edit_task(e):
    taskHTML = document[editTaskID]
    child = taskHTML.children[0].children[1]
    taskID = taskHTML.id
    taskObj = json.loads(storage[taskID])
    newTask = document['taskToEdit'].value
    if newTask.strip():
        child.clear()
        child <= (f'{newTask}')
        taskObj['task'] = newTask
        storage[taskID] = json.dumps(taskObj, ensure_ascii=False)
        document['modalEditTasksContainer'].classList.add('hidden')

@bind(document['taskToEdit'], 'keypress')
def edit_with_enter(e):
    if e.keyCode == 13:
        edit_task(e)

@bind(document['dellAllTasksBtn'], 'click')
def dell_all_tasks(e):
    for task in storage:
        del storage[task]
        del document[task]
        document['modalDellAllTasksContainer'].classList.add('hidden')
        document['delTasksBtn'].disabled = True

@bind(document['closeAddTasksBtn'], 'click')
def hide_modal(e):
    document['task'].value = ''
    document['modalAddTasksContainer'].classList.add('hidden')

@bind(document['closeEditTasksBtn'], 'click')
def hide_modal(e):
    document['modalEditTasksContainer'].classList.add('hidden')

@bind(document['closeDellAllTasksBtn'], 'click')
def hide_modal(e):
    document['modalDellAllTasksContainer'].classList.add('hidden')


def divGenerator(taskID, task, done = False):
    mainDiv = html.DIV(Class='flex justify-between py-1', id=taskID)
    div1 = html.DIV(Class='flex items-center')
    if done:
        htmlInput = html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer min-w-min', src='./static/assets/img/tick-done.png')
    else:
        htmlInput = html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer min-w-min', src='./static/assets/img/tick.png')       
    inputP = html.P(Class='flex items-center')
    inputP <= htmlInput
    taskP = html.P(Class='ml-2 text-lg')
    taskP <= (f'{task}')
    div1 <= (inputP + taskP)
    div2 = html.DIV(Class='flex items-center')
    inputP = html.P(Class='flex items-center')
    htmlInput1 = html.IMG(id=f'edit_{taskID}', Class='h-6 cursor-pointer', src='./static/assets/img/edit.png') 
    htmlInput2 = html.IMG(id=f'del_{taskID}', Class='h-6 ml-2 cursor-pointer', src='./static/assets/img/delete.png')
    inputP <= (htmlInput1 + htmlInput2)   
    div2 <= (inputP)
    mainDiv <= (div1 + div2)
    return mainDiv

# runs on load: populate tasks stored in storage
if len(storage) > 0:
    for taskID in storage:
        taskObj = json.loads(storage[taskID])
        taskItself = taskObj['task']
        taskDone = taskObj['done']
        taskDiv = divGenerator(taskID, taskItself, taskDone)
        document['tasksList'] <= taskDiv
        document[f'edit_{taskID}'].bind('click', editBtn)
        document[f'del_{taskID}'].bind('click', delBtn)
        document[f'done_{taskID}'].bind('click', doneBtn)  
        document['delTasksBtn'].disabled = False
  