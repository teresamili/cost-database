# views/__init__.py
from .auth import auth_blueprint
from .project import project_blueprint
from .individual_project import individual_project_blueprint
from .individual_projects2 import individual_project2_blueprint
from .unit_price import unit_price_blueprint
from .material_price import material_price_blueprint
from .road import road_blueprint
from .bridge import bridge_blueprint
from .culvert import culvert_blueprint
from .drainage import drainage_blueprint
from .traffic import traffic_blueprint
from .lighting import lighting_blueprint
from .waterpipe import waterpipe_blueprint
from .electrical import electrical_blueprint
from .telecom import telecom_blueprint
from .green import green_blueprint
from .tunnel import tunnel_blueprint



__all__ = [
    'auth_blueprint',
    'project_blueprint',
    'individual_project_blueprint',
    'individual_project2_blueprint',
    'unit_price_blueprint',
    'material_price_blueprint',
    'road_blueprint',
    'bridge_blueprint',
    'culvert_blueprint',
    'drainage_blueprint',
    'traffic_blueprint',
    'lighting_blueprint',
    'waterpipe_blueprint',
    'electrical_blueprint',
    'telecom_blueprint',
    'green_blueprint',
    'tunnel_blueprint',
    ]