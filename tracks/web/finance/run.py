from webapp import db, create_app
from webapp.users.models import User, Role, UserRoles
from webapp.transactions.models import Share, Transaction


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'UserRoles': UserRoles,
            'Share': Share, 'Transaction': Transaction}


if __name__ == "__main__":
    app.run(debug=True)
