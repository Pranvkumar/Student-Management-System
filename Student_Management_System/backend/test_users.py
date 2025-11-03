from database import DatabaseConnection

db = DatabaseConnection()
users = db.execute_query('SELECT username, password, role FROM Users')

if users:
    print('\n✅ Database connected successfully!')
    print('\n📋 Users in database:')
    print('-' * 60)
    for user in users:
        print(f"Username: {user['username']:20} Password: {user['password']:15} Role: {user['role']}")
    print('-' * 60)
    print(f'\nTotal users: {len(users)}')
else:
    print('❌ No users found or database connection failed!')
    print('Please run the SQL files to insert sample data.')
