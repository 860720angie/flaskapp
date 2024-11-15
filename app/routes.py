from flask import jsonify, request, render_template, redirect, url_for
from app import app
from .utils import read_tasks, write_tasks

AUTH_TOKEN = "123"

@app.route('/')
def home():
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = read_tasks()
    title = request.form.get('title')
    category = request.form.get('category')

    # Validate that title and category contain only letters
    if not title or not category:
        return render_template('index.html', tasks=tasks, error="Both title and category are required.")
    if not title.isalpha() or not category.isalpha():
        return render_template('index.html', tasks=tasks, error="Error: Only letters are allowed for title and category.")

    new_task = {
        'id': max([task['id'] for task in tasks], default=0) + 1,
        'title': title,
        'status': 'pending',
        'category': category
    }
    tasks.append(new_task)
    write_tasks(tasks)
    return redirect(url_for('home'))

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['status'] = 'completed'
        write_tasks(tasks)
        return redirect(url_for('home'))
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['POST'])
def handle_task(task_id):
    method = request.form.get('_method')
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)

    if method == 'DELETE':
        token = request.form.get('token')
        if token != AUTH_TOKEN:
            return render_template('index.html', tasks=tasks, error="Invalid token."), 403
        if task:
            tasks.remove(task)
            write_tasks(tasks)
            return redirect(url_for('home'))
    elif method == 'PUT':
        updated_title = request.form.get('title')
        updated_category = request.form.get('category')
        updated_status = request.form.get('status', 'pending')

        if task:
            task['title'] = updated_title or task['title']
            task['category'] = updated_category or task['category']
            task['status'] = updated_status
            write_tasks(tasks)
            return redirect(url_for('home'))

    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/categories', methods=['GET'])
def get_categories():
    tasks = read_tasks()
    categories = list(set(task.get('category') for task in tasks if 'category' in task))
    return jsonify(categories), 200

@app.route('/tasks/categories/<category_name>', methods=['GET'])
def get_tasks_by_category(category_name):
    tasks = read_tasks()
    filtered_tasks = [task for task in tasks if task.get('category') == category_name]
    return jsonify(filtered_tasks), 200

@app.route('/search_task', methods=['GET'])
def search_task():
    task_id = request.args.get('task_id', type=int)
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task:
        return render_template('index.html', tasks=tasks, task=task)
    return render_template('index.html', tasks=tasks, error="Task not found.")
