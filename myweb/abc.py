from main import db
from models import User

u = User(first_name = 'Le', last_name = 'Bonh', email = 'lethanhbinh12t5nh2020@gmail.com', password_hash='daaritroxx')

db.session.add(u)