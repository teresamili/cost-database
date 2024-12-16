# views/__init__.py
from .auth import auth_blueprint
from .project import project_blueprint
from .individual_project import individual_project_blueprint
from .individual_projects2 import individual_project2_blueprint
from .unit_price import unit_price_blueprint
from .material_price import material_price_blueprint

__all__ = [
    'auth_blueprint',
    'project_blueprint',
    'individual_project_blueprint',
    'individual_project2_blueprint',
    'unit_price_blueprint',
    'material_price_blueprint'
]