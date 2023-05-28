import pymongo
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_fernet_key(key: bytes) -> bytes:
    assert isinstance(key, bytes)

    hlib = hashlib.md5()
    hlib.update(key)

    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


def chat():
    available_names = ['Alice', 'Bob']

    while True:
        chosen_name = input('Digite seu nome: ')

        if chosen_name in available_names:
            available_names.remove(chosen_name)

        else: raise Exception('Nome indisponível.')

        friend = available_names[0]

        chosen_option = input(f'\nVocê está conectado como: {chosen_name}.\n'
                            f'{chosen_name}, o que deseja fazer?\n'
                            f'A) Enviar uma mensagem secreta para {friend}.\n'
                            'B) Ler as mensagens que estão no banco. ')

        if chosen_option.lower() == 'a':
            message = input(f'\nOk {chosen_name}, digite a mensagem: ')

            # texto que vai ser usado pra gerar a chave
            secret_code = input('\nAgora digite um texto para cifrar sua mensagem: ')

            # gera uma chave em bytes a partir do código secreto definido
            key = generate_fernet_key(secret_code.encode('utf-8'))
            fernet = Fernet(key)

            # criptografa a mensagem
            encrypted_message = fernet.encrypt(message.encode('utf-8'))

            messages.insert_one({
                'from': chosen_name,
                'to': friend,
                'wasRead': False,
                'message': encrypted_message,
                })

            print(f'\n{chosen_name}, sua mensagem foi gravada no banco.')
            available_names.append(chosen_name)

        elif chosen_option.lower() == 'b':
            print(f'\nOlá {chosen_name}, essas são as mensagens que você recebeu:\n')

            received_messages = []

            # passa um for em todos os documentos da coleção contendo
            # to: "nome de quem tá acessando as mensagens recebidas",
            # filtra somente a chave message e tira o id (vem por padrão)
            # depois pega os valores (mensagem criptografada) e desempacota
            for info_dict in messages.find({'to': chosen_name}, {'message': True, '_id': False}):
                received_messages.append(*info_dict.values())

            counter = 1

            for message in received_messages:
                print(f'{counter}) {message}', end='\n')
                counter += 1

            print()

            chosen_message = int(input('Quer ler qual mensagem? '))

            chosen_message_index = received_messages[chosen_message - 1]

            print()

            ask_secret_code = input('Qual é o código secreto? ')

            if ask_secret_code == secret_code:
                decrypted_message = fernet.decrypt(chosen_message_index).decode('utf-8')

                print(f'\nMensagem descriptografada: {decrypted_message}')

            else: print('Código errado.')

            available_names.append(chosen_name)

        else: print('\nOpção inválida.')


conn_str = 'mongodb+srv://user:password@cluster0.dzwrbs1.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(conn_str)

db = client.Chat

messages = db.Messages

chat()
