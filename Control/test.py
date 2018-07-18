from Database.DB import DB

# db = DB(table='status')
# db.insert(mac='12:23:34', name='mtk', task='stress')
# db.insert(mac='23:34:45', name='weishitong', task='perform')
# print(db.display_all())

data = {
    'name': 'haolimin',
    'sex': 'male'
}
if type(data) is dict:
    print('dict')
