API_URL =       'https://canvas.vu.nl'
API_KEY =       '<your_key_here>' # See README.MD for how to create one.

course =        '<your_course_here>'
action =        'status' # Any of 'dump', 'status', 'delete', 'conclude', 'deactivate'.
user_file =     '<your_file_here.csv>' # list of target/non-target users, one per line. None ignores the user_file.
user_file_id =  'sis_user_id' # sis_user_id, login_id (i.e., student-number, student-id).
user_file_type = 'nontargets' # 'targets' / 'nontargets'
user_state =    [] # List of 'active', 'invited', 'creation_pending', 'deleted', 'rejected', 'completed', 'inactive', 'current_and_invited', 'current_and_future', 'current_and_concluded'. Empty list stands for 'All'.
user_role =     ['StudentEnrollment'] # List of: 'StudentEnrollment', 'TeacherEnrollment', 'TaEnrollment', 'ObserverEnrollment', 'DesignerEnrollment', 'Coordinator'. Empty list stands for 'All'.
