# run.py

import os
from flasgger import Swagger

from app import create_app

config = os.getenv('APP_CONFIG')
app = create_app(config)

Swagger(app, template_file="swager.yml")

if __name__ == '__main__':
    app.run()
