from unittest import TestCase

from api.app import app

'''Class_API.py Tests'''


def super_user(client):
    # Login
    login_response = client.get("/api/v1/user/login", json={
        'username': 'vitaliksupercool228',
        'password': 'lolkek129L'
    })
    token = login_response.json['access_token']
    auth_header = {'Authorization': f"Bearer {token}"}
    return auth_header, 1


class MyTest(TestCase):
    client = app.test_client()

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        response = self.client.get("/api/v1/hello-world-19")
        self.assertEqual(response.status_code, 200)


class UserApiTests(TestCase):
    client = app.test_client()

    def login_header(self):
        # Login
        login_response = self.client.get("/api/v1/user/login", json={
            'username': 'arseniiohar228',
            'password': 'seniorohar228666',
        })
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['access_token']
        auth_header = {'Authorization': f"Bearer {token}"}
        return auth_header

    def test_user_ops(self):
        # Create the user
        user_data = {
            'username': 'arseniiohar228',
            'firstName': 'Arsenii',
            'lastName': 'Ohar',
            'email': 'arsen.ogar@gmail.com',
            'password': 'seniorohar228666',
            'phone': '+380987669293',
            'role': 'teacher'
        }
        headers, _ = super_user(self.client)
        response = self.client.post("/api/v1/user",
                                    json=user_data, headers=headers)

        self.assertEqual(response.status_code, 200)
        _id = int(response.json['id'])
        # Login
        auth_header = self.login_header()
        # Get the user
        user = self.client.get(f"/api/v1/user/{_id}", headers=auth_header)
        self.assertEqual(user.status_code, 200)
        # Put the user(update)
        put_response = self.client.put("/api/v1/user",
                                       headers=auth_header,
                                       json={"id": _id, "email": "senka666228@gmail.com"})
        self.assertEqual(put_response.status_code, 200)

        # Delete the user
        delete_response = self.client.delete(f"/api/v1/user/{_id}",
                                             headers=auth_header)
        self.assertEqual(delete_response.status_code, 200)

    def test_create_invalid_user(self):
        # Create the user
        user_data = {
            'username': 'arseniiohar228',
            'firstName': 'Arsenii',
            'lastName': 'Ohar',
            'email': 'arsen.ogar@gmail.com',
            'password': 'seniorohar228666',
            'phone': '+380987669293',
            'role': 'teacher'
        }
        auth_headers, _ = super_user(self.client)
        ok_response = self.client.post("/api/v1/user",
                                       json=user_data, headers=auth_headers)
        response = self.client.post("/api/v1/user",
                                    json=user_data, headers=auth_headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual(200, ok_response.status_code)
        _id = int(ok_response.json['id'])
        auth_header = self.login_header()
        # Get the user
        user = self.client.get(f"/api/v1/user/{_id}", headers=auth_header)
        self.assertEqual(user.status_code, 200)
        delete_response = self.client.delete(f"/api/v1/user/{_id}",
                                             headers=auth_header)
        self.assertEqual(delete_response.status_code, 200)


class ClassApiTests(TestCase):
    client = app.test_client()

    def test_default_class(self):
        superuser = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": superuser[1]
        }
        response = self.client.post("/api/v1/class",
                                    headers=superuser[0],
                                    json=class_
                                    )
        _id = response.json['id']
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(f"/api/v1/class/{_id}",
                                      headers=super_user(self.client)[0])
        self.assertEqual(response.status_code, 200)

    def test_complex_class(self):
        # create class
        headers, user_id = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": user_id
        }
        response = self.client.post("/api/v1/class",
                                    headers=headers,
                                    json=class_
                                    )
        self.assertEqual(response.status_code, 200)
        _id = response.json['id']

        # add a user to this class
        class_user = {
            "class_id": _id,
            "user_id": user_id
        }
        response = self.client.post("/api/v1/class/student",
                                    json=class_user,
                                    headers=headers)
        self.assertEqual(200, response.status_code)

        # get the students
        response = self.client.get(f"/api/v1/{_id}/student", headers=headers)
        students = response.json
        exists = False
        for student in students:
            if student['id'] == user_id:
                exists = True
                break

        self.assertTrue(exists)
        # remove the student

        response = self.client.delete(f"/api/v1/class/student", headers=headers,
                                      json={"user": user_id, "class": _id})
        self.assertEqual(200, response.status_code)
        # update the class
        new_title = "Other title"
        class_['title'] = new_title
        response = self.client.put(f"/api/v1/class", headers=headers, json={"id": _id, "title": new_title})

        self.assertEqual(200, response.status_code)
        # get the class
        response = self.client.get(f"/api/v1/class/{_id}", headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertIn('title', response.json)
        self.assertEqual(response.json['title'], class_['title'])

        # delete the class
        response = self.client.delete(f"/api/v1/class/{_id}",
                                      headers=headers)
        self.assertEqual(200, response.status_code)

    def test_get_all_classes(self):
        # create the user
        headers, user_id = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": user_id
        }
        response = self.client.post("/api/v1/class",
                                    headers=headers,
                                    json=class_
                                    )
        _id = response.json['id']
        self.assertEqual(response.status_code, 200)

        # get the class
        classes = self.client.get("/api/v1/class")
        self.assertEqual(classes.status_code, 200)
        b = False
        for i in classes.json:
            if i['title'] == 'SUPER UNIQUE NAME':
                b = True
                break

        self.assertTrue(b)  # assert if the item has been returned
        # delete the class
        response = self.client.delete(f"/api/v1/class/{_id}",
                                      headers=headers)
        self.assertEqual(response.status_code, 200)


