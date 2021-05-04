import sqlite3
from datetime import datetime as date
import os
from flask import Flask, g, request
from flask_restful import Resource, Api

DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = b'\xa7\xf9\x85\xac \x85\xccL\xeb\xb8\xcd\xcb\xe7Ey\xeb\xc1\xa2~E'

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

app.config.update(
    DATABASE=os.path.join(app.root_path, 'database.db')
)

print(app.config['DATABASE'])


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        g.sqlite_db.row_factory = dict_factory
    return g.sqlite_db


@app.teardown_appcontext
def close_db(self):
    if hasattr(g, 'sqlite_db'):
        print('db closed')
        g.sqlite_db.close()


class AddCourse(Resource):
    def post(self):
        title = request.json['title']

        try:
            start_date = date.strptime(request.json['start_date'], "%Y-%m-%d")
            end_date = date.strptime(request.json['end_date'], "%Y-%m-%d")
        except ValueError:
            return {"Error": "This is the incorrect date string format. It should be YYYY-MM-DD"}, 400

        lectures = int(request.json['lectures'])
        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            INSERT INTO courses (title, start_date, end_date, lectures) 
            VALUES (?, ?, ?, ?)
            """,
            (title, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), lectures)
        )
        get_db().commit()

        return {"Message": "Course added successfully"}, 200


class CoursesList(Resource):
    def get(self):
        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            SELECT title
            FROM courses
            """)
        result = [item['title'] for item in db_cursor.fetchall()]
        return {'titles': result}, 200


class GetCourseById(Resource):
    def get(self):
        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            SELECT * 
            FROM courses
            WHERE id == :_id
            """,
            {"_id": int(request.json["id"])}
        )

        if result := db_cursor.fetchone():
            return result, 200

        return {"Error": "Course with this id was not found"}, 404


class GetFilteredCourses(Resource):
    def get(self):

        try:
            start_date = date.strptime(request.json['start_date'], "%Y-%m-%d")
            end_date = date.strptime(request.json['end_date'], "%Y-%m-%d")
        except ValueError:
            return {"Error": "This is the incorrect date string format. It should be YYYY-MM-DD"}, 400

        if start_date >= end_date:
            return {"Error": "The start_date is greater than the end_date"}, 400

        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            SELECT id, start_date, end_date
            FROM courses
            WHERE title == :_title
            """,
            {"_title": request.json["title"]}
        )

        courses_dates = {course['id']: (date.strptime(course['start_date'], "%Y-%m-%d"),
                                        date.strptime(course['end_date'], "%Y-%m-%d"))
                         for course in db_cursor.fetchall()}

        accepted_courses_id = [str(_id) for _id, value in courses_dates.items()
                               if value[0] >= start_date and value[1] <= end_date]
        query = f"""
            SELECT * 
            FROM courses
            WHERE id in ({', '.join(accepted_courses_id)})
            """
        db_cursor.execute(query)
        return db_cursor.fetchall(), 200


class ChangeCourseAttributes(Resource):
    def put(self):

        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            SELECT start_date, end_date
            FROM courses
            WHERE id == :_id
            """,
            {"_id": request.json["id"]}
        )

        dates = db_cursor.fetchone()
        if not dates:
            return {"Error": "Course with this id was not found"}, 404

        if request.json.get('title'):
            self.title = request.json.get('title')

        if request.json.get('start_date'):
            try:
                self.start_date = date.strptime(request.json.get('start_date'), "%Y-%m-%d")
            except ValueError:
                return {"Error": "This is the incorrect date string format. It should be YYYY-MM-DD"}, 400

        if request.json.get('end_date'):
            try:
                self.end_date = date.strptime(request.json.get('end_date'), "%Y-%m-%d")
            except ValueError:
                return {"Error": "This is the incorrect date string format. It should be YYYY-MM-DD"}, 400

        if request.json.get('lectures'):
            self.lectures = request.json.get('lectures')

        if hasattr(self, 'start_date') and hasattr(self, 'end_date'):
            if self.start_date > self.end_date:
                return {"Error": "The start_date is greater than the end_date"}, 400

            self.start_date = self.start_date.strftime("%Y-%m-%d")
            self.end_date = self.end_date.strftime("%Y-%m-%d")

        elif hasattr(self, 'start_date'):

            if self.start_date >= date.strptime(dates['end_date'], "%Y-%m-%d"):
                return {"Error": "The start_date is greater than the end_date"}, 400

            self.start_date = self.start_date.strftime("%Y-%m-%d")

        elif hasattr(self, 'end_date'):

            if self.end_date <= date.strptime(dates['start_date'], "%Y-%m-%d"):
                return {"Error": "The end_date is smaller than the start_date"}, 400

            self.end_date = self.end_date.strftime("%Y-%m-%d")

        query = f"""
            UPDATE courses 
            SET {' , '.join(f"{key} = '{str(val)}'" for (key, val) in self.__dict__.items())}
            WHERE id == {request.json['id']}
            """
        db_cursor.execute(query)
        get_db().commit()

        return {'Message': "Course attributes changed successfully"}, 200


class DeleteCourse(Resource):
    def delete(self):

        course_id = request.json['id']

        db_cursor = get_db().cursor()
        db_cursor.execute(
            """
            SELECT * 
            FROM courses
            WHERE id == :_id 
            """,
            {'_id': course_id}
        )

        if not db_cursor.fetchone():
            return {"Error": "Course with this id was not found"}, 404

        db_cursor.execute(
            """
            DELETE
            FROM courses
            WHERE id == :_id 
            """,
            {'_id': course_id}
        )
        get_db().commit()

        return {'Message': "Course deleted successfully"}, 200


api.add_resource(AddCourse, '/add-course', methods=['POST'])
api.add_resource(CoursesList, '/get-titles-courses', methods=['GET'])
api.add_resource(GetCourseById, '/get-course', methods=['GET'])
api.add_resource(GetFilteredCourses, '/get-filtered-courses', methods=['GET'])
api.add_resource(ChangeCourseAttributes, '/change-attributes', methods=['PUT'])
api.add_resource(DeleteCourse, '/delete-course', methods=['DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
