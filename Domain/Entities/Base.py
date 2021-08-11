from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Table

Base = declarative_base()

project_tag = Table('project_tag', Base.metadata,
    Column('project_id', ForeignKey('projects.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

post_tag = Table('post_tag', Base.metadata,
    Column('post_id', ForeignKey('posts.id')),
    Column('tag_id', ForeignKey('tags.id'))
)