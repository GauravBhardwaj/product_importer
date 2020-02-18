# from flask import request, jsonify
# from sqlalchemy.sql import ClauseElement
#
# from app.api import bp
#
#
# # @bp.route('/products', methods=['POST'])
# # def create_user():
# #     pass
# from app.models import product
# from app import db
# ALLOWED_EXTENSIONS = set(['.csv', '.txt'])
#
#
# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# def get_or_create(session, model, defaults=None, **kwargs):
#     instance = session.query(model).filter_by(**kwargs).first()
#     if instance:
#         return instance, False
#     else:
#         params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
#         params.update(defaults or {})
#         instance = model(**params)
#         session.add(instance)
#         return instance, True
#
# @bp.route('/product_upload', methods=['POST'])
# def create_product():
#     if 'file' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#
#     file = request.files['file']
#     if file.filename == '':
#         resp = jsonify({'message': 'No file selected for uploading'})
#         resp.status_code = 400
#         return resp
#
#     if file and allowed_file(file.filename):
#         #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         resp = jsonify({'message': 'File successfully uploaded'})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
#         resp.status_code = 400
#         return resp