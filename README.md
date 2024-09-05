# SUSP

Uma plataforma para auxiliar na busca por atendimento na rede pública de saúde

## Ambiente de Desenvolvimento

Nosso ambiente de desenvolvimento possui:

- Python 3.12

Instale o python, crie um _venv_ com `python -m venv .venv`, ative com `source .venv/bin/activate` (repita isso sempre que abrir um novo _shell_ na pasta raíz do projeto). Com o _venv_ ativo, execute `pip install -r requirements.txt` para instalar as dependências e execute com `fastapi dev src/app.py` (sempre com o _venv_ ativo). 

O projeto por padrão fica hospedado em `localhost:8000`

## Padrões de Projeto

### Desenvolvimento

Usamos duas _branches_ principais: `main` e `dev`. Na `main` teremos apenas versões estáveis da plataforma, na `dev` teremos sempre a versão mais atualizada do projeto com os PR mais recentes.

Novas contribuições devem ser feitas sempre criando novas _branches_ a partir da `dev` e finalizadas com um PR para a `dev`. 

### Branches e Commits

Vamos usar os padrões dos [_conventional commits_](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13).

Para nome de _branches_ vamos usar `kebab-case` iniciando com um tipo dos _conventional commits_.

Para _commits_, _branches_ e código em geral vamos dar preferência pela língua inglesa.