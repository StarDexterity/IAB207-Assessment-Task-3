# This file creates a new copy of the database 
# *** WARNING ***
# All data from any pre-existing database will be lost
# Note: 
#   Small changes to db can be done from with db browser
# Use with extreme caution
from website import create_app, db

if __name__ == "__main__":
    if input("Continue? (Y/N)") == "Y":
        app = create_app()
        db.init_app(app)
        ctx=app.app_context()
        ctx.push()
        db.drop_all()
        db.create_all()