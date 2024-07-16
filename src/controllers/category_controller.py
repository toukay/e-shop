from flask import Blueprint, request, Response, jsonify 
from sqlalchemy.orm import Session
from schemas import CategoryInputSchema, CategorySchema
from services.category_service import CategoryService
from custom_exceptions import EntityNotFoundError

import database

category_bp = Blueprint("category", __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories() -> Response:
    session: Session = next(database.generate_session())
    service = CategoryService(session)
    categories = service.get_all_categories()
    return jsonify([CategorySchema.model_validate(category).model_dump() for category in categories])


@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = CategoryService(session)
    try:
        category = service.get_category_by_id(category_id)
        return jsonify(CategorySchema.model_validate(category).model_dump())
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@category_bp.route('/categories', methods=['POST'])
def create_category() -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = CategoryService(session)
    category_data = request.json
    try:
        category_input = CategoryInputSchema(**category_data)
        category = service.create_category(category_input)
        return jsonify(CategorySchema.model_validate(category).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = CategoryService(session)
    category_data = request.json
    try:
        category_input = CategoryInputSchema(**category_data)
        category = service.update_category(category_id, category_input)
        return jsonify(CategorySchema.model_validate(category).model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int) -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = CategoryService(session)
    try:
        category = service.delete_category(category_id)
        return '', 204
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
