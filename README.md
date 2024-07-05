# Car Rental System API

Este projeto é um Minimum Viable Product (MVP) e parte integrante da disciplina "Desenvolvimento Full Stack Básico", do curso de Pós-Graduação em Engenharia de Software da Pontifícia Universidade Católica do Rio de Janeiro (PUC-Rio). Trata-se de uma API desenvolvida em Python e com Flask, junto com a criação de um banco de dados com as tabelas **car**, **user** e **rental**. A API possui as rotas GET, POST e DELETE.

---
## Instalação

### 1. Clonar o repositório:

```
git clone https://github.com/FernandoMiyazaki/puc-rio-mvp1-back-end.git
```

### 2. Abrir o repositório:

```
cd puc-rio-mvp1-back-end
```

### 3. Criar e ativar um ambiente virtual

Windows

```
python -m venv venv
```
```
.\venv\Scripts\activate
```

Mac/Linux

```
python3 -m venv venv
```
```
source venv/bin/activate
```

### 4. Fazer a instalação das bibliotecas Python listadas no `requirements.txt`.

```
pip install -r requirements.txt
```

### 5. Executar a API:

```
flask run --host 0.0.0.0 --port 5000
```

### 6. Acessar a documentação da aplicação:

Abra o [http://127.0.0.1:5000] no navegador.
