docker build [path] -t [nazov_kontajneru]
docker run [nazov_kontajneru]

docker build . -t my_python_app
docker run my_python_app

---------------------------------------------
py -m pip install uvicorn
py -m pip install fastapi