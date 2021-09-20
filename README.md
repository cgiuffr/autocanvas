# autocanvas
Automate simple Canvas tasks related to course enrollments.

Dependencies:
* Python 3.6+.
* CanvasAPI, installation instructions: https://canvasapi.readthedocs.io/en/stable/getting-started.html#installing-canvasapi.

Relevant API documentation:
* https://canvas.instructure.com/doc/api/enrollments.html
* https://canvasapi.readthedocs.io/en/stable/course-ref.html
* https://canvasapi.readthedocs.io/en/stable/enrollment-ref.html

To create a Canvas API key:
* Go to Canvas --> Profile --> Settings.
* Click on 'Approved integrations' --> 'New access token'.

Usage:

```shell
$ cp params_default.py params.py # and edit params.py
$ ./autocanvas.py
```

Example workflow to delete unenrolled students from a course:
* Create a Canvas API key as described above.
* Create a `params.py` file from `params_default.py` file.
* Edit `params.py` as follows:
  * `API_KEY`: Paste your newly created API key (access token).
  * `course`: Enter your course ID.
  * `user_file`: Enter the name of the file with all the *enrolled* students.
* Run `./autocanvas.py` to verify the list of to-be-deleted unenrolled ones.
* Edit `params.py` again as follows:
  * `action`: Enter `delete` (Warning: this action cannot be undone).
* Run `./autocanvas.py` again to actually delete unenrolled students. 