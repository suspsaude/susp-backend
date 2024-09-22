# SUSP

Uma plataforma para auxiliar na busca por atendimento na rede pública de saúde

## Como executar o projeto

### Pré-requisitos

Instale o Docker e o Docker Compose em sua máquina.

Copie o arquivo `.env.example` para `.env` e preencha as variáveis de ambiente.

## Ambiente de Desenvolvimento

Dado o Docker Compose configurado, basta executar o comando:

```bash
docker-compose --profile dev up
```

Note que, caso você tenha baixado algum pacote de python, deve ser rodado o comando com a flag `--build` para que o container seja reconstruído com as novas dependências.

```bash
docker-compose --profile dev up --build
```

Nesse caso, o container já estará configurado para hot reload, ou seja, qualquer alteração no código fonte será refletida automaticamente no container.

O projeto por padrão fica hospedado em `localhost:8000`

Para encerrar a execução do projeto, basta executar:

```bash
docker-compose down
```

Você pode querer instalar as dependências do projeto em sua máquina local para ter melhor autocomplete ou uso do LSP. Para isso, basta seguir os passos abaixo:
1. Inicie um ambiente virtual com `python -m venv .venv`
2. Ative o ambiente virtual com `source .venv/bin/activate`
3. Instale as dependências do projeto com `pip install -r requirements.txt`

## Ambiente de Produção

Para rodar o projeto em produção, execute:

```bash
docker-compose --profile prod up --build -d
```

Da mesma forma que o Ambiente de Desenvolvimento, o projeto deverá estar em `localhost:8000` por padrão.

Para encerrar:

```bash
docker-compose down
```

## Padrões de Projeto

### Desenvolvimento

Usamos duas _branches_ principais: `main` e `dev`. Na `main` teremos apenas versões estáveis da plataforma, na `dev` teremos sempre a versão mais atualizada do projeto com os PR mais recentes.

Novas contribuições devem ser feitas sempre criando novas _branches_ a partir da `dev` e finalizadas com um PR para a `dev`.

### Branches e Commits

Vamos usar os padrões dos [_conventional commits_](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13).

Para nome de _branches_ vamos usar `kebab-case` iniciando com um tipo dos _conventional commits_.

Para _commits_, _branches_ e código em geral vamos dar preferência pela língua inglesa.
