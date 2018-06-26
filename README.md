# Projeto de Redes
## Diário de Bordo

### 25/06/2018
Q3 - Deu-se inicio a implementação da questão 03. Foi criada a estrutura básica do cliente e do servidor, e adicionado a funcionalidade de LOGIN.

### 06/06/2018
Q2 - Foi implementado o comando SHARE, e com ele todos os requesitos mínimos da questão 02 foram atendidos. Há um interesse por otimização e continuidade dessa questão, portanto se houver tempo ao final outras coisas serão implementadas. Dentre elas:
- Melhorar modularização
- Otimizar transferências, inclusive o GET.
- Derterminar tamanho dos buffers com algum argumento, e não arbitrariamente. 
- Usar uma nova conexão para transferência dos arquivos (out of band).

Inicia-se o estudo e o planejamento para a questão 03.

### 04/06/2018
Q2 - A implementação da transferencia de dados no GET e no POST foi alterada. Antes, lia-se todo o arquivo de uma vez, e o mesmo era mandando todo de uma vez para o socket. Isso gerava vários bugs e até impossibilitava a transferencia de arquivos maiores. Agora lê-se linha por linha, e blocos de 100 linhas são enviadas para o socket. Isso permite que arquivos grande sejam transferidos (ainda que esporádicos bugs aconteçam). Por algum motivo o comando GET é substancialmente mais lento que o POST, mesmo numa rede local, nossa única suspeita é que sejam as threads e alocamento de recursos para elas. Aproveitamos as alterações para implementar um simples sistema de porcentagem de transferência. 

### 03/06/2018
Implementado o MKDIR para criar um nova pasta na questão 02. Foi iniciada a implementação do SHARE para compartilhamento, onde o arquivo de texto já está sendo alterado, mas ao fazer um GET ele nao vai para a pasta do dono e sim do destinatário. Talvez para resolver isso seja necessário reformular toda a forma que os diretorios sao armazenados na lista.

### 02/06/2018
Implementado o PUT da questão 02. O código foi melhor modularizado em funções. Alguns bugs e erros foram corrigidos.

### 01/06/2018
Implementado o GET da questão 02. O bug na transferencia do POST foi resolvido.

### 30/05/2018
Implementados os comandos POST e DELETE na questão 02.
Algumas ponderações sobre o POST.
- A transferência de arquivos ainda apresenta bugs, como os relacionados ao tamanho do arquivo, que fazem ele ir para o próximo recv.
- Não verifica se o arquivo já existe na nuvem (POST também está sendo PUT)

### 29/05/2018
Implementada a autenticação nos arquivos da questão 02.

### 28/05/2018
Iniciado o desenvolvimento da questão 02. Começamos com o estudo de threads usando a biblioteca (legado) _thread_. Depois foi construida a estrutura de código do servidor, onde depois as funções serão desenvolvidas. Também foi mais definido de quem serão os papeis de entre o servidor e cliente.

### 24/05/2018
A parte de TCP e UDP da questão 1 se dará por um simples comunicador Cliente-Servidor, onde cada um deve esperar sua vez de falar. A parte HTTP será feita separadamente. Começou-se o estudo de Threads para as próximas questões.

### 21/05/2018
Foi feita uma redocumentação nas classes UDP, adicionou-se as classes TCP à questão 01.

### 28/04/2018
O código da questão 01 que já existia foi adaptado para usar POO. A verificação de palíndromo foi retirada.

### 20/04/2018
Foi feita a leitura do projeto e iniciado os primeiros testes que darão origem ao que será a questão 01. Por enquanto o arquivo possui duas funções, um Server UDP que escuta, e um Client UDP que envia. Ao receber algo do client, o server retorna aquilo é ou não um palíndromo. 
