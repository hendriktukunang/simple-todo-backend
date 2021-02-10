from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.authtoken.views import ObtainAuthToken


class BaseUnitest(TestCase):
    """
    a base unitest is parent of all unitest classes, currently we only have API request unitest,
    but in future we will have socket connection, so we also will inherti this class to socket unitest
    """

    depedency_testcases = []
    executor_class = None
    execute_dependency_testcases = True
    instance = None
    no_response_body = False
    no_url_args = False

    def __init__(self, *args, **kwargs):
        self.executor_class = kwargs.get("executor_class", None)
        TestCase.__init__(self, methodName="test_api")

    def run_depedencies_testcases(self):
        has_dependency_test_cases_action = getattr(
            self, "dependency_testcases_actions", None
        )
        for test_cls in self.depedency_testcases:
            test_obj = test_cls(executor_class=self, execute_dependency_testcases=False)
            depencency_response = test_obj.manually_execute()

            if has_dependency_test_cases_action:
                cls_name = str(test_cls.__name__)
                if cls_name in self.dependency_testcases_actions:
                    self.dependency_testcases_actions[cls_name](
                        response=depencency_response
                    )

    def setUp(self):
        self.pre_run_test()
        if self.execute_dependency_testcases:
            self.run_depedencies_testcases()

    def tearDown(self):
        self.teardown_dependencies_test()

    def teardown_dependencies_test(self):
        if self.execute_dependency_testcases:
            for test_cls in self.depedency_testcases:
                test_obj = test_cls(executor_class=self)
                test_obj.tearDown()

    def manually_execute(self):
        return self.test_api()

    def test_api(self):
        return self.run_test()

    def testcase_callback(self, **kwargs):
        pass

    def resolve_url(self, *args, **kwargs):
        view_name = kwargs.get("view_name")
        return reverse(view_name, args=args)

    def assert_result(self, **kwargs):
        expected_result = kwargs.get("expected_result")
        actual_result = kwargs.get("actual_result")
        rule_kwargs = kwargs.get("rule_kwargs")
        if type(expected_result) is list:
            for (expected_data, actual_data, rule_data) in zip(
                expected_result, actual_result, rule_kwargs
            ):
                self.assert_result(
                    expected_result=expected_data,
                    actual_result=actual_data,
                    rule_kwargs=rule_data,
                )
        else:

            for key in expected_result:
                actual_value = actual_result.get(key)
                expected_value = expected_result.get(key)
                if type(expected_value) is list:
                    for (expected_data, actual_data, rule_data) in zip(
                        expected_value, actual_value, rule_kwargs.get(key, {})
                    ):
                        self.assert_result(
                            expected_result=expected_data,
                            actual_result=actual_data,
                            rule_kwargs=rule_data,
                        )
                elif type(expected_value) is not dict:
                    if (
                        key not in rule_kwargs
                        or "read_only" in rule_kwargs.get(key, {})
                    ) and key not in getattr(self, "ignore_fields", []):
                        self.assertEqual(actual_value, expected_value)
                else:
                    self.assert_result(
                        expected_result=expected_value,
                        actual_result=actual_value,
                        rule_kwargs=rule_kwargs.get(key, {}),
                    )

    def get_testcase_rule(self):
        testcase_rule = getattr(self, "rule", None)
        if testcase_rule is None:
            raise Exception("rule is not defined ")
        return testcase_rule

    def get_testcase_payload(self):
        testcase_payload = getattr(self, "payload", None)
        if testcase_payload is None:
            raise Exception("payload is not defined ")
        return testcase_payload

    def get_testcase_expected_response(self):
        testcase_expected_response = getattr(self, "expected_response", None)
        if testcase_expected_response is None:
            raise Exception("expected_response is not defined ")
        return testcase_expected_response


