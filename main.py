from website import db, create_app

if db != 'sport_event_db.sqlite':
    app=create_app()
    ctx=app.app_context()
    ctx.push()
    db.create_all()
    
if __name__=='__main__':
    napp=create_app()
    napp.run(debug=True)