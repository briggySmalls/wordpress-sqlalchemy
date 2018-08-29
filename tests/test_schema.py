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
def session(engine):  # pylint: disable=redefined-outer-name
    """Create an ORM session from the engine"""
    return sessionmaker(bind=engine)


def test_create_term():
    # Create some posts
    hearing = wp.Post(post_name="hearing")
    touch = wp.Post(post_name="touch")
    sight = wp.Post(post_name="sight")
    taste = wp.Post(post_name="taste")
    smell = wp.Post(post_name="smell")

    # Create some terms
    earth = wp.Term(
        name="Earth",
        slug="earth",
        taxonomy="elements",
        description="Both cold and dry",
        posts=[smell, taste, sight, hearing, touch])
    aether = wp.Term(
        name="Fire",
        slug="fire",
        taxonomy="elements",
        description="Both hot and dry",
        posts=[sight, hearing, touch])
    aether = wp.Term(
        name="Aether",
        slug="aether",
        taxonomy="elements",
        description="Heavenly substance")

    # Query the posts
    assert not aether.posts
    assert len(set([hearing, touch, sight, taste, smell]).intersection(earth.posts)) == 5
    assert earth in hearing.terms
