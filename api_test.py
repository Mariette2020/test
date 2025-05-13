from requests import get, post, delete, put


print(get('http://127.0.0.1:5000/api/comments').json())

print(get('http://127.0.0.1:5000/api/comments/1').json())

print(get('http://127.0.0.1:5000/api/comments/10').json())

#print(get('http://127.0.0.1:5000/api/comments/ab').json())

print()

print(post('http://127.0.0.1:5000/api/comments', json={}).json())

print(post('http://127.0.0.1:5000/api/comments',
           json={'email': 'Заголовок'}).json())

'''print(post('http://127.0.0.1:5000/api/comments',
           json={'title': 'Щи',
                 'content': 'Очень вкусный суп',
                 'user_id': '3'
                 }).json())
'''
print()

print(delete('http://127.0.0.1:5000/api/comments/999').json())

print(delete('http://127.0.0.1:5000/api/comments/3').json())

print()

print(get('http://127.0.0.1:5000/api/users').json())

print(get('http://127.0.0.1:5000/api/users/1').json())

print(get('http://127.0.0.1:5000/api/users/10').json())

print()

print(post('http://127.0.0.1:5000/api/users', json={}).json())

print(post('http://127.0.0.1:5000/api/users',
           json={'email': 'Заголовок'}).json())

'''print(post('http://127.0.0.1:5000/api/users',
           json={'email': 'vitaerbium@selenim.hs',
                 'password': '1356',
                 'password_again': '1356',
                 'surname': 'Эрбиева',
                 'name': 'Виталия',
                 'age': '12',
                 'address': 'Анаида, Зеленоградская 12'
                 }).json())

print()'''

print(delete('http://127.0.0.1:5000/api/users/1').json())

print(put('http://127.0.0.1:5000/api/comments/12',
           json={'title': 'Щиииииииииииии',
                 'content': 'Очень вкусный суп',
                 'user_id': '3'
                 }).json())

'''print(get('http://127.0.0.1:5000/api/v2/jobs').json())

print(get('http://127.0.0.1:5000/api/v2/jobs/1').json())

print(get('http://127.0.0.1:5000/api/v2/jobs/6').json())

print(get('http://127.0.0.1:5000/api/v2/jobs/a').json())

print()

print(post('http://localhost:8080/api/v2/jobs', json={}).json())

print(post('http://localhost:8080/api/v2/jobs',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:8080/api/v2/jobs',
           json={'title': 'Action #14',
                 'title_of_activity': 'Creating environmental services',
                 'team_leader': 'Emma Meledanri',
                 'duration': '35 hours',
                 'list_of_collaborators': '11, 12, 13',
                 'is_finished': 'Is not finished'
                 }).json())

print()

print(delete('http://localhost:8080/api/jobs/999').json())

print(delete('http://localhost:8080/api/jobs/13').json())
'''