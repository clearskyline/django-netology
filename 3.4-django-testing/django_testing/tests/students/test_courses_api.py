from random import randrange
import pytest
from django_testing import settings
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


'''
The following fixture was not required in my app:

@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory
'''


@pytest.fixture()
def course_factory():
    def factory(st_q=50, *args, **kwargs):
        students_set = baker.prepare(Student, _quantity=st_q, _fill_optional=True)
        return baker.make(Course, students=students_set, *args, **kwargs)
    return factory


@pytest.fixture()
def override_max_limit():
    settings.MAX_STUDENTS_PER_COURSE = 10


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_retrieve_course(client, course_factory):
    courses = course_factory(_quantity=8)
    c_id = randrange(1, 8)
    response = client.get(f'/api/v1/courses/{c_id}/')
    assert response.status_code == 200
    assert response.json()['name'] == courses[c_id-1].name
    assert response.json()['students'] == [f'{st.name}, {st.birth_date}' for st in courses[c_id-1].students.all()]


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=8)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    for i, c in enumerate(response.json()):
        assert c['name'] == courses[i].name
        assert c['students'] == [f'{st.name}, {st.birth_date}' for st in courses[i].students.all()]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=15)
    c_id = randrange(1, 15)
    response = client.get('/api/v1/courses/', data={'id': c_id})
    assert response.status_code == 200
    assert response.json()[0]['name'] == courses[c_id-1].name
    assert response.json()[0]['students'] == [f'{st.name}, {st.birth_date}' for st in courses[c_id-1].students.all()]


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=15)
    c_id = randrange(1, 15)
    response = client.get('/api/v1/courses/', data={'name': courses[c_id].name})
    assert response.status_code == 200
    assert response.json()[0]['name'] == courses[c_id].name
    assert response.json()[0]['students'] == [f'{st.name}, {st.birth_date}' for st in courses[c_id].students.all()]


@pytest.mark.django_db()
def test_create_course(client):
    count = Course.objects.count()
    sample_course = {'name': 'python2354', 'students': []}
    response = client.post('/api/v1/courses/', data=sample_course)
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert response.json()['name'] == sample_course['name']
    assert response.json()['students'] == sample_course['students']


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=15)
    c_id = randrange(1, 15)
    upd_course = {"name": "new python course203234342", "students": []}
    response = client.patch(f'/api/v1/courses/{c_id}/', data=upd_course)
    assert response.status_code == 200
    assert response.json()['name'] == upd_course['name']
    assert response.json()['students'] == upd_course['students']


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=15)
    count = Course.objects.count()
    c_id = randrange(1, 15)
    response = client.delete(f'/api/v1/courses/{c_id}/')
    response_check = client.get(f'/api/v1/courses/{c_id}/')
    assert response.status_code == 204
    assert response_check.status_code == 404
    assert Course.objects.count() == count - 1


# additional test
@pytest.mark.parametrize('student_count', [5, 15])
@pytest.mark.django_db()
def test_settings_limit(course_factory, override_max_limit, student_count):
    course_with_students = course_factory(st_q=student_count, _quantity=1)
    course_with_students_count = course_with_students[0].students.count()
    # MAX_STUDENTS_PER_COURSE override in fixture
    assert course_with_students_count <= settings.MAX_STUDENTS_PER_COURSE
