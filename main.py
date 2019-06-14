# Copyright 2019
#
# Workshop Ninja Python

import ninja
import config


app = ninja.create_app(config)


# TODO: Esto es sólo cuando ejecutamos localmente. Revisar app.yaml
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
