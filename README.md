Django REST Framework test project
==================================

A sample Django project to get familiar with Django REST Framework.
Accomplished following the [official tutorial](http://www.django-rest-framework.org/tutorial/1-serialization).

Test the project with requests like:
```
curl -iL -X GET http://127.0.0.1:8000/snippets
curl -iL -X GET http://127.0.0.1:8000/snippets/2/highlight
curl -iL -X DELETE http://127.0.0.1:8000/snippets/1/ -u admin:admin
```