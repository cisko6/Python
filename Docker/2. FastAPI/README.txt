docker build . -t fast-api

docker run -p 8000:8000 --name mycontainername fast-api
	-> musíme explicitne zadať port, pretože to nefungovalo

