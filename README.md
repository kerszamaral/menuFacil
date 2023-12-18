# Menu Fácil

## Sobre o projeto

O Menu Fácil é um projeto de um sistema de gerenciamento de cardápios de restaurantes. O sistema permite que o usuário crie um cardápio, adicione itens a ele e o publique. O cardápio pode ser acessado por qualquer pessoa através do portal do Menu Fácil.

## Tecnologias utilizadas

- Python 3.12.1
- Django 5

## Feito por

- [Ian Kersz Amaral](https://github.com/kerszamaral)
- [Augusto Kessler Pires](https://github.com/Gutok66)
- [Pedro Heinrique Bouvie Roewer](https://github.com/pedrohbroewer)
- [Thiago Trautwein Santos](https://github.com/ThiagoTrautwein)
- [Tiago Vier Preto](https://github.com/Tiago-Vier-Preto)

## Como rodar o projeto

### Para rodar esse projeto, inicialize um ambiente virtual com

```bash
python3 -m venv venv
```

### e ative-o com

```bash
source venv/bin/activate
```

### ou

```powershell
.\venv\Scripts\activate
```

### Depois, instale as dependências com

```bash
pip install -r requirements.txt
```

### e entre na pasta do projeto com

```bash
cd src
```

### Por fim, migre o banco de dados com

```bash
python manage.py migrate
```

### e crie os grupos de usuários com

```bash
python manage.py create_groups
```

### Para criar um superusuário, use

```bash
python manage.py createsuperuser
```

### e rode o servidor com

```bash
python manage.py runserver
```

### O servidor estará rodando em [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
