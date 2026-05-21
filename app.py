# app.py - Application Factory & Entry Point

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import CONNECTION_STRING, SECRET_KEY
from models import db, User

# ── Extensions ──────────────────────────────────────────────────────────────
bcrypt  = Bcrypt()
login_manager = LoginManager()
csrf    = CSRFProtect()


def create_app():
    app = Flask(__name__)

    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from routes.auth_routes     import auth_bp
    from routes.admin_routes    import admin_bp
    from routes.customer_routes import customer_bp
    from routes.manager_routes  import manager_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp,    url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(manager_bp,  url_prefix='/manager')

    # Home route
    @app.route('/')
    def index():
        from models import Product, Category, Brand
        products   = Product.query.filter_by(IsActive=True).limit(8).all()
        categories = Category.query.all()
        brands     = Brand.query.all()
        return render_template('index.html', products=products,
                               categories=categories, brands=brands)

    # Product listing (public)
    @app.route('/products')
    def products():
        from flask import request
        from models import Product, Category, Brand
        category_id = request.args.get('category', type=int)
        brand_id    = request.args.get('brand',    type=int)
        search      = request.args.get('search',   '')

        query = Product.query.filter_by(IsActive=True)
        if category_id:
            query = query.filter_by(CategoryID=category_id)
        if brand_id:
            query = query.filter_by(BrandID=brand_id)
        if search:
            query = query.filter(Product.ProductName.ilike(f'%{search}%'))

        products   = query.all()
        categories = Category.query.all()
        brands     = Brand.query.all()
        return render_template('products.html', products=products,
                               categories=categories, brands=brands,
                               selected_cat=category_id, selected_brand=brand_id, search=search)

    # Product detail (public)
    @app.route('/product/<int:pid>')
    def product_detail(pid):
        from models import Product, Review
        product = Product.query.get_or_404(pid)
        reviews = Review.query.filter_by(ProductID=pid, Status='Approved').all()
        return render_template('product_detail.html', product=product, reviews=reviews)

    # 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── Run ──────────────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
