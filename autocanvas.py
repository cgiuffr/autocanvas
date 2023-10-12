#!/usr/bin/python3

import sys
import logging

from canvasapi import Canvas
from canvasapi import account
from canvasapi import requester
from types import SimpleNamespace
from datetime import datetime, timedelta

class CanvasManager():
    canvas = None
    course = None

    def __init__(self, log_level):
        logger = logging.getLogger("canvasapi")
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)

    def connect(self, url, key, course):
        self.canvas = Canvas(url, key)
        self.course = self.canvas.get_course(course)

    def close(self):
        self.canvas = None

    def get_user(self, id, id_type):
        return self.canvas.get_user(id, id_type=id_type)

    def get_target_enrollments(self, user_ids, user_id_name, type, state, role):
        enrollments = []
        user_id_set = None
        if user_ids:
            user_id_set = set(user_ids)
        for e in self.course.get_enrollments(role=role, state=state):
            user = e.user
            if not user['sis_user_id'] or not user['sis_user_id'].isnumeric():
                continue
            if not user_ids:
                enrollments.append(e)
                continue
            if type == 'new':
                if user[user_id_name] in user_id_set:
                    user_id_set.remove(user[user_id_name])
                continue
            if type == 'targets' and user[user_id_name] not in user_id_set:
                continue
            if type == 'nontargets' and user[user_id_name] in user_id_set:
                continue
            enrollments.append(e)

        if type == 'new':
            for user_id in user_id_set:
                try:
                    enrollments.append(self.new_enrollment_stub(
                        user_id, user_id_name, role[0]))
                except requester.ResourceDoesNotExist:
                    print("WARNING: Can't find user with {}: {}".format(user_id_name, user_id))

        return enrollments

    def enrollment_to_string(self, enrollment):
        e = enrollment
        u = e.user
        return f'{u["short_name"]}, {u["id"]}, {u["sis_user_id"]}, {u["login_id"]}, {e.role}, {e.enrollment_state}'

    def remove_enrollment(self, enrollment, task):
        enrollment.deactivate(task=task)

    def new_enrollment_stub(self, user_id, user_id_name, role):
        u = self.get_user(user_id, user_id_name)
        user = {'short_name': u.short_name, 'id': u.id,
                'sis_user_id': '?', 'login_id': '?'}
        user[user_id_name] = user_id
        e = SimpleNamespace(role=role, enrollment_state='new', user=user)
        return e

    def create_enrollment(self, enrollment_stub, task):
        state = task[len('new-'):]
        user = enrollment_stub.user
        notify = 'false'
        if state == 'invited':
            notify = 'true'

        # xxx: this should also include 'type' : enrollment_stub.role, but this would currently raise a bad request due to probably a bug in the canvasapi package. As a result, we always enroll students (default) right now.
        self.course.enroll_user(user['id'], enrollment={
                                'enrollment_state': state, 'notify': notify})
        return

    def handle_enrollments(self, action, enrollments):
        for e in enrollments:
            if action == 'dump':
                print(f'[{action}] {repr(e)}')
                continue
            if action == 'status':
                print(f'[{action}] {self.enrollment_to_string(e)}')
                continue
            if action in {'delete', 'conclude', 'deactivate'}:
                print(f'[{action}] {self.enrollment_to_string(e)}')
                self.remove_enrollment(e, action)
                continue
            if action in {'new-active', 'new-invited', 'new-inactive'}:
                print(f'[{action}] {self.enrollment_to_string(e)}')
                self.create_enrollment(e, action)
                continue


def main():
    try:
        import params
    except ImportError:
        print("Please create params.py based on params_default.py first.")
        sys.exit(1)

    user_ids = None
    if params.user_file:
        with open(params.user_file, 'r') as f:
            lines = [line.rstrip() for line in f]
            user_ids = lines

    cm = CanvasManager(params.log_level)
    cm.connect(params.API_URL, params.API_KEY, params.course)
    enrollments = cm.get_target_enrollments(
        user_ids, params.user_id_name, params.user_type, params.user_state, params.user_role)
    cm.handle_enrollments(params.action, enrollments)
    cm.close()


if __name__ == "__main__":
    main()
