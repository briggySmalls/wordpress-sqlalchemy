from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, DateTime, UniqueConstraint, MetaData, join
from sqlalchemy.orm import relationship, backref, column_property
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AutoRepr:
    def __repr__(self):
        class_name = self.__class__.__name__
        attribute_strings = [
            "%s=%r" % (attr, getattr(self, attr))
            for attr in dir(self)
            if not attr.startswith('_') and attr != 'metadata'
        ]
        return "<%s %s>" % (class_name, ", ".join(attribute_strings))


class Comment(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_comments'
    comment_ID = Column(Integer, primary_key=True, nullable=False)
    comment_post_ID = Column(Integer, ForeignKey('wp_posts.ID'), nullable=False)
    comment_author = Column(Text(length=None), nullable=False)
    comment_author_email = Column(String(length=100), nullable=False)
    comment_author_url = Column(String(length=200), nullable=False)
    comment_author_IP = Column(String(length=100), nullable=False)
    comment_date = Column(DateTime(timezone=False), nullable=False)
    comment_date_gmt = Column(DateTime(timezone=False), nullable=False)
    comment_content = Column(Text(length=None), nullable=False)
    comment_karma = Column(Integer, nullable=False)
    comment_approved = Column(String(length=4), nullable=False)
    comment_agent = Column(String(length=255), nullable=False)
    comment_type = Column(String(length=20), nullable=False)
    comment_parent = Column(Integer, ForeignKey('wp_comments.comment_ID'), nullable=False)
    user_id = Column(Integer, ForeignKey('wp_users.ID'), nullable=False)

    # ORM layer relationships
    post = relationship('Post', back_populates="comments")
    children = relationship(
        'Comment',
        backref=backref('parent', remote_side=[comment_ID])
    )
    user = relationship('User', back_populates="comments")


class Link(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_links'
    link_id = Column(Integer, primary_key=True, nullable=False)
    link_url = Column(String(length=255), nullable=False)
    link_name = Column(String(length=255), nullable=False)
    link_image = Column(String(length=255), nullable=False)
    link_target = Column(String(length=25), nullable=False)
    link_description = Column(String(length=255), nullable=False)
    link_visible = Column(String(length=1), nullable=False)
    link_owner = Column(Integer, ForeignKey('wp_users.ID'), nullable=False)
    link_rating = Column(Integer, nullable=False)
    link_updated = Column(DateTime(timezone=False), nullable=False)
    link_rel = Column(String(length=255), nullable=False)
    link_notes = Column(Text(length=None), nullable=False)
    link_rss = Column(String(length=255), nullable=False)

    # ORM layer relationships
    owner = relationship('User', back_populates="links")


class Option(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_options'
    option_id = Column(Integer, primary_key=True, nullable=False)
    blog_id = Column(Integer, primary_key=True, nullable=False)
    option_name = Column(String(length=64), primary_key=True, nullable=False)
    option_value = Column(Text(length=None), nullable=False)
    autoload = Column(String(length=3), nullable=False)


class PostMeta(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_postmeta'
    meta_id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('wp_posts.ID'), nullable=False)
    meta_key = Column(String(length=255), primary_key=False, nullable=True)
    meta_value = Column(Text(length=None), primary_key=False, nullable=True)

    # ORM layer relationships
    post = relationship('Post', back_populates='meta')


TERM_TABLE = Table(
    "wp_terms", Base.metadata,
    Column('term_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=55), nullable=False),
    Column('slug', String(length=200), nullable=False),
    Column('term_group', Integer, nullable=False, default=0),
    UniqueConstraint('slug'),
)

TERM_TAXONOMY_TABLE = Table(
    "wp_term_taxonomy", Base.metadata,
    Column('term_taxonomy_id', Integer, primary_key=True, nullable=False),
    Column('term_id', Integer, ForeignKey('wp_terms.term_id'), nullable=False),
    Column('taxonomy', String(length=32), nullable=False),
    Column('description', Text(length=None), nullable=False, default=''),
    Column('parent', Integer, ForeignKey('wp_term_taxonomy.term_taxonomy_id'), nullable=False, default=0),
    Column('count', Integer, nullable=False, default=0),
    UniqueConstraint('term_id', 'taxonomy'),
)

TERM_TAXONOMY_JOIN = join(TERM_TABLE, TERM_TAXONOMY_TABLE)

TERM_RELATIONSHIP_TABLE = Table(
    'wp_term_relationships', Base.metadata,
    Column('object_id', Integer, ForeignKey('wp_posts.ID'), primary_key=True, nullable=False),
    Column('term_taxonomy_id', Integer, ForeignKey(TERM_TAXONOMY_TABLE.c.term_taxonomy_id), primary_key=True, nullable=False)
)


class Post(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_posts'
    ID = Column(Integer, primary_key=True, nullable=False)
    post_author = Column(Integer, ForeignKey('wp_users.ID'), nullable=False, default=0)
    post_date = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    post_date_gmt = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    post_content = Column(Text(length=None), nullable=False)
    post_title = Column(Text(length=None), nullable=False)
    post_excerpt = Column(Text(length=None), nullable=False)
    post_status = Column(String(length=10), nullable=False, default='publish')
    comment_status = Column(String(length=15), nullable=False, default='open')
    ping_status = Column(String(length=6), nullable=False, default='open')
    post_password = Column(String(length=20), nullable=False, default='')
    post_name = Column(String(length=200), nullable=False)
    to_ping = Column(Text(length=None), nullable=False, default='')
    pinged = Column(Text(length=None), nullable=False, default='')
    post_modified = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    post_modified_gmt = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    post_content_filtered = Column(Text(length=None), nullable=False, default='')
    post_parent = Column(Integer, ForeignKey('wp_posts.ID'), nullable=False, default=0)
    guid = Column(String(length=255), nullable=False)
    menu_order = Column(Integer, nullable=False, default=0)
    post_type = Column(String(length=20), nullable=False, default='post')
    post_mime_type = Column(String(length=100), nullable=False)
    comment_count = Column(Integer, nullable=False, default=0)

    # ORM layer relationships
    author = relationship('User', back_populates='posts')
    children = relationship(
        'Post',
        backref=backref('parent', remote_side=[ID]))
    comments = relationship('Comment', back_populates="post")
    meta = relationship('PostMeta', back_populates="post")
    terms = relationship(
        "Term",
        secondary=TERM_RELATIONSHIP_TABLE,
        back_populates='posts')


class Term(Base):
    # Table fields
    __table__ = TERM_TAXONOMY_JOIN
    id = column_property(
        TERM_TABLE.c.term_id,
        TERM_TAXONOMY_TABLE.c.term_id)

    # ORM layer relationships
    posts = relationship(
        "Post",
        secondary=TERM_RELATIONSHIP_TABLE,
        back_populates='terms')


class UserMeta(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_usermeta'
    umeta_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('wp_users.ID'), nullable=False)
    meta_key = Column(String(length=255), primary_key=False, nullable=True)
    meta_value = Column(Text(length=None), primary_key=False, nullable=True)

    # ORM layer relationships
    user = relationship('User', back_populates='meta')


class User(AutoRepr, Base):
    # Table fields
    __tablename__ = 'wp_users'
    ID = Column(Integer, primary_key=True, nullable=False)
    user_login = Column(String(length=60), nullable=False)
    user_pass = Column(String(length=64), nullable=False)
    user_nicename = Column(String(length=50), nullable=False)
    user_email = Column(String(length=100), nullable=False)
    user_url = Column(String(length=100), nullable=False)
    user_registered = Column(DateTime(timezone=False), nullable=False)
    user_activation_key = Column(String(length=60), nullable=False)
    user_status = Column(Integer, nullable=False)
    display_name = Column(String(length=250), nullable=False)

    # ORM layer relationships
    comments = relationship('Comment', back_populates='user')
    meta = relationship('UserMeta', back_populates='user')
    links = relationship('Link', back_populates='owner')
    posts = relationship('Post', back_populates='author')
