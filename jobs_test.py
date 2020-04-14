from requests import get, post

test_data = (
    ('http://localhost:5000/api/v2/jobs/1',
     '''{'jobs': {'job': 'WebTort', 'user': {'name': 'Anvar'}, 'work_size': 12}}'''),
    ('http://localhost:5000/api/v2/jobs',
     '''{'jobs': [{'job': 'WebTort', 'user': {'name': 'Anvar'}, 'work_size': 12}, {'job': 'Заголовок', 'user': {'name': 'Anvar'}, 'work_size': 15}, {'job': 'Заголовок', 'user': {'name': 'Anvar'}, 'work_size': 15}, {'job': 'Заголовок', 'user': {'name': 'Anvar'}, 'work_size': 15}]}'''),
    ('http://localhost:5000/api/v2/jobs/ava', '''{'error': 'Not found'}'''),
    ('http://localhost:5000/api/v2/jobs/999', '''{'message': 'Jobs 999 not found'}''')
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
    (
    ['http://localhost:5000/api/v2/jobs/1', {}], '''{'message': 'The method is not allowed for the requested URL.'}'''),
    (['http://localhost:5000/api/v2/jobs', {}],
     '''{'message': {'job': 'Missing required parameter in the JSON body or the post body or the query string'}}'''),
    (['http://localhost:5000/api/v2/jobs', {'title': 'Заголовок'}],
     '''{'message': {'job': 'Missing required parameter in the JSON body or the post body or the query string'}}'''),
    (['http://localhost:5000/api/v2/jobs', {'job': 'Заголовок',
                                            'work_size': 15,
                                            'team_leader': 1,
                                            'is_finished': False,
                                            'collaborators': '1,2,3'}],
     '''{'success': 'OK'}'''),
)
for input_s, correct_output_s in test_data:
    f = 1
    try:
        if input_s[1]:
            output_s = str(post(input_s[0], json=input_s[1]).json())
        else:
            output_s = str(post(input_s[0]).json())
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
