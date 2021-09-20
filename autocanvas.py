#!/usr/bin/python3

import sys

from canvasapi import Canvas

try:
    import params
except ImportError:
    print("Please create params.py based on params_default.py first.")
    sys.exit(1)

class CanvasManager():
    canvas = None
    course = None

    def connect(self, url, key, course):
        self.canvas = Canvas(url, key)
        self.course = self.canvas.get_course(course)
    
    def get_target_enrollments(self, user_file, user_file_id, user_file_type, state, role):
        enrollments = []
        ids = {}
        if user_file:
            with open(user_file, 'r') as f:
                lines = [line.rstrip() for line in f]
                ids = set(lines)
        for e in self.course.get_enrollments(role=role, state=state):
            user = e.user
            if not user_file:
                enrollments.append(e)
                continue
            if user_file_type == 'targets' and user[user_file_id] not in ids:
                continue
            if user_file_type == 'nontargets' and user[user_file_id] in ids:
                continue
            enrollments.append(e)
        return enrollments
    
    def enrollment_to_string(self, enrollment):
        e = enrollment
        u = e.user
        return f'{u["short_name"]}, {u["sis_user_id"]}, {u["login_id"]}, {e.role}, {e.enrollment_state}'
    
    def remove_enrollment(self, enrollment, task):
        enrollment.deactivate(task=task)

cm = CanvasManager()
cm.connect(params.API_URL, params.API_KEY, params.course)
enrollments = cm.get_target_enrollments(params.user_file, params.user_file_id, params.user_file_type, params.user_state, params.user_role)

for e in enrollments:
    u = e.user
    if params.action == 'dump':
        print(f'[{params.action}] {repr(e)}')
        continue
    if params.action == 'status':
        print(f'[{params.action}] {cm.enrollment_to_string(e)}')
        continue
    if params.action in {'delete', 'conclude', 'deactivate'}:
        print(f'[{params.action}] {cm.enrollment_to_string(e)}')
        cm.remove_enrollment(e, params.action)
        continue

sys.exit(0)
