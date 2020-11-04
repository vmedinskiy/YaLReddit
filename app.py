from datetime import timedelta
from flask import Flask, request, jsonify
from tools.misc import check_keys, make_resp, create_jwt_generate_response
from tools.my_json_encoder import MyJSONEncoder
from posts.post import Post
from posts.repo import InMemoryPostsRepo
# from users.repo import InMemoryUsersRepo
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from users.sqlite_repo import SqliteUsersRepo
from users.user import User

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.user_repo = SqliteUsersRepo("./db/redditclone.db")
# app.user_repo = InMemoryUsersRepo()
app.post_repo = InMemoryPostsRepo()
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRES'] = timedelta(hours=24)
app.config['JWT_HEADER_NAME'] = 'authorization'
app.config['JWT_IDENTITY_CLAIM'] = 'user'
# app.user_repo.request_create("vvm", "12345678")
app.jwt = JWTManager(app)


@app.route('/', defaults={'path': ''})
@app.route('/a/<path:path>')
@app.route('/u/<path:path>')
def root(path):
    return app.send_static_file("index.html")


@app.route("/api/login", methods=['POST'])
def user_login():
    if not request.json:
        return make_resp(jsonify({'error': 'Empty request'}), 400)
    elif not check_keys(request.json, ('username', 'password')):
        return make_resp(jsonify({'message': 'Bad request'}), 400)
    user, error = app.user_repo.authorize(request.json["username"], request.json["password"])
    if user is None:
        return make_resp(jsonify({'message': error}), 400)
    return create_jwt_generate_response(user)


@app.route("/api/posts/", methods=["GET"])
def get_all_posts():
    return make_resp(jsonify(app.post_repo.get_all()), 200)


@app.route("/api/posts/<category_name>", methods=["GET"])
def get_posts_by_category(category_name):
    return make_resp(jsonify(app.post_repo.get_by_category(category_name)), 200)


@app.route("/api/user/<user_login>", methods=["GET"])
def get_posts_by_user_login(user_login):
    return make_resp(jsonify(app.post_repo.get_by_user_login(user_login)), 200)


@app.route("/api/post/<int:post_id>", methods=["GET"])
def get_post_by_id(post_id):
    return make_resp(jsonify(app.post_repo.get_by_id(post_id)), 200)


@app.route("/api/post/<int:post_id>", methods=["DELETE"])
@jwt_required
def delete_post_by_id(post_id):
    result = app.post_repo.request_delete(post_id, User(**get_jwt_identity()))
    if result is not None:
        return make_resp(jsonify({"message": result}), 400)
    else:
        return make_resp(jsonify({"message": "success"}), 200)


@app.route("/api/posts/", methods=["POST"])
@jwt_required
def add_post():
    if not request.json:
        return make_resp(jsonify({'message': 'Empty request'}), 400)
    elif not check_keys(request.json, ("category", "type", "title")):
        return make_resp(jsonify({'message': 'Bad request'}), 400)
    post = Post(**request.json)
    post.author = User(**get_jwt_identity())
    post = app.post_repo.request_create(post)
    return make_resp(jsonify(post), 200)


@app.route("/api/register", methods=['POST'])
def user_register():
    if not request.json:
        return make_resp(jsonify({'message': 'Empty request'}), 400)
    elif not check_keys(request.json, ('username', 'password')):
        return make_resp(jsonify({'message': 'Bad request'}), 400)
    created_user = app.user_repo.request_create(request.json["username"], request.json["password"])
    if created_user is None:
        return make_resp(jsonify({'message': "duplicated username"}), 400)
    return create_jwt_generate_response(created_user)


if __name__ == '__main__':
    app.run()
