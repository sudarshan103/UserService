from app.models.extensions import db
from app.models.service_user import ServiceUser


class ServiceUserRepo:
    @staticmethod
    def create(username, first_name, last_name = None, password = None):
        new_record = ServiceUser()
        new_record.username = username
        new_record.first_name = first_name
        new_record.last_name = last_name
        if password:
            new_record.set_password(password)
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @classmethod
    def authenticate_user(cls, param):
        param.update(deleted_at=None)
        return ServiceUser.find_first_by_filter(param)

    @classmethod
    def get_user_by_filter(cls, param):
        param.update(deleted_at=None)
        columns = [c for c in ServiceUser.__table__.columns if c.name != 'password']
        return db.session.query(*columns).filter_by(**param).first()

    @classmethod
    def get_all_users_by_filter(cls, param):
        param.update(deleted_at=None)
        columns = [c for c in ServiceUser.__table__.columns if c.name != 'password']
        return db.session.query(*columns).filter_by(**param).all()