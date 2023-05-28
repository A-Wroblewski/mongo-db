import pymongo
import string
import random
import redis

def generate_data():
    letters = string.ascii_letters
    digits = string.digits

    for _ in range(1, 5001):
        random_year = random.randint(2020, 2023)
        random_integer = random.randint(5, 10)
        random_string = ''.join(random.choices(letters, k=random_integer))
        random_id = ''.join(random.choices(digits, k=11))
        courses = ['Architecture', 'Biology', 'Cooking', 'Economy', 'Software Engineering',]

        strings.append({
            f'Name': random_string,
            f'ID': random_id,
            f'Approved course': random.choice(courses),
            f'Year': random_year,
            })


connection_string = 'mongodb+srv://user:password@cluster0.qnytgbo.mongodb.net/?retryWrites=true&w=majority'

mongo_client = pymongo.MongoClient(connection_string)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    if 'approvedPeople' in mongo_client.list_database_names():
        mongo_client.drop_database('approvedPeople')

        keys = redis_client.keys()
        redis_client.delete(*keys)

    db = mongo_client.approvedPeople

    people_info = db.people_info

    strings = []

    generate_data()

    people_info.insert_many(strings)
