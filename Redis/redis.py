import gerar_dados as data

mongo_database = data.mongo_client['approvedPeople']

mongo_collection = mongo_database['people_info']

for info in mongo_collection.find():
    data.redis_client.set(info['ID'], str(info))

while True:
    user_choice = input('Choose 1 to include a new person.\n'
                        'Choose 2 to remove a person.\n'
                        'Choose 3 to exit.\n'
                        'Input: ')

    match user_choice:
        case '1':
            print()

            document = {
            f'Name': (name:=input('Name: ')),
            f'ID': (id:=input('ID: ')),
            f'Approved course': (course:=input('Approved course: ')),
            f'Year': (year:=input('Year: ')),
            }

            print()

            mongo_collection.insert_one(document)
            data.redis_client.set(id, str(document))

            print(f'{name} (ID {id}) was included in the database...\n')

        case '2':
            target = input('\nType the person\'s ID you wish to remove ("C" to cancel): ')

            if not target.lower() == 'c':
                mongo_collection.delete_one({'ID': target})
                data.redis_client.delete(target)

            print()

        case '3':
            print('\nTerminating process...')
            break

        case _: print('\nInvalid option.\n')
