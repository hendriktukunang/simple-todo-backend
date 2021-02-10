hi welcome to backend side of simple todo app, 
this app built with django and django rest framwork as main backend, 
postgres on database side, 
redis and django channels on socket connection  and celery and rabbitmq on background task management 

you can login with django admin panel with superuser access here (http://api.simple-todo.blankontech.com/admin/)
username/email : hendrik@blankontech.com
password : 123456

Project Explanation points:
1. i'm using inheritance concept for most of the project structure to prevent any duplication on code.
2. for authentication i'm using builtin django token management,  and extends ObtainAuthToken for authentication view
3. on todo api side, i created some base classes that you can find inside commons/views.py, this base classes can be used on other requests as well by extend them.

App Feature:
it has simple read, create and delete todo operation, with socket sync, so you can try to login on 2 different tab/browser, 
once data changed on 1 side it will automatically sync to other browser via socket and task executed under celery

Unitest:
in current project i'm using builtin django unitest, i created a unitest library for api services by simplify the process, 
so developer only need to write payload, expected response from server and rule of assert process, please check on accounts/tests.py and todos/tests.py 

Pytest:
i added 2 pytest unitest on accounts app
