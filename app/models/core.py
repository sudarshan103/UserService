import uuid
from datetime import datetime, timezone

from flask import current_app
from flask_sqlalchemy.session import Session
from sqlalchemy import Column, Integer, DateTime, inspect, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from app import db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def new_session() -> Session:
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    SessionFactory = sessionmaker(engine)
    return SessionFactory()


def manage_database_and_tables():
    """
    Ensures the database exists and creates the necessary tables.
    """
    # Get the SQLAlchemy engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # Check if the database exists
    if not database_exists(engine.url):
        create_database(engine.url)  # Create the database
        print("Database created successfully.")

    # Create tables based on the models
    db.create_all()
    print("Tables created successfully.")

class Id:
    id = Column(Integer, primary_key=True, autoincrement=True)
    def __eq__(self, other):
        """Check equality based on the primary key."""
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

class CoreMethods:
    def to_dict(self):
        """Convert the SQLAlchemy model instance into a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update_from_dict(self, data):
        """Update model instance with the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        """Generate a string representation of the model instance."""
        attrs = ", ".join(f"{key}={repr(value)}" for key, value in self.to_dict().items())
        return f"<{self.__class__.__name__}({attrs})>"


    def save(self, session: Session, flush_only=False):
        """
        Save the current instance to the session.
        Optionally flush instead of committing.

        Args:
            session (Session): The SQLAlchemy session.
            flush_only (bool): If True, flush changes without committing.

        Returns:
            self: Returns the instance for chaining.
        """
        try:
            session.add(self)
            if flush_only:
                session.flush()  # Generate primary key but don't commit.
            else:
                session.commit()
            return self
        except SQLAlchemyError as e:
            session.rollback()
            raise e


    def delete(self, session: Session):
        """Delete the current instance from the database."""
        session.delete(self)
        session.commit()

    @classmethod
    def find_first_by_filter(cls, filter_dict):
        return db.session.query(cls).filter_by(**filter_dict).first()

    @classmethod
    def find_all_by_filter(cls, filter_dict):
        return db.session.query(cls).filter_by(**filter_dict).all()

    def refresh(self, session: Session):
        """
        Refresh the instance with the latest database state.

        Args:
            session (Session): The SQLAlchemy session.
        """
        try:
            session.refresh(self)
        except SQLAlchemyError as e:
            session.rollback()
            raise e


class CoreModel(db.Model, Id, CoreMethods):
    pass

class Uuid:
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))


class RecordDate:
    created = Column(DateTime, default=datetime.now(timezone.utc), nullable= False)
    updated = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, onupdate=datetime.now(timezone.utc))

class SoftDelete:
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        """Mark the record as deleted."""
        self.deleted_at = datetime.now(timezone.utc)

    def is_deleted(self):
        """Check if the record is soft-deleted."""
        return self.deleted_at is not None
