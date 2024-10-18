# blueprints are imported explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .review import review_views
from .staff import staff_views
from .students import student_views
from .admin import setup_admin

# Add all blueprints to this list
views = [user_views, index_views, auth_views, review_views, staff_views, student_views]


