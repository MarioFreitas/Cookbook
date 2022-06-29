from app_config import *
from app_index import *
from app_recipe import *
from app_edit import *
from app_new import *
from app_airFryer import *
from app_instantPot import *
from app_freezer import *
import os

if __name__ == '__main__':
    try:
        os.chdir('/home/pi/shared/Cookbook')
    except FileNotFoundError:
        pass
    app.run(debug=True, host='0.0.0.0')
