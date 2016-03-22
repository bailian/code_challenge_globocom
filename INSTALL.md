** Instruções para configuração do ambiente que o sistema será executado

Assumindo que no SO já possui python instalado e o usuário possui permissão de SUDO, devemos seguir as etapas abaixo:

Dentro do projeto foi criado o script Fabfile.py que automatiza toda configuração de ambiente do projeto e realiza tarefas de deploy.
Antes de utilizar deve ser alterado alguns dados das variáveis env, tais como: senha do banco de dados, hosts do banco de dados,hosts, usuário, etc.

- Montar ambiente
  Para montar o ambiente deve rodar o script por linha de comando:
  Fab local master config_env setup

  - local: informações do ambiente que será montado
  - master: branch que será utilizada para baixar o código do repositório.
  - config_env: configurações que serão utilizadas para criar o ambiente de acordo com o OS.
  - setup: método que irá criar os diretórios utilizados pela aplicação, criação da virtualenv, clone do projeto, checkout da última versão da branch, instalar os requirements na virtualenv, instalar as configurações do Nginx.
  - create_database: Cria a base de dados do projeto.

  O arquivo de automação possui muitos outros métodos para administração do projeto nas instâncias dos servidores.