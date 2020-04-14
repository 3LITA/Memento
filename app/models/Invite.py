from app.run import db


class Invite(db.Model):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # M-O
    public_deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id'), primary_key=True
    )  # M-O
    invite_code = db.Column(db.String(100))
