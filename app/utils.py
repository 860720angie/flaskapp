# Helper functions to read and write tasks. 
import json

def read_tasks():
    with open('tasks.json', 'r') as file:
        return json.load(file)

def write_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)
