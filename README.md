# NLP_Bot

`ensaio_0.md`: https://github.com/MatFreitas/NLP_Bot/blob/main/ensaio_0.md

`ensaio_1.md`: https://github.com/MatFreitas/NLP_Bot/blob/main/ensaio_1.md

`ensaio_2.md`: https://github.com/MatFreitas/NLP_Bot/blob/main/ensaio_2.md

`ensaio_3.md`: https://github.com/MatFreitas/NLP_Bot/blob/main/ensaio_3.md

### Para rodar esse projeto localmente

Primeiramente, é necessário ir até o [Discord Developer Portal](https://discord.com/developers/applications). Se não tiver uma conta discord, crie uma. Logo 
em seguida, será necessário obter o `TOKEN` da aplicação. Para isso:

1. Clique no botão "Criar aplicação"
2. Dê um nome à sua aplicação e clique em "Criar"
3. Clique na seção "Bot" na barra lateral esquerda
4. Clique no botão "Adicionar Bot"
5. Copie o token fornecido na seção "Token de autenticação" Lembre-se de manter o token em sigilo, pois ele é usado para controlar o acesso ao seu bot. 
É altamente recomendável que você não compartilhe o token com ninguém ou o inclua em arquivos públicos, como repositórios no GitHub.

Para dar as permissões necessárias para o Bot e conectá-lo a um servidor, ainda no Discord Developer Portal:

1. Clique na aplicação (bot) que você deseja adicionar ao servidor
2. Clique na seção "Bot" na barra lateral esquerda
3. Acione todos os toggles de "Privileged Gateway Intents"
3. Clique na seção "OAuth2" na barra lateral esquerda
4. Selecione a opção URL Generator
5. Em scopes, selecione "bot"
6. Selecione "Admin" como priviégio
7. Clique no botão "Gerar link de convite"
8. Copie o link gerado
9. Cole o link em seu navegador
10. Selecione o servidor ao qual você deseja adicionar o bot
11. Clique no botão "Autorizar" Isso adicionará o bot ao servidor como um membro e permitirá que ele envie e receba mensagens, 
assim como outros membros. Lembre-se de que você precisa ser um administrador do servidor para adicionar o bot. Depois de adicionar
o bot ao servidor, você pode usar o nome do servidor e o ID do canal em seu código para fazer o bot se conectar ao canal específico.

Agora, basta substituir no arquivo `discord_bot.py` os campos `TOKEN`, com o token copiado no passo 5 da primeira etapa, `GUILD_NAME`, com o nome do
servidor ao qual você adicionou o bot, e, finalmente, `CHANNEL_NAME` com o nome do canal do servidor no qual você deseja que o bot envie mensagens.
Depois, rode esse arquivo e o bot estará online e responderá a comandos.

### Comandos

- O comando `!source` retorna um link para o repositório onde está o código-fonte do chatbot.
- O comando `!author` retorna o nome e e-mail do autor do chatbot.
