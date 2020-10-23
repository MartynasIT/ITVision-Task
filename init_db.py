from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
base = declarative_base()


# I initialize database here
class Calls(base):
    __tablename__ = 'CallLog'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UUID = Column(String(250), nullable=False)
    CallStartTime = Column(Integer, nullable=True)
    CallEndTime = Column(Integer, nullable=True)
    CallerID = Column(Integer, nullable=False)
    Extension = Column(String(250), nullable=True)
    Direction = Column(String(250), nullable=True)
    DialedNumber = Column(String(250), nullable=False)
    Duration = Column(Integer, nullable=True)
    Billsec = Column(Integer, nullable=True)
    AnswerState = Column(String(250), nullable=True)

    @property
    def serialize(self):
        return {
            'ID': self.ID,
            'UUID': self.UUID,
            'CallStartTime': self.CallStartTime,
            'CallEndTime': self.CallEndTime,
            'CallerID': self.CallerID,
            'Extension': self.Extension,
            'Direction': self.Direction,
            'DialedNumber': self.DialedNumber,
            'Duration': self.Duration,
            'Billsec': self.Billsec,
            'AnswerState': self.AnswerState,
        }


engine = create_engine('sqlite:///CallLog.db')
base.metadata.create_all(engine)
