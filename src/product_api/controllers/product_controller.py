from flask import Blueprint, request, Response, jsonify 
from sqlalchemy.orm import Session
from schemas import ProductInputSchema, ProductSchema
from services.product_service import ProductService
from custom_exceptions import EntityNotFoundError

import database

product_bp = Blueprint("product", __name__)

@product_bp.route('/products', methods=['GET'])
def get_products() -> Response:
    session: Session = next(database.generate_session())
    service = ProductService(session)
    products = service.get_all_products()
    return jsonify([ProductSchema.model_validate(product).model_dump() for product in products])


@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductService(session)
    try:
        product = service.get_product_by_id(product_id)
        return jsonify(ProductSchema.model_validate(product).model_dump())
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route('/products', methods=['POST'])
def create_product() -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductService(session)
    product_data = request.json
    try:
        product_input = ProductInputSchema(**product_data)
        product = service.create_product(product_input)
        return jsonify(ProductSchema.model_validate(product).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductService(session)
    product_data = request.json
    try:
        product_input = ProductInputSchema(**product_data)
        product = service.update_product(product_id, product_input)
        return jsonify(ProductSchema.model_validate(product).model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int) -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductService(session)
    try:
        product = service.delete_product(product_id)
        return '', 204
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
