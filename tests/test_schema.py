"""Basic schema tests"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from wpalchemy import classes as wp


@pytest.fixture
def engine():
    """Create a test engine using simple database in memory"""
    return create_engine('sqlite:///:memory:', echo=True)


@pytest.fixture
def session(engine):
    """Create an ORM session from the engine"""
    return sessionmaker(bind=engine)


def test_create_post(session):
    comment = wp.Comment()
    post = wp.Post()
