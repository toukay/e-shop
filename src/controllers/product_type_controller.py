from flask import Blueprint, request, Response, jsonify
from sqlalchemy.orm import Session
from schemas import ProductTypeInputSchema, ProductTypeSchema
from services.product_type_service import ProductTypeService
from custom_exceptions import EntityNotFoundError
import database


product_type_bp = Blueprint("product_type", __name__)


@product_type_bp.route('/product-types', methods=['GET'])
def get_types() -> Response:
    session: Session = next(database.generate_session())
    service = ProductTypeService(session)
    product_types = service.get_all_types()
    return jsonify([ProductTypeSchema.model_validate(p_t).model_dump() for p_t in product_types])


@product_type_bp.route('/product-types/<int:product_type_id>', methods=['GET'])
def get_type(product_type_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductTypeService(session)
    try:
        product_type = service.get_type_by_id(product_type_id)
        return jsonify(ProductTypeSchema.model_validate(product_type).model_dump())
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@product_type_bp.route('/product-types', methods=['POST'])
def create_type() -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductTypeService(session)
    product_type_data = request.json
    try:
        product_type_input = ProductTypeInputSchema(**product_type_data)
        product_type = service.create_type(product_type_input)
        return jsonify(ProductTypeSchema.model_validate(product_type).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@product_type_bp.route('/product-types/<int:product_type_id>', methods=['PUT'])
def update_type(product_type_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductTypeService(session)
    product_type_data = request.json
    try:
        product_type_input = ProductTypeInputSchema(**product_type_data)
        product_type = service.update_type(product_type_id, product_type_input)
        return jsonify(ProductTypeSchema.model_validate(product_type).model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@product_type_bp.route('/product-types/<int:product_type_id>', methods=['DELETE'])
def delete_type(product_type_id: int) -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = ProductTypeService(session)
    try:
        brand = service.delete_brand(product_type_id)
        return '', 204
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
