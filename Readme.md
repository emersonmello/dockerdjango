# Usando docker-compose para combinar: nginx, postgresql e django

## Requisitos

- [Docker Engine](https://docs.docker.com/linux/) 1.11 ou superior
- [Docker Compose](https://docs.docker.com/compose/install/) 1.7.1 ou superior

## Passos para carregar os *containers*, criar esquema no banco de dados e subir a aplicação

1.	git clone http://github.com/emersonmello/dockerdjango
1.	cd dockerdjango
1.	docker-compose up
1.	docker-compose run web python manage.py migrate
1.	docker-compose run web python manage.py loaddata catalog/fixtures/fixture.json

Por fim, abra o navegador web e aponte para: http://localhost 


