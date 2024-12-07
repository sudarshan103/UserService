
from sqlalchemy import Column, String, BigInteger, Boolean
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.core import RecordDate, SoftDelete, CoreMethods, Uuid
from app.models.extensions import db


class ServiceUser(db.Model, CoreMethods, RecordDate, Uuid, SoftDelete):
    __tablename__ = 'service_user'  # Name of the table in the database
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(256), nullable=False, index=True)
    password = Column(String(256), nullable=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=True)
    is_admin = Column(Boolean, default=False)

    # Method to check password hash
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Method to hash the password before saving
    def set_password(self, password):
        self.password = generate_password_hash(password)