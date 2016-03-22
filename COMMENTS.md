** Projeto desevolvido utilizando as tecnologias abaixo:

- Linguagem: Python 2.7.5
- Framework: Django 1.9.4
- Database: Mysql 5.6.14
- Framework JS: jQuery 1.12.2
- Framework Teste de carga: Locust

De acordo com o escopo do desafio eu criei todo o ciclo pertinente a votação do programa Big Brother Brasil com as entidades: edições do programa, participantes, paredões e votação dos paredões que podem ser visualizadas e administradas através do admin da aplicação que pode ser visializado acessando a url: http://<Dominio>/admin/.

- Admin
  O admin não customizado, pois acreditei que o foco seria na votação dos usuários, com mais tempo poderia ser alterado o template e criado mais features.
Não está sendo criado os testes unitários do admin, pois já existe testes feitos pelo próprio framework.

- Front da aplicação
  Tentei criar um layout baseado no layout atual do site do programa com as mesmas cores, header e footer. Com mais tempo o layout poderia ter sido mais elaborado, utilizar a fonts corretas, incluir widgets com enquetes, informações, publicidades, funcionalidades que fariam o usuário ter um maior tempo de navegação no site.

Telas de votação e resultado
  De acordo com o layput do desafio verifiquei que as telas eram popin's, tentei deixar o mais próximo possível de acordo com as ferraments(GIMP) utilizadas para medir, cortar e etc.
  Não utilizei as imagens dos participantes que estavam no sprite, pois como criei a app participantes e achei melhor o usuário(admin) efetuar o upload da mesma pela app, desa forma pode ser alterada quando quiser. A imagem dos participantes encontra-se dentro do projeto na app core/static/_img.

  Quando a index é carregada ela já vem com o form de votação no contexto da página, desa forma é montado o form no popin. Foi utilizado a proteção do CSRF para evitar as requisições de votação de outros domínios.

  A votação é feita via ajax utilizando o método POST, evidando o form serializado que será validado no backend, caso tenha sucesso é efetuado a votação ou retornará uma mensagem de erro para o usuário, solicitando que tente efetuar o voto mais tarde. Não é informado o motivo do erro, por motivo de evitar que essas informações possam ser utilizadas para efetuar ataques ao sistema.

Tempo restante para votação
  Não utilizei um websockect no resultado da votação, pois não tive tempo para implementação.

Teste de carga
  Utilizando a ferramenta de teste de carga Locust, pois a mesma é em python e não é necessário criar nenhum arquivo de configuração em xml. Nunca tinha tido contato com a ferramenta, mas achei fácil de utilizar e com boa documentação.

Dump da base de dados
  No projeto possui um dump da base de dados.

Credenciais
  Admin
    usuário: admin
    senha: qw34rt67