from apps.commons.unitests import SerializedApiRequestUnitest, BaseObtainAuthToken
from .views import CreateTodo, GetTodo, ListTodo, UpdateTodo, DeleteTodo
from apps.accounts.tests import AuthWithCorrectCredentialsTest


class CreateTodoTest(SerializedApiRequestUnitest, BaseObtainAuthToken, CreateTodo):
    depedency_testcases = [
        AuthWithCorrectCredentialsTest,
    ]

    payload = {
        "task": "set goals",
    }
    expected_response = {
        "id": None,
        "task": "set goals",
        "created_at": None,
        "last_updated_at": None,
    }
    rule = {
        "id": {"ignore": True},
        "created_at": {"ignore": True},
        "last_updated_at": {"ignore": True},
    }


class ListTodoTest(SerializedApiRequestUnitest, BaseObtainAuthToken, ListTodo):
    depedency_testcases = [AuthWithCorrectCredentialsTest, CreateTodoTest]
    payload = {}
    expected_response = {
        "count": None,
        "current": None,
        "next": None,
        "results": [
            {
                "id": None,
                "task": "set goals",
                "created_at": None,
                "last_updated_at": None,
            }
        ],
    }
    rule = {
        "count": {"ignore": True},
        "current": {"ignore": True},
        "next": {"ignore": True},
        "results": [
            {
                "id": {"ignore": True},
                "created_at": {"ignore": True},
                "last_updated_at": {"ignore": True},
            }
        ],
    }


class GetTodoTest(SerializedApiRequestUnitest, BaseObtainAuthToken, GetTodo):
    def __init__(self, *args, **kwargs):
        self.dependency_testcases_actions = {}
        super(GetTodoTest, self).__init__(*args, **kwargs)
        self.dependency_testcases_actions[
            "CreateTodoTest"
        ] = self.set_todo_id_into_url_args

    def set_todo_id_into_url_args(self, response):
        id = response.get("id")
        self.url_args = [
            id,
        ]

    depedency_testcases = [AuthWithCorrectCredentialsTest, CreateTodoTest]
    payload = {}
    expected_response = {
        "id": None,
        "task": "set goals",
        "created_at": None,
        "last_updated_at": None,
    }
    rule = {
        "id": {"ignore": True},
        "created_at": {"ignore": True},
        "last_updated_at": {"ignore": True},
    }


class UpdateTodoTest(SerializedApiRequestUnitest, BaseObtainAuthToken, UpdateTodo):
    def __init__(self, *args, **kwargs):
        self.dependency_testcases_actions = {}
        super(UpdateTodoTest, self).__init__(*args, **kwargs)
        self.dependency_testcases_actions[
            "CreateTodoTest"
        ] = self.set_todo_id_into_url_args

    def set_todo_id_into_url_args(self, response):
        id = response.get("id")
        self.url_args = [
            id,
        ]

    depedency_testcases = [AuthWithCorrectCredentialsTest, CreateTodoTest]
    payload = {"task": "hendrik task"}
    expected_response = {
        "id": None,
        "task": "hendrik task",
        "created_at": None,
        "last_updated_at": None,
    }
    rule = {
        "id": {"ignore": True},
        "created_at": {"ignore": True},
        "last_updated_at": {"ignore": True},
    }


class DeleteTodoTest(SerializedApiRequestUnitest, BaseObtainAuthToken, DeleteTodo):
    def __init__(self, *args, **kwargs):
        self.dependency_testcases_actions = {}
        super(DeleteTodoTest, self).__init__(*args, **kwargs)
        self.dependency_testcases_actions[
            "CreateTodoTest"
        ] = self.set_todo_id_into_url_args

    def set_todo_id_into_url_args(self, response):
        id = response.get("id")
        self.url_args = [
            id,
        ]

    depedency_testcases = [AuthWithCorrectCredentialsTest, CreateTodoTest]
    no_response_body = True

    payload = {}
    expected_response = {}
    rule = {}
