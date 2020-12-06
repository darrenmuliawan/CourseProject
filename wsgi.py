from server import app
import os
import json

environ = os.environ.get("APP_ENV")
dataconfig = json.loads(open("config.json", "r").read())
app.dataenv = dataconfig[environ]
app.rootpath = dataconfig[environ]['rootpath']
app.datasetpath = dataconfig[environ]['datasetpath']
app.searchconfig = dataconfig[environ]['searchconfig']

if __name__=="__main__":
    app.run()
