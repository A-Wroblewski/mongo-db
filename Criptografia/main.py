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

        chosen_option = input(f'\nVocê se conectou como: {chosen_name}.\n'
                            f'{chosen_name}, o que deseja fazer?\n\n'
                            f'A) Enviar uma mensagem secreta para {friend}.\n'
                            'B) Ler as mensagens que estão no banco. ')

        if chosen_option.lower() == 'q': break

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

            print(f'{chosen_name}, sua mensagem foi gravada no banco.\n')
            available_names.append(chosen_name)

        elif chosen_option.lower() == 'b':
            received_messages = []

            # passa um for em todos os documentos da coleção contendo
            # to: "nome de quem tá acessando as mensagens recebidas",
            # filtra somente a chave message e tira o id (vem por padrão)
            # depois pega os valores (mensagem criptografada) e desempacota
            for info_dict in messages.find({'to': chosen_name}, {'message': True, '_id': False}):
                received_messages.append(*info_dict.values())

            if not received_messages:
                print('\nVocê não recebeu nenhuma mensagem.\n')
                available_names.append(chosen_name)
                continue

            print(f'\nOlá {chosen_name}, essas são as mensagens que você recebeu:\n')

            counter = 1

            for msg in received_messages:
                print(f'{counter}) {msg}', end='\n')
                counter += 1

            print()

            chosen_message = int(input('Quer ler qual mensagem? '))
            chosen_message = received_messages[chosen_message - 1]

            print()

            ask_secret_code = input('Qual é o código secreto? ')

            # erro aqui no caso de 2 códigos diferentes...
            # caso uma mensagem seja enviada e outro código secreto seja escolhido,
            # a mensagem enviada com o código antigo vai dar erro se ele for o novo
            if ask_secret_code == secret_code:
                decrypted_message = fernet.decrypt(chosen_message).decode('utf-8')

                messages.update_one(
                    {'message': chosen_message},
                    {'$set': {'wasRead': True}}
                )

                print(f'\nMensagem descriptografada: {decrypted_message}\n')

            else: print('Código errado.\n')

            available_names.append(chosen_name)

        else:
            print('\nOpção inválida.\n')
            available_names.append(chosen_name)


connection_string = 'mongodb+srv://user:password@cluster0.dzwrbs1.mongodb.net/?retryWrites=true&w=majority'

mongo_client = pymongo.MongoClient(connection_string)

if 'Chat' in mongo_client.list_database_names():
    mongo_client.drop_database('Chat')

db = mongo_client.Chat

messages = db.Messages

chat()
