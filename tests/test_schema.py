"""Basic schema tests"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, and_

import pytest

from wpalchemy import classes
from wpalchemy import tables


@pytest.fixture
def engine():
    """Create a test engine using simple database in memory"""
    engine = create_engine('sqlite:///:memory:', echo=False)
    tables.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_maker(engine):  # pylint: disable=redefined-outer-name
    """Create an ORM session from the engine"""
    return sessionmaker(bind=engine)


def test_term(engine, session_maker):  # pylint: disable=redefined-outer-name
    # Create a terms
    earth = classes.Term(
        name="Earth",
        slug="earth",
        taxonomy="elements",
        description="Both cold and dry")
    # Commit changes
    session = session_maker()
    session.add(earth)
    session.commit()

    # Verify term appears in table as expected
    selection = select([tables.terms, tables.term_taxonomies]).where(
        tables.terms.c.term_id == tables.term_taxonomies.c.term_id)
    result = engine.execute(selection)
    assert result.returns_rows

    # Assert the expected terms are created
    rows = result.fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row['name'] == "Earth"
    assert row['slug'] == "earth"
    assert row['taxonomy'] == "elements"
    assert row['description'] == "Both cold and dry"


def test_term_relationships(engine, session_maker):  # pylint: disable=redefined-outer-name
    # Create some posts
    taste = classes.Post(
        post_name="taste", post_title='', post_content='', post_excerpt='',
        guid='', post_mime_type='')
    touch = classes.Post(
        post_name="touch", post_title='', post_content='', post_excerpt='',
        guid='', post_mime_type='')
    # Create some terms
    earth = classes.Term(
        name="Earth",
        slug="earth",
        taxonomy="elements",
        description="Both cold and dry",
        posts=[taste, touch])
    # Commit changes
    session = session_maker()
    session.add_all([taste, touch, earth])
    session.commit()

    # Query for all term relationships
    selection = select([
        tables.posts,
        tables.term_relationships,
        tables.term_taxonomies,
        tables.terms]).where(
            and_(
                tables.term_relationships.c.object_id == tables.posts.c.ID,
                tables.term_relationships.c.term_taxonomy_id == tables.term_taxonomies.c.term_taxonomy_id,
                tables.term_taxonomies.c.term_id == tables.terms.c.term_id))
    result = session.connection().execute(selection)
    assert result.returns_rows
    rows = result.fetchall()

    # Assert expected relationships exist
    assert len(rows) == 2
    expected_rows = (
        {'post_name': "taste", 'name': "Earth"},
        {'post_name': "touch", 'name': "Earth"},
    )
    for row, expected in zip(rows, expected_rows):
        assert row['post_name'] == expected['post_name']
        assert row['name'] == expected['name']