class TeacherApiTests(TestCase):
    client = app.test_client()

    def test_get_teacher(self):
        headers, _id = super_user(self.client)

        response = self.client.get(f"/api/v1/teacher/{_id}", headers=headers)

        self.assertIn('user', response.json)
        self.assertIn('username', response.json['user'])
        self.assertEqual('vitaliksupercool228', response.json['user']['username'])

        print(response.json)

    def test_full_teacher(self):
        headers, _id = super_user(self.client)

        user_data = {
            'username': 'arseniiohar228',
            'firstName': 'Arsenii',
            'lastName': 'Ohar',
            'email': 'arsen.ogar@gmail.com',
            'password': 'seniorohar228666',
            'phone': '+380987669293',
            'role': 'teacher'
        }
        response = self.client.post("/api/v1/teacher", headers=headers, json={"User": user_data,
                                                                              "Teacher":
                                                                                  {"diplomas": None,
                                                                                   "employment": None,
                                                                                   }})

        self.assertEqual(200, response.status_code)
        self.assertIn('id', response.json)
        _id = response.json['id']

        response = self.client.get(f"api/v1/teacher/{_id}", headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(user_data['username'], response.json['user']['username'])

        response = self.client.delete(f"/api/v1/teacher/{_id}", headers=headers)
        self.assertEqual(200, response.status_code)

    def test_unique_teacher(self):
        headers, _id = super_user(self.client)

        user_data = {
            'username': 'arseniiohar228',
            'firstName': 'Arsenii',
            'lastName': 'Ohar',
            'email': 'arsen.ogar@gmail.com',
            'password': 'seniorohar228666',
            'phone': '+380987669293',
            'role': 'teacher'
        }
        response = self.client.post("/api/v1/teacher", headers=headers, json={"User": user_data,
                                                                              "Teacher":
                                                                                  {"diplomas": None,
                                                                                   "employment": None,
                                                                                   }})

        self.assertEqual(200, response.status_code)
        self.assertIn('id', response.json)
        _id = response.json['id']

        response = self.client.post("/api/v1/teacher", headers=headers, json={"User": user_data,
                                                                              "Teacher":
                                                                                  {"diplomas": None,
                                                                                   "employment": None,
                                                                                   }})
        self.assertEqual(400, response.status_code)

        response = self.client.delete(f"/api/v1/teacher/{_id}", headers=headers)
        self.assertEqual(200, response.status_code)


class StudentApiTests(TestCase):
    client = app.test_client()

    def test_get_all_classes(self):
        headers, _id = super_user(self.client)
        response = self.client.get(f"api/v1/classes/{_id}", headers=headers)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json)

    def test_send_request(self):
        headers, _id = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": _id
        }
        response = self.client.post("/api/v1/class",
                                    headers=headers,
                                    json=class_
                                    )
        self.assertEqual(response.status_code, 200)
        class_id = response.json['id']

        response = self.client.post(f"/api/v1/student/request/{class_id}", headers=headers)
        self.assertEqual(200, response.status_code)

        response = self.client.delete(f"/api/v1/class/{class_id}",
                                      headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_accept_request(self):
        headers, _id = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": _id
        }
        response = self.client.post("/api/v1/class",
                                    headers=headers,
                                    json=class_
                                    )
        self.assertEqual(response.status_code, 200)
        class_id = response.json['id']

        response = self.client.post(f"/api/v1/student/request/{class_id}", headers=headers)
        self.assertEqual(200, response.status_code)

        response = self.client.get(f"/api/v1/class/requests/{class_id}", headers=headers)
        request = [{"class_id": class_id,
                    "user_id": _id}]
        self.assertEqual(200, response.status_code)
        self.assertEqual(request, response.json)

        response = self.client.delete(f"/api/v1/class/{class_id}",
                                      headers=headers)
        self.assertEqual(response.status_code, 200)


class MessageApiTests(TestCase):
    client = app.test_client()

    def test_get_messages(self):
        print('test_get_messages is running')
        # Create a class
        headers, user_id = super_user(self.client)
        class_ = {
            "title": "SUPER UNIQUE NAME",
            "description": "SUPER UNIQUE DESCRIPTION",
            "teacher_id": user_id
        }
        response = self.client.post("/api/v1/class",
                                    headers=headers,
                                    json=class_
                                    )
        print(f'Response: {response.json}')
        self.assertEqual(response.status_code, 200)
        _id = response.json['id']

        # Add an invalid message
        message = {
            "content": "Hi everyone, welcome to our class! I hope you will enjoy it.",
            "date": "23-01-2004",  # this is intentional
            "user": user_id,
            "class_": _id
        }
        response = self.client.post(f"/api/v1/class/message",
                                    headers=headers,
                                    json=message)
        print(f'Response: {response.json}')
        self.assertEqual(400, response.status_code)

        # Add a valid message
        message.pop('date')
        response = self.client.post(f"/api/v1/class/message",
                                    headers=headers,
                                    json=message)
        print(f'Response: {response.json}')
        self.assertEqual(200, response.status_code)
        self.assertIn('id', response.json)

        # Delete a message
        response = self.client.delete("/api/v1/class/message",
                                      headers=headers,
                                      json={'id': response.json['id']})
        print(f'Response: {response.json}')
        self.assertEqual(200, response.status_code)

        # Get the messages
        response = self.client.get(f"/api/v1/class/messages/{_id}", headers=headers)
        print(f'Response: {response.json}')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

        # Delete a class
        response = self.client.delete(f"/api/v1/class/{_id}",
                                      headers=super_user(self.client)[0])
        print(f'Response: {response.json}')
        self.assertEqual(response.status_code, 200)
