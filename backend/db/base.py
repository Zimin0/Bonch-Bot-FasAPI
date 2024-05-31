# Let's put the import of all these models in one single file named 'base.py'. It will be helpful to create all the tables at once in our web app.

from db.base_class import Base 
from db.models.user import User
from db.models.pc import PC
from db.models.session import PC_Session
from db.models.time_period import TimePeriod