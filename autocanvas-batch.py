#!/usr/bin/python3

import sys
import logging

import csv

from autocanvas import CanvasManager


def main():
    try:
        import params
    except ImportError:
        print("Please create params.py based on params_default.py first.")
        sys.exit(1)

    # Parse config file
    action = params.action
    if action not in ['dump', 'status']:
        action = None
    batch_file = params.user_file
    course_map = {}

    # Parse batch (course,user) file
    with open(batch_file, newline='') as csvfile:
        reader = csv.reader(
            csvfile, delimiter=params.csv_delimiter, quotechar=params.csv_quotechar)
        for row in reader:
            if len(row) < 2:
                continue
            course = row[0]
            user_id = row[1]
            if course not in course_map:
                course_map[course] = []
            course_map[course].append(user_id)

    # Process each course
    for course, user_ids in course_map.items():
        print(
            f'[info] Processing course {course} using {len(user_ids)} users...')
        cm = CanvasManager(params.log_level)
        cm.connect(params.API_URL, params.API_KEY, course)

        # First remove users
        curr_action = action
        if not curr_action:
            curr_action = 'delete'
        user_type = 'nontargets'
        enrollments = cm.get_target_enrollments(
            user_ids, params.user_id_name, user_type, params.user_state, params.user_role)
        print(
            f'[action] Performing "delete" action on {len(enrollments)} users...')
        cm.handle_enrollments(curr_action, enrollments)

        # Now add new users
        curr_action = action
        if not curr_action:
            curr_action = 'new-active'
        user_type = 'new'
        enrollments = cm.get_target_enrollments(
            user_ids, params.user_id_name, user_type, params.user_state, params.user_role)
        print(
            f'[action] Performing "new-active" action on {len(enrollments)} users...')
        cm.handle_enrollments(curr_action, enrollments)
        cm.close()


if __name__ == "__main__":
    main()
