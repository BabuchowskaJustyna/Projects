import json
from enum import Enum
from datetime import date


class Priority(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class Status(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'


class Task:
    """
    Represents a task in the task list.

    >>> task = Task("Buy groceries", priority=Priority.HIGH, deadline="2025-01-20")
    >>> task.title
    'Buy groceries'
    >>> task.priority.name
    'HIGH'
    >>> task.status.name
    'PENDING'
    >>> task.to_dict()
    {'task_id': 0, 'title': 'Buy groceries', 'description': '', 'priority': 'High', 'status': 'Pending', 'deadline': '2025-01-20'}
    >>> print(task)
    Buy groceries - Priority: High, Status: Pending
    >>> task2 = Task("Read book", priority=Priority.LOW)
    >>> task2.to_dict()
    {'task_id': 1, 'title': 'Read book', 'description': '', 'priority': 'Low', 'status': 'Pending', 'deadline': None}
    >>> Task.id_counter = 0
    """
    id_counter: int = 0

    def __init__(self, title, task_id=None, description: str | None = None, priority: Priority = Priority.LOW,
                 status: Status = Status.PENDING, deadline=None):
        self.title = title
        self.description = description or ''
        self.priority = priority
        self.status = status
        self.deadline = deadline
        self.task_id = task_id

        if task_id is None:
            number = self.id_number()
            self.set_id(number)

    @classmethod
    def id_number(cls) -> int:
        """
        Liczy id dla wszystkich task (licznik współdzielony między wszystkimi instancjami)
        """
        id_number = cls.id_counter
        cls.id_counter += 1
        return id_number

    @classmethod
    def update_counter(cls, new_id):
        """
        Update counter after load_from_file with old ids
        """
        cls.id_counter = new_id

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        if value is None:
            self._deadline = None
        else:
            try:
                parsed_date = date.fromisoformat(value)
                self._deadline = str(parsed_date)
            except ValueError:
                raise ValueError('Incorrect date format YYYY-MM-DD')

    def set_id(self, number):
        self.task_id = number

    def to_dict(self):
        return {'task_id': self.task_id, 'title': self.title, 'description': self.description,
                'priority': self.priority.value, 'status': self.status.value, 'deadline': self.deadline}

    def __str__(self):
        return f'{self.title} - Priority: {self.priority.value}, Status: {self.status.value}'


class TaskList:
    """
    Manages a list of tasks.

    >>> task_list = TaskList()
    >>> len(task_list._tasks)
    0
    >>> task_list.add_task("assignment #1", priority=Priority.HIGH)
    >>> task_list.add_task("assignment #2", priority=Priority.LOW, deadline="2025-01-20")
    >>> task_list.add_task("assignment #3", priority=Priority.MEDIUM, deadline="2025-01-20")
    >>> len(task_list._tasks)
    3
    >>> task_list.remove_task(999)
    Traceback (most recent call last):
    ...
    ValueError: Task ID does not exist.
    >>> task_list.remove_task(0)
    >>> len(task_list._tasks)
    2
    >>> task_list.update_task(1, status=Status.COMPLETED)
    >>> task_list.update_task(2, status=Status.IN_PROGRESS)
    >>> print(task_list.list_tasks())
    - assignment #2 - Priority: Low, Status: Completed
    - assignment #3 - Priority: Medium, Status: In Progress
    >>> print(task_list.list_tasks(status=Status.IN_PROGRESS))
    - assignment #3 - Priority: Medium, Status: In Progress
    >>> task_list.save_to_file('tasks.json')
    >>> task_list = TaskList()
    >>> task_list.load_from_file("tasks.json")
    >>> len(task_list._tasks) > 0
    True
    >>> print(task_list.list_tasks())
    - assignment #2 - Priority: Low, Status: Completed
    - assignment #3 - Priority: Medium, Status: In Progress
    >>> task_list = TaskList()
    >>> task_list.add_task("Complete assignment", priority=Priority.HIGH)
    >>> task_list.add_task("Buy groceries", priority=Priority.LOW)
    >>> task_list.add_task("Read book", priority=Priority.MEDIUM)
    >>> print(task_list.list_tasks())
    - Complete assignment - Priority: High, Status: Pending
    - Buy groceries - Priority: Low, Status: Pending
    - Read book - Priority: Medium, Status: Pending
    >>> task_list.update_task(4, status=Status.IN_PROGRESS)
    >>> task_list.update_task(5, status=Status.COMPLETED)
    >>> print(task_list)
    Task List:
    - Complete assignment - Priority: High, Status: Pending
    - Buy groceries - Priority: Low, Status: In Progress
    - Read book - Priority: Medium, Status: Completed
    """

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, title: str, task_id: int | None = None, description: str | None = None,
                 priority: Priority = Priority.LOW,
                 status: Status = Status.PENDING, deadline: str | None = None) -> None:
        task = Task(title, task_id, description, priority, status, deadline)
        self._tasks.append(task)

    def _find_task(self, id_number: int) -> Task:
        try:
            task_to_find = list(filter(lambda task: task.task_id == id_number, self._tasks))[0]
            return task_to_find
        except IndexError:
            raise ValueError('Task ID does not exist.')

    def remove_task(self, id_number: int) -> None:
        task_to_remove = self._find_task(id_number)
        if task_to_remove:
            self._tasks.remove(task_to_remove)

    def update_task(self, id_number: int, status: Status | None = None, priority: Priority | None = None):
        task_to_update: Task = self._find_task(id_number)
        if status:
            task_to_update.status = status
        elif priority:
            task_to_update.priority = priority
        else:
            raise ValueError('You must provide status or priority to make an update')

    def list_tasks(self, status: Status = None, sort: Priority | str | None = None) -> str:
        """
        filter by status, sort by (priority or deadline)
        """
        if status:
            tasks = list(filter(lambda obj: obj.status == status, self._tasks))
        elif isinstance(sort, Priority):
            tasks = sorted(self._tasks, key=lambda obj: obj.priority == sort)
        elif sort:
            tasks = sorted(self._tasks, key=lambda obj: obj.deadline == sort)
        else:
            tasks = self._tasks
        tasks_view = '\n'.join([f'- {str(task)}' for task in tasks])
        return tasks_view

    def save_to_file(self, file_name: str) -> None:
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self._tasks],
                      file,
                      indent=4)

    def load_from_file(self, file_name: str) -> None:
        self._tasks = []
        try:
            with open(file_name, 'r') as file:
                content = json.load(file)
            for obj in content:
                obj['priority'] = Priority(obj['priority'])
                obj['status'] = Status(obj['status'])
                self.add_task(**obj)
            Task.update_counter(max(task.task_id for task in self._tasks) + 1)
        except (FileNotFoundError, json.JSONDecodeError):
            Task.update_counter(0)

    def __str__(self) -> str:
        title = 'Task List:\n'
        tasks_all = self.list_tasks()
        return f'{title}{tasks_all}'