class ApiRequestUnitest(BaseUnitest):
    """
    AApiRequestUnitest is base class for rest api unitest, we will exntends this class to serialized api,
    or Non serialized api wher it's not return any content on response like on delete method
    """

    method = None
    url_args = []

    def __init__(self, *args, **kwargs):
        super(ApiRequestUnitest, self).__init__(*args, **kwargs)
        self.get_method()

    def get_authorization(self):
        if AllowAny not in self.permission_classes:
            if self.executor_class is not None:
                _token = self.executor_class.token
            else:
                _token = self.token
            return {"HTTP_AUTHORIZATION": "Token " + _token}
        return {}

    def create_api_view_callback(self, **kwargs):
        if self.executor_class:
            self.executor_class.instance = kwargs.get("response")

    def auth_api_view_callback(self, **kwargs):
        response = kwargs.get("response")
        if self.executor_class:
            self.executor_class.token = response.get("token")

    def __get_request_func(self, method):
        if method.lower() == "post":
            return self.client.post
        elif method.lower() == "get":
            return self.client.get
        elif method.lower() == "put":
            return self.client.put
        elif method.lower() == "patch":
            return self.client.patch
        elif method.lower() == "delete":
            return self.client.delete

    def make_request(self, method, url, payload, **authorization):
        self.client = APIClient()
        if authorization:
            self.client.credentials(**authorization)
        response = self.__get_request_func(method)(url, payload, format="json")
        rule_kwargs = self.get_testcase_rule()

        if method != "delete" and not self.no_response_body:
            response = response.json()
        if not self.no_response_body:
            self.assert_result(
                expected_result=self.get_testcase_expected_response(),
                actual_result=response,
                rule_kwargs=rule_kwargs,
            )

        self.testcase_callback(response=response)

        return response

    def get_expected_result(self):
        raise Exception(
            "expected_result must be declared in " + str(type(self).__name__)
        )

    def pre_run_test(self):
        return self.executor_class

    def run_test(self):
        if issubclass(type(self), APIView):
            authorization = self.get_authorization()
            payload = self.get_testcase_payload()
            view_name = str(type(self).__name__)
            if not self.no_url_args:
                url_args = (
                    self.executor_class.url_args
                    if self.executor_class
                    else self.url_args
                )
            else:
                url_args = []
            self.url = self.resolve_url(*url_args, view_name=view_name)
            return self.make_request(self.method, self.url, payload, **authorization)

    def get_method(self):
        self.method = None

        overrided_method = getattr(self, "test_case_request_method", None)

        if overrided_method:
            self.method = overrided_method

        elif issubclass(type(self), ObtainAuthToken):
            self.method = "post"
            self.testcase_callback = self.auth_api_view_callback
        elif issubclass(type(self), CreateAPIView) or getattr(self, "post", None):
            self.method = "post"
            self.testcase_callback = self.create_api_view_callback
        elif issubclass(type(self), UpdateAPIView) or getattr(self, "patch", None):
            self.method = "patch"
        elif issubclass(type(self), DestroyAPIView) or getattr(self, "delete", None):
            self.method = "delete"
        elif (
            issubclass(type(self), ListAPIView)
            or issubclass(type(self), RetrieveAPIView)
            or getattr(self, "get", None)
        ):
            self.method = "get"
        elif getattr(self, "put", None):
            self.method = "put"

        return self.method


class SerializedApiRequestUnitest(ApiRequestUnitest):
    """
    serizlized means response is bound to a specific serializer, or return anything in json format,
    some api for delete operation won't have any response, that will be handled inside non serialized api request unitest
    """

    def __init__(self, *args, **kwargs):
        super(SerializedApiRequestUnitest, self).__init__(*args, **kwargs)

    def get_base_class_name(self):
        try:
            for cls in self.__class__.__bases__:
                if issubclass(cls, APIView):
                    return cls.__name__
            raise Exception(
                str(self.__class__.__name__) + " doesn't have any base class"
            )
        except:
            raise Exception(
                str(self.__class__.__name__) + " doesn't have any base class"
            )

    def resolve_url(self, *args, **kwargs):
        base_class_name = self.get_base_class_name()
        kwargs["view_name"] = base_class_name
        return super().resolve_url(*args, **kwargs)

    def run_test(self):
        if type(self) != SerializedApiRequestUnitest:
            return super(SerializedApiRequestUnitest, self).run_test()


class BaseObtainAuthToken:
    def __init__(self, *args, **kwargs):
        self.depedency_testcases_actions["AuthTest"] = self.obtain_token

    def obtain_token(self, response):
        if self.executor_class:
            self.executor_class.token = response.get("token")
        else:
            self.token = response.get("token")
