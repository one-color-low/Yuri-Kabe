# ファイル更新を検知してuwsgiを自動的に再起動するプログラムです。

import uwsgi
from uwsgidecorators import filemon

filemon('/uploader')(uwsgi.reload)
