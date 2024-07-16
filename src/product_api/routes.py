from flask import Blueprint
from controllers.product_controller import product_bp
from controllers.brand_controller import brand_bp
from controllers.product_type_controller import product_type_bp
from controllers.category_controller import category_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(product_bp, url_prefix='/api')
api_bp.register_blueprint(brand_bp, url_prefix='/api')
api_bp.register_blueprint(product_type_bp, url_prefix='/api')
api_bp.register_blueprint(category_bp, url_prefix='/api')
