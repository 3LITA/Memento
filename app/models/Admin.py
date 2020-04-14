from app.run import db


class Admin(db.Model):
    """
    rights: 1: admin
            2: creator
    """

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # M-O
    public_deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id'), primary_key=True
    )  # M-O
    rights = db.Column(db.Integer)
