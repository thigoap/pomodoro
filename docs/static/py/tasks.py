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
    else:
       print('storage vazio')

# tasks list buttons
def doneBtn(e):
    taskHTML = document[e.target.id[5:]]
    child = taskHTML.children[0].children[0]
    taskID = taskHTML.id 
    done = json.loads(storage[taskID])['done']
    del document[e.target.id]
    if not done:
        child <= html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer', src='./static/assets/tick-done.png')
        storage[taskID] = storage[taskID].replace('false', 'true').replace('tick', 'tick-done')
    else:
        child <= html.IMG(id=f'done_{taskID}', Class='h-6 cursor-pointer', src='./static/assets/tick.png')        
        storage[taskID] = storage[taskID].replace('true', 'false').replace('tick-done', 'tick')
    document[f'done_{taskID}'].bind('click', doneBtn)

def editBtn(e):
    global oldTask, editTaskID
    oldTask = document[e.target.id[5:]]
    document['modalEditTasksContainer'].classList.remove('hidden')
    document['taskToEdit'].focus()
    document['taskToEdit'].value = oldTask.text
    editTaskID = oldTask.id

def delBtn(e):
    del document[e.target.id[4:]]
    del storage[e.target.id[4:]]

# modal buttons
@bind(document['addBtn'], 'click')
def add_task(e):
    task = document['task'].value.replace('<', '')
    timestamp = time.time()
    if task.strip():
        mainDiv = html.DIV(Class='flex justify-between py-1', id=timestamp)
        div1 = html.DIV(Class='flex items-center')
        inputP = html.P(Class='flex items-center')
        htmlInput = html.IMG(id=f'done_{timestamp}', Class='h-6 cursor-pointer', src='./static/assets/tick.png')
        inputP <= htmlInput
        taskP = html.P(task, Class='ml-2 text-lg')
        div1 <= (inputP + taskP)
        div2 = html.DIV(Class='flex items-center')
        inputP = html.P(Class='flex items-center')
        htmlInput1 = html.IMG(id=f'edit_{timestamp}', Class='h-6 cursor-pointer', src='./static/assets/edit.png') 
        htmlInput2 = html.IMG(id=f'del_{timestamp}', Class='h-6 ml-2 cursor-pointer', src='./static/assets/delete.png')
        inputP <= (htmlInput1 + htmlInput2)   
        div2 <= (inputP)
        mainDiv <= (div1 + div2)
        # storage[str(timestamp)] = json.dumps({'idf': timestamp, 'task': task, 'div': mainDiv.innerHTML, 'done': False}, ensure_ascii=False)
        storage[str(timestamp)] = json.dumps({'idf': timestamp, 'div': mainDiv.innerHTML, 'done': False}, ensure_ascii=False)
        document['tasksList'] <= mainDiv
        document['modalAddTasksContainer'].classList.add('hidden')
        document['task'].value = ''
        document[f'edit_{timestamp}'].bind('click', editBtn)
        document[f'del_{timestamp}'].bind('click', delBtn)
        document[f'done_{timestamp}'].bind('click', doneBtn)

@bind(document['editBtn'], 'click')
def edit_task(e):
    newTask = document['taskToEdit'].value.replace('<', '')
    if newTask.strip():
        old = '<p class=\\"ml-2 text-lg\\">'+ oldTask.text
        new = '<p class=\\"ml-2 text-lg\\">'+ newTask
        storage[editTaskID] = storage[editTaskID].replace(old, new)
        # storage[editTaskID] = storage[editTaskID].replace(oldTask.text, newTask)
        print(storage[editTaskID])
        document[editTaskID].children[0].children[1].text = newTask
        document['modalEditTasksContainer'].classList.add('hidden')

@bind(document['dellAllTasksBtn'], 'click')
def dell_all_tasks(e):
    for task in storage:
        del storage[task]
        del document[task]
        document['modalDellAllTasksContainer'].classList.add('hidden')

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


# runs on load: populate tasks stored in storage
for taskID in storage:
    taskDiv = json.loads(storage[taskID])['div'].replace('\\','')
    document['tasksList'] <= html.DIV(taskDiv, Class='flex justify-between py-1', id=taskID)
    document[f'edit_{taskID}'].bind('click', editBtn)
    document[f'del_{taskID}'].bind('click', delBtn)
    document[f'done_{taskID}'].bind('click', doneBtn)
    print(storage[taskID])


# for item in storage:
#     # print(storage[item])
#     del item
