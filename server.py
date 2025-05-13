from data.comments import Comments
from flask import Flask
from data import db_session, api_comments
from forms.user import RegisterForm
from flask import render_template, redirect
from data.users import User

from forms.login import LoginForm
from forms.user import RegisterForm
from forms.user import CommentsForm

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session#, jobs_api

from flask import request, jsonify

from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def about():
    db_sess = db_session.create_session()
    comments = db_sess.query(Comments)
    return render_template('main_page.html', comments=comments, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user.check_password(form.password.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            password=form.password.data,
            password_again=form.password_again.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/write_a_comment', methods=['GET', 'POST'])
def write_a_comment():
    form = CommentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        comment = Comments()
        comment.title = form.title.data
        comment.content = form.content.data
        comment.user_id = current_user.id
        db_sess.add(comment)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('write_a_comment.html', title='Оставить комментарий', form=form)


@app.route('/comments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comments(id):
    form = CommentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        comments = db_sess.query(Comments).filter(Comments.id == id,
                                          Comments.user == current_user
                                          ).first()
        if comments:
            form.title.data = comments.title
            form.content.data = comments.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        comments = db_sess.query(Comments).filter(Comments.id == id,
                                          Comments.user == current_user
                                          ).first()
        if comments:
            comments.title = form.title.data
            comments.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('write_a_comment.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/comments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def comments_delete(id):
    db_sess = db_session.create_session()
    comments = db_sess.query(Comments).filter(Comments.id == id,
                                      Comments.user == current_user
                                      ).first()
    if comments:
        db_sess.delete(comments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')




@app.route('/exclude')
def exclude():
    return render_template('exclude.html')

@app.route('/include')
def include():
    return render_template('include.html')


@app.route('/breakfasts')
def breakfasts():
    return render_template('breakfasts.html')

@app.route('/breakfasts/fried-egg')
def breakfasts_fe():
    return render_template('breakfasts/fried-egg.html')

@app.route('/breakfasts/omelet')
def breakfasts_om():
    return render_template('breakfasts/omelet.html')

@app.route('/breakfasts/pumpkin')
def breakfasts_pm():
    return render_template('breakfasts/pumpkin.html')

@app.route('/breakfasts/porridge')
def breakfasts_pr():
    return render_template('breakfasts/porrige.html')

@app.route('/breakfasts/cottage-cheese-pancakes')
def breakfasts_ccp():
    return render_template('breakfasts/cottage-cheese-pancakes.html')

@app.route('/breakfasts/cottage-cheese')
def breakfasts_cc():
    return render_template('breakfasts/cottage-cheese.html')

@app.route('/breakfasts/cornporridge')
def breakfasts_cp():
    return render_template('breakfasts/cornporridge.html')

@app.route('/breakfasts/buckwheat-porridge')
def breakfasts_bp():
    return render_template('breakfasts/buckwheat-porridge.html')


@app.route('/lunches')
def lunches():
    return render_template('lunches.html')

@app.route('/lunches/zhi')
def lunches_zh():
    return render_template('lunches/zhi.html')

@app.route('/lunches/rassoln')
def lunches_rs():
    return render_template('lunches/rassoln.html')

@app.route('/lunches/goroh')
def lunches_gh():
    return render_template('lunches/goroh.html')

@app.route('/lunches/grib')
def lunches_gr():
    return render_template('lunches/grib.html')

@app.route('/lunches/uha')
def lunches_uh():
    return render_template('lunches/uha.html')

@app.route('/lunches/frikad')
def lunches_fr():
    return render_template('lunches/frikad.html')

@app.route('/lunches/kartofeln')
def lunches_kf():
    return render_template('lunches/kartofeln.html')


@app.route('/dinners')
def dinners():
    return render_template('dinners.html')

@app.route('/dinners/cabbage')
def dinners_cb():
    return render_template('dinners/cabbage.html')

@app.route('/dinners/chicken')
def dinners_ch():
    return render_template('dinners/chicken.html')

@app.route('/dinners/ezhiki')
def dinners_ez():
    return render_template('dinners/ezhiki.html')

@app.route('/dinners/vegetables')
def dinners_vg():
    return render_template('dinners/vegetables.html')

@app.route('/dinners/plov')
def dinners_pl():
    return render_template('dinners/plov.html')

@app.route('/dinners/mushrooms')
def dinners_ms():
    return render_template('dinners/mushrooms.html')

@app.route('/dinners/meatballs')
def dinners_mb():
    return render_template('dinners/meatballs.html')

@app.route('/dinners/fish')
def dinners_fs():
    return render_template('dinners/fish.html')



@app.route('/desserts')
def desserts():
    return render_template('desserts.html')

@app.route('/desserts/healthy_conf')
def desserts_kf():
    return render_template('desserts/healthy-conf.html')

@app.route('/desserts/pancakes')
def desserts_pn():
    return render_template('desserts/pancakes.html')

@app.route('/desserts/porr_cake')
def desserts_pc():
    return render_template('desserts/porr-cake.html')

@app.route('/desserts/cookies')
def desserts_cs():
    return render_template('desserts/cookies.html')

@app.route('/desserts/applepie')
def desserts_ap():
    return render_template('desserts/applepie.html')

@app.route('/desserts/cornbiscuits')
def desserts_cb():
    return render_template('desserts/cornbiscuits.html')

@app.route('/desserts/pizza')
def desserts_pz():
    return render_template('desserts/pizza.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')



def create_new_user():
    user = User()
    user.email = 'castvaleria@amethyst.hs'
    user.password = '3456'
    user.password_again = '3456'
    user.surname = 'Кастомарова'
    user.name = 'Валерия'
    user.age = '12'
    user.address = '?'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def create_comment():
    db_sess = db_session.create_session()
    comments = Comments(title="Омлет", content="Прекрасный рецепт! Все получилось очень вкусно!",
                user_id=2)
    db_sess.add(comments)
    db_sess.commit()


# Api-Rest
def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"Users {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'user': users.to_dict(
            only=('email', 'name', 'password', 'surname'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('password_again', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('address', required=True)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('email', 'password', 'name', 'surname')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if args['password'] == args['password_again']:
            users = User(
                email=args['email'],
                password=args['password'],
                password_again=args['password_again'],
                surname=args['surname'],
                name=args['name'],
                age=args['age'],
                address=args['address']
            )
            session.add(users)
            session.commit()
            return jsonify({'id': users.id})
        return 'password != password_again'


def abort_if_comments_not_found(comments_id):
    session = db_session.create_session()
    comments = session.query(Comments).get(comments_id)
    if not comments:
        abort(404, message=f"Comments {comments_id} not found")


parser1 = reqparse.RequestParser()
parser1.add_argument('title', required=True)
parser1.add_argument('content', required=True)
parser1.add_argument('user_id', required=True)


class CommentsResource(Resource):
    def get(self, comments_id):
        abort_if_comments_not_found(comments_id)
        session = db_session.create_session()
        comments = session.query(Comments).get(comments_id)
        return jsonify({'comments': comments.to_dict(
            only=('title', 'content', 'user_id'))})

    def delete(self, comments_id):
        abort_if_comments_not_found(comments_id)
        session = db_session.create_session()
        comments = session.query(Comments).get(comments_id)
        session.delete(comments)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, comments_id):
        args = parser1.parse_args()
        session = db_session.create_session()
        abort_if_comments_not_found(comments_id)
        comments = session.query(Comments).get(comments_id)
        session.delete(comments)
        comments = Comments(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id']
        )
        session.add(comments)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        comments = session.query(Comments).all()
        return jsonify({'comments': [item.to_dict(
            only=('title', 'content', 'user_id')) for item in comments]})

    def post(self):
        args = parser1.parse_args()
        session = db_session.create_session()
        comments = Comments(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id']
        )
        session.add(comments)
        session.commit()
        return jsonify({'id': comments.id})





if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.register_blueprint(api_comments.blueprint)

    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')

    api.add_resource(CommentsListResource, '/api/comments')
    api.add_resource(CommentsResource, '/api/comments/<int:comments_id>')

    #create_new_user()
    #create_comment()
    app.run()
