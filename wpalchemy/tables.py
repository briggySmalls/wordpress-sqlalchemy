"""Module that makes tables accessible"""

from wpalchemy import classes


metadata = classes.Base.metadata

comments = classes.Comment.__table__
links = classes.Link.__table__
options = classes.Option.__table__
postmeta = classes.PostMeta.__table__
posts = classes.Post.__table__
term_relationships = classes.TERM_RELATIONSHIP_TABLE
term_taxonomies = classes.TERM_TAXONOMY_TABLE
terms = classes.TERM_TABLE
usermeta = classes.UserMeta.__table__
users = classes.User.__table__
