from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import text

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    role = Column(String(50), nullable=False)

    rentals = relationship("Rental", back_populates="owner")
    reviews = relationship("Review", back_populates="author")

class Rental(Base):
    __tablename__ = 'rental'

    rental_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    owner = relationship("User", back_populates="rentals")
    reservations = relationship("Reservation", back_populates="rental")
    reviews = relationship("Review", back_populates="rental")

class Reservation(Base):
    __tablename__ = 'reservation'

    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    rental = relationship("Rental", back_populates="reservations")
    transaction = relationship("Transaction", uselist=False, back_populates="reservation")

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(300))

    author = relationship("User", back_populates="reviews")
    rental = relationship("Rental", back_populates="reviews")

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    reservation_id = Column(Integer, ForeignKey('reservation.reservation_id'), nullable=False)

    reservation = relationship("Reservation", back_populates="transaction")


DATABASE_URL = "postgresql+psycopg2://postgres:38743874@localhost:5432/booking_online"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Model:
    def __init__(self):
        self.session = session

    def get_all_tables(self):
        try:
            result = self.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            return [row[0] for row in result]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_all_columns(self, table_name):
        try:
            result = self.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = :table"), {"table": table_name})
            return [row[0] for row in result]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def add_data(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            return 0

    def update_data(self, obj):
        try:
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            return 0

    def delete_data(self, obj):
        try:
            self.session.delete(obj)
            self.session.commit()
            return 1
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            return 0

    def search_data(self, model_class, **filters):
        try:
            query = self.session.query(model_class).filter_by(**filters)
            return query.all()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def generate_data(self, model_class, count):
        try:
            for i in range(count):
                if model_class == User:
                    obj = User(name=f"User{i}", email=f"user{i}@example.com", role="tenant" if i % 2 == 0 else "landlord")
                elif model_class == Rental:
                    obj = Rental(title=f"Rental {i}", description=f"Description {i}", price=100 + i, user_id=1)
                else:
                    continue

                self.session.add(obj)

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def execute_raw_query(self, query, params=None):
        try:
            result = self.session.execute(text(query), params or {})
            return result.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
