from requests import get, post

test_data = (
    ('http://localhost:5000/api/v2/user/1',
     '''{'user': {'id': 1, 'name': 'Anvar', 'surname': 'Artemov'}}'''),
    ('http://localhost:5000/api/v2/user',
     '''{'user': [{'id': 1, 'name': 'Anvar', 'surname': 'Artemov'}]}'''),
    ('http://localhost:5000/api/v2/user/ava', '''{'error': 'Not found'}'''),
    ('http://localhost:5000/api/v2/user/999', '''{'message': 'User 999 not found'}''')
)

for input_s, correct_output_s in test_data:
    f = 1
    try:
        output_s = str(get(input_s).json())


    except Exception as E:
        if correct_output_s == None:
            continue
        break
    else:

        if output_s != correct_output_s:
            f = 0
            break

test_data = (
    (['http://localhost:5000/api/v2/user/1', {}],
     '''{'message': 'The method is not allowed for the requested URL.'}'''),
    (['http://localhost:5000/api/v2/user', {}],
     '''{'message': {'name': 'Missing required parameter in the JSON body or the post body or the query string'}}'''),
    (['http://localhost:5000/api/v2/user', {'title': 'Заголовок'}],
     '''{'message': {'name': 'Missing required parameter in the JSON body or the post body or the query string'}}'''),
    (['http://localhost:5000/api/v2/user', {'name': 'John',
                                            'age': 15,
                                            'surname': 'Legend',
                                            'position': 'chief',
                                            'speciality': 'explorer',
                                            'email': 'johnlegend@nasa.com',
                                            'address': 'wallstreed,p23',
                                            'hashed_password': "imsuperhero"}],
     '''{'success': 'OK'}'''),
)
for input_s, correct_output_s in test_data:
    f = 1
    try:
        if input_s[1]:
            output_s = str(post(input_s[0], json=input_s[1]).json())
        else:
            output_s = str(post(input_s[0]).json())
        print(correct_output_s)
        print(output_s)
    except Exception as E:
        if correct_output_s == None:
            continue

        f = 0
        break
    else:
        if output_s != correct_output_s:
            f = 0
            break

if f:
    print('YES')
else:
    print('NO')
