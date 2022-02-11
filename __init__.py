from flask import Flask

app = Flask(__name__)

import views

print('''
.-,--.       .   . .      ,,--. .---. 
 '|__/ . . ,-| ,-| |  ,-. |`, | \___  
 ,|    | | | | | | |  |-' |   |     \ 
 `'    `-^ `-^ `-^ `' `-' `---' `---' 
 ''')

views._index()
