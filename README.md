# Indicium_Tech_Code_Challenge


Etapas:
- ter instalado o docker
- git clone
- docker-compose up na pasta para inicializar o banco 


# docker run -it -v C:/Github:/project meltano/meltano init
# docker run -it -v ${PWD}:/project meltano/meltano init
dando erro nesse segundo, fica github:c: como se fosse linux   

Esse funcionou no terminal linux
## docker run -v /mnt/c/Github:/projects -w /projects meltano/meltano init meltano
