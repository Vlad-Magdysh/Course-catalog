import unittest
import os
import tempfile
from app import flask_app, init_db


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
        flask_app.config['TESTING'] = True
        self.test_app = flask_app.test_client()
        init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_app.config['DATABASE'])

    def test_success_add_course(self):
        # Given
        expected_message = {"message": "Course added successfully"}
        expected_code = 200
        # When
        rv = self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                     "end_date": "2019-07-12", 'lectures': 7})
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_wrong_date_format_DD_MM_YYYY(self):
        # Given
        expected_message = {"message": "This is the incorrect date string format. It should be YYYY-MM-DD"}
        expected_code = 400
        # When
        rv = self.test_app.post('/add-course', json={"title": "course1", "start_date": "11-09-2011",
                                                     "end_date": "09-07-2012", 'lectures': 7})
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_wrong_date_format_MM_YYYY_DD(self):
        # Given
        expected_message = {"message": "This is the incorrect date string format. It should be YYYY-MM-DD"}
        expected_code = 400
        # When
        rv = self.test_app.post('/add-course', json={"title": "course1", "start_date": "11-2011-18",
                                                     "end_date": "09-2012-01", 'lectures': 5})
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_wrong_date_range(self):
        # Given
        expected_message = {"message": "The start_date is equal or greater than the end_date"}
        expected_code = 400
        # When
        rv = self.test_app.post('/add-course', json={"title": "course1", "start_date": "2019-11-11",
                                                     "end_date": "2019-07-12", 'lectures': 7})
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_get_titles_courses(self):
        # Given
        expected = {"titles": ["course1", "course2", "course3"]}
        expected_code = 200
        # When
        self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "course2", "start_date": "2015-01-17",
                                                "end_date": "2018-05-11", 'lectures': 24})
        self.test_app.post('/add-course', json={"title": "course3", "start_date": "2019-02-21",
                                                "end_date": "2019-11-22", 'lectures': 6})
        rv = self.test_app.get('/get-titles-courses')
        # Then
        self.assertEqual(expected, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_empty_get_courses_titles(self):
        # Given
        expected = {'titles': []}
        expected_code = 200
        # When
        rv = self.test_app.get('/get-titles-courses')
        # Then
        self.assertEqual(expected, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_get_by_id(self):
        # Given
        expected_id = 2
        expected_answer = {"id": expected_id, "title": "right_course2", "start_date": "2015-01-17",
                           "end_date": "2018-05-11", 'lectures': 24}
        expected_code = 200
        # When
        self.test_app.post('/add-course', json={"title": "wrong_course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "right_course2", "start_date": "2015-01-17",
                                                "end_date": "2018-05-11", 'lectures': 24})
        self.test_app.post('/add-course', json={"title": "wrong_course3", "start_date": "2019-02-21",
                                                "end_date": "2019-11-22", 'lectures': 6})
        rv = self.test_app.get('/get-course', json={"id": expected_id})
        # Then
        self.assertEqual(expected_answer, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_wrong_get_by_id(self):
        # Given
        expected_id = 4
        expected_message = {"message": "Course with this id was not found"}
        expected_code = 404
        # When
        self.test_app.post('/add-course', json={"title": "wrong_course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "wrong_course2", "start_date": "2015-01-17",
                                                "end_date": "2018-05-11", 'lectures': 24})
        self.test_app.post('/add-course', json={"title": "wrong_course3", "start_date": "2019-02-21",
                                                "end_date": "2019-11-22", 'lectures': 6})
        rv = self.test_app.get('/get-course', json={"id": expected_id})
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_get_filtered_courses(self):
        # Given
        expected = {"title": "course", "start_date": "2017-01-01", "end_date": "2020-01-01"}
        expected_answer = {
            '2': {"id": 2, "title": "course", "start_date": "2018-01-17", "end_date": "2018-05-11", 'lectures': 14},
            '3': {"id": 3, "title": "course", "start_date": "2017-02-21", "end_date": "2018-10-22", 'lectures': 6},
            '6': {"id": 6, "title": "course", "start_date": "2017-02-21", "end_date": "2019-11-22", 'lectures': 16}
        }
        # When
        self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "course", "start_date": "2018-01-17",
                                                "end_date": "2018-05-11", 'lectures': 14})
        self.test_app.post('/add-course', json={"title": "course", "start_date": "2017-02-21",
                                                "end_date": "2018-10-22", 'lectures': 6})
        self.test_app.post('/add-course', json={"title": "course2", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 7})
        self.test_app.post('/add-course', json={"title": "course", "start_date": "2010-01-17",
                                                "end_date": "2018-05-11", 'lectures': 34})
        self.test_app.post('/add-course', json={"title": "course", "start_date": "2017-02-21",
                                                "end_date": "2019-11-22", 'lectures': 16})
        rv = self.test_app.get('/get-filtered-courses', json=expected)
        # Then
        self.assertEqual(expected_answer, rv.get_json())

    def test_change_attributes(self):
        # Given
        _id = 2
        expected_title = 'changed_title'
        expected_end_date = '2021-09-15'
        query = {'id': _id, 'title': expected_title, "end_date": expected_end_date}
        expected_message = {'message': "Course attributes changed successfully"}
        expected_code = 200
        # When
        self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "course2", "start_date": "2018-01-17",
                                                "end_date": "2018-05-11", 'lectures': 14})
        self.test_app.post('/add-course', json={"title": "course3", "start_date": "2017-02-21",
                                                "end_date": "2018-10-22", 'lectures': 6})
        msg = self.test_app.put('/change-attributes', json=query)
        rv = self.test_app.get('/get-course', json={"id": _id})
        # Then
        self.assertEqual(_id, rv.get_json().get('id'))
        self.assertEqual(expected_title, rv.get_json().get('title'))
        self.assertEqual(expected_end_date, rv.get_json().get('end_date'))
        self.assertEqual(expected_message, msg.get_json())
        self.assertEqual(expected_code, msg.status_code)

    def test_wrong_change_attributes(self):
        # Given
        _id = 1
        wrong_start_date = '2022-01-01'
        wrong_end_date = '2021-09-15'
        query = {'id': _id, 'start_date': wrong_start_date, "end_date": wrong_end_date}
        expected_message = {"message": "The start_date is equal or greater than the end_date"}
        expected_code = 400
        # When
        self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        rv = self.test_app.put('/change-attributes', json=query)
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_empty_change_attributes(self):
        # Given
        _id = 2
        expected_title = 'changed_title'
        expected_end_date = '2021-09-15'
        query = {'id': _id, 'title': expected_title, "end_date": expected_end_date}
        expected_message = {"message": "Course with this id was not found"}
        expected_code = 404
        # When
        rv = self.test_app.put('/change-attributes', json=query)
        # Then
        self.assertEqual(expected_message, rv.get_json())
        self.assertEqual(expected_code, rv.status_code)

    def test_delete_course(self):
        # Given
        expected_id = 2
        expected_delete_message = {'message': "Course deleted successfully"}
        expected_get_message = {"message": "Course with this id was not found"}
        # When
        self.test_app.post('/add-course', json={"title": "course1", "start_date": "2018-09-11",
                                                "end_date": "2019-07-12", 'lectures': 17})
        self.test_app.post('/add-course', json={"title": "course2", "start_date": "2018-01-17",
                                                "end_date": "2018-05-11", 'lectures': 14})
        self.test_app.post('/add-course', json={"title": "course3", "start_date": "2017-02-21",
                                                "end_date": "2018-10-22", 'lectures': 6})
        msg = self.test_app.delete('/delete-course', json={'id': expected_id})
        rv = self.test_app.get('/get-course', json={'id': expected_id})
        # Then
        self.assertEqual(expected_delete_message, msg.get_json())
        self.assertEqual(expected_get_message, rv.get_json())

    def test_empty_delete_course(self):
        # Given
        expected_id = 2
        expected_message = {"message": "Course with this id was not found"}
        # When
        rv = self.test_app.delete('/delete-course', json={'id': expected_id})
        # Then
        self.assertEqual(expected_message, rv.get_json())


if __name__ == '__main__':
    unittest.main()
