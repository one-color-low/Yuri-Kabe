import uwsgi
from uwsgidecorators import filemon

filemon('/Yuri-Kabe')(uwsgi.reload)
