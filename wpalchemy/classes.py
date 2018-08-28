from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
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
    __tablename__ = 'wp_comments'
    comment_ID = Column(Integer, primary_key=True)
    comment_post_ID = Column(Integer, ForeignKey('wp_posts.ID'))
    comment_author = Column(Text(length=None))
    comment_author_email = Column(String(length=100))
    comment_author_url = Column(String(length=200))
    comment_author_IP = Column(String(length=100))
    comment_date = Column(DateTime(timezone=False))
    comment_date_gmt = Column(DateTime(timezone=False))
    comment_content = Column(Text(length=None))
    comment_karma = Column(Integer)
    comment_approved = Column(String(length=4))
    comment_agent = Column(String(length=255))
    comment_type = Column(String(length=20))
    comment_parent = Column(Integer, ForeignKey('wp_comments.comment_ID'))
    user_id = Column(Integer, ForeignKey('wp_users.ID'))

    post = relationship('Post', back_populates="comments")
    parent = relationship('Comment', back_populates="children")
    children = relationship('Comment', back_populates="parent")
    user = relationship('User', back_populates="comments")


class Link(AutoRepr, Base):
    __tablename__ = 'wp_links'
    link_id = Column(Integer, primary_key=True)
    link_url = Column(String(length=255))
    link_name = Column(String(length=255))
    link_image = Column(String(length=255))
    link_target = Column(String(length=25))
    link_description = Column(String(length=255))
    link_visible = Column(String(length=1))
    link_owner = Column(Integer, ForeignKey('wp_users.ID'))
    link_rating = Column(Integer)
    link_updated = Column(DateTime(timezone=False))
    link_rel = Column(String(length=255))
    link_notes = Column(Text(length=None))
    link_rss = Column(String(length=255))

    owner = relationship('User', back_populates="links")


class Option(AutoRepr, Base):
    __tablename__ = 'wp_options'
    option_id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, primary_key=True)
    option_name = Column(String(length=64), primary_key=True)
    option_value = Column(Text(length=None))
    autoload = Column(String(length=3))


class PostMeta(AutoRepr, Base):
    __tablename__ = 'wp_postmeta'
    meta_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('wp_posts.ID'))
    meta_key = Column(String(length=255), primary_key=False)
    meta_value = Column(Text(length=None), primary_key=False)

    post = relationship('Post', back_populates='meta')


TERM_RELATIONSHIP_TABLE = Table(
    'wp_term_relationships', Base.metadata,
    Column('object_id', Integer, ForeignKey('left.id')),
    Column('term_taxonomy_id', Integer, ForeignKey('right.id'))
)


class Post(AutoRepr, Base):
    __tablename__ = 'wp_posts'
    ID = Column(Integer, primary_key=True)
    post_author = Column(Integer, ForeignKey('wp_users.ID'))
    post_date = Column(DateTime(timezone=False))
    post_date_gmt = Column(DateTime(timezone=False))
    post_content = Column(Text(length=None))
    post_title = Column(Text(length=None))
    post_excerpt = Column(Text(length=None))
    post_status = Column(String(length=10))
    comment_status = Column(String(length=15))
    ping_status = Column(String(length=6))
    post_password = Column(String(length=20))
    post_name = Column(String(length=200))
    to_ping = Column(Text(length=None))
    pinged = Column(Text(length=None))
    post_modified = Column(DateTime(timezone=False))
    post_modified_gmt = Column(DateTime(timezone=False))
    post_content_filtered = Column(Text(length=None))
    post_parent = Column(Integer, ForeignKey('wp_posts.ID'))
    guid = Column(String(length=255))
    menu_order = Column(Integer)
    post_type = Column(String(length=20))
    post_mime_type = Column(String(length=100))
    comment_count = Column(Integer)

    author = relationship('User', back_populates='posts')
    parent = relationship('Post', back_populates='children')
    comments = relationship('Post', back_populates="post")
    meta = relationship('PostMeta', back_populates="post")
    taxonomies = relationship(
        "TermTaxonomy",
        secondary=TERM_RELATIONSHIP_TABLE,
        back_populates='posts')


class TermTaxonomy(AutoRepr, Base):
    __tablename__ = 'wp_term_taxonomy'
    term_taxonomy_id = Column(Integer, primary_key=True)
    term_id = Column(Integer, ForeignKey('wp_terms.term_id'))
    taxonomy = Column(String(length=32))
    description = Column(Text(length=None))
    parent = Column(Integer, ForeignKey('wp_term_taxonomy.term_taxonomy_id'))
    count = Column(Integer)

    __table_args__ = (
        UniqueConstraint('term_id', 'taxonomy'),
    )

    term = relationship("Term", back_populates='taxonomy')
    posts = relationship(
        "Post",
        secondary=TERM_RELATIONSHIP_TABLE,
        back_populates="taxonomies")


class Term(AutoRepr, Base):
    __tablename__ = 'wp_terms'
    term_id = Column(Integer, primary_key=True)
    name = Column(String(length=55))
    slug = Column(String(length=200))
    term_group = Column(Integer)

    __table_args__ = (
        UniqueConstraint('slug'),
    )

    taxonomy = relationship("TermTaxonomy", back_populates='term')


class UserMeta(AutoRepr, Base):
    __tablename__ = 'wp_usermeta'
    umeta_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('wp_users.ID'))
    meta_key = Column(String(length=255), primary_key=False)
    meta_value = Column(Text(length=None), primary_key=False)

    user = relationship('User', back_populates='meta')


class User(AutoRepr, Base):
    __tablename__ = 'wp_users'
    ID = Column(Integer, primary_key=True)
    user_login = Column(String(length=60))
    user_pass = Column(String(length=64))
    user_nicename = Column(String(length=50))
    user_email = Column(String(length=100))
    user_url = Column(String(length=100))
    user_registered = Column(DateTime(timezone=False))
    user_activation_key = Column(String(length=60))
    user_status = Column(Integer)
    display_name = Column(String(length=250))

    comments = relationship('Comment', back_populates='user')
    meta = relationship('UserMeta', back_populates='user')
    links = relationship('Link', back_populates='owner')
    posts = relationship('Post', back_populates='author')
