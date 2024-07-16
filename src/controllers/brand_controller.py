from flask import Blueprint, request, Response, jsonify 
from sqlalchemy.orm import Session
from schemas import BrandInputSchema, BrandSchema
from services.brand_service import BrandService
from custom_exceptions import EntityNotFoundError

import database

brand_bp = Blueprint("brand", __name__)

@brand_bp.route('/brands', methods=['GET'])
def get_brands() -> Response:
    session: Session = next(database.generate_session())
    service = BrandService(session)
    brands = service.get_all_brands()
    return jsonify([BrandSchema.model_validate(brand).model_dump() for brand in brands])


@brand_bp.route('/brands/<int:brand_id>', methods=['GET'])
def get_brand(brand_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = BrandService(session)
    try:
        brand = service.get_brand_by_id(brand_id)
        return jsonify(BrandSchema.model_validate(brand).model_dump())
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@brand_bp.route('/brands', methods=['POST'])
def create_brand() -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = BrandService(session)
    brand_data = request.json
    try:
        brand_input = BrandInputSchema(**brand_data)
        brand = service.create_brand(brand_input)
        return jsonify(BrandSchema.model_validate(brand).model_dump()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@brand_bp.route('/brands/<int:brand_id>', methods=['PUT'])
def update_brand(brand_id: int) -> Response | tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = BrandService(session)
    brand_data = request.json
    try:
        brand_input = BrandInputSchema(**brand_data)
        brand = service.update_brand(brand_id, brand_input)
        return jsonify(BrandSchema.model_validate(brand).model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@brand_bp.route('/brands/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id: int) -> tuple[Response, int]:
    session: Session = next(database.generate_session())
    service = BrandService(session)
    try:
        brand = service.delete_brand(brand_id)
        return '', 204
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
