# tela inicial:
    # Título: Hashzap
    # Botão: Iniciar o chat
        # quando clicar no botão:
        # abrir um popup
            # Título: Bem vindo ao Hashzap
            # Caixa de Texto: Escreva seu nome no chat
            #Botão: Entrar no chat
                # quando clicar no botão: 
                    # Sumir com o título e com o botão de Iniciar Chat
                        # carregar o chat
                        # carregar o campo de enviar mensagem: 'Digite sua mensagem'
                        # Botão enviar
                            # quando clicar no botão enviar 
                            # envia a mensagem e limpa a caixa de mensagem


# Utilizando o  Flet
# importar o Flet
import flet as ft

# Criar uma função principal para rodar o seu aplicativo
def main(pagina):
    # Título
    texto = ft.Text('Hashzap')

    chat = ft.Column()

    nome_usuario =  ft.TextField(label='Escreva seu nome')
    

    # websocket - tunel de comunicação entre 2 usuários
    def enviar_msg_tunel(mensagem):
        tipo = mensagem['tipo']
        if tipo == 'mensagem':
            texto_mensagem = mensagem['texto']
            usuario_mensagem = mensagem['usuario']
            # adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem['usuario']
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=ft.colors.ORANGE_500))
        pagina.update()

    pagina.pubsub.subscribe(enviar_msg_tunel)

    
    def enviar_mensagem(evento):
        pagina.pubsub.send_all({'texto': campo_mensagem.value, 'usuario': nome_usuario.value, 'tipo': 'mensagem'})
        # limpar a caixa de enviar mensagem
        campo_mensagem.value = ''
        pagina.update()

    campo_mensagem = ft.TextField(label='Digite aqui sua mensagem', on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton('Enviar', on_click=enviar_mensagem)
    
    def entrar_popup(evento):
        pagina.pubsub.send_all({'usuario': nome_usuario.value, 'tipo': 'entrada'})
        # adicionar o chat
        pagina.add(chat)
        # fechar o popup
        popup.open = False
        # Sumir com o botão Iniciar Chat
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        # Carregar campo de enviar mensagem
        # Carregar o botão enviar mensagem
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
        ))

        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text('Bem vindo ao Hashzap'),
        content=nome_usuario,
        actions=[ft.ElevatedButton('Entrar', on_click=entrar_popup)],
        )
        
    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton('Iniciar chat', on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main)

# deploy