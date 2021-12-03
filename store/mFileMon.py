import uwsgi
from uwsgidecorators import filemon

filemon('/uploader')(uwsgi.reload)
