from decimal import Decimal

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from app.models import Category, Product, Review

def get_category_by_slug(db: Session, slug: str) -> Category | None:
    return db.query(Category).filter(Category.slug == slug).first()


def get_category_by_id(db: Session, id: int) -> Category | None:
    return db.query(Category).filter(Category.id == id).first()


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def create_category(db: Session, name: str, slug: str, parent_id: int | None) -> Category:
    category = Category(name=name, slug=slug, parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_slug(db: Session, slug: str) -> Product | None:
    return db.query(Product).filter(Product.slug == slug).first()


def list_products(
    db: Session,
    category_id: int | None = None,
    search: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    only_active: bool = True,
    offset: int = 0,
    limit: int = 20,
) -> list[Product]:
    query = db.query(Product)

    if only_active:
        query = query.filter(Product.is_active.is_(True))
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()


def create_product(db: Session, **fields) -> Product:
    product = Product(**fields)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, fields: dict) -> Product:
    for key, value in fields.items():
        if value is not None:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()

def search_products(
    db: Session,
    q: str | None,
    category_id: int | None,
    min_price: Decimal | None,
    max_price: Decimal | None,
    min_rating: float | None,
    sort_by: str,
    page: int,
    page_size: int,
):
    rating_subq = (
        select(
            Review.product_id,
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.product_id)
        .subquery()
    )

    stmt = select(Product, rating_subq.c.avg_rating).outerjoin(
        rating_subq, rating_subq.c.product_id == Product.id
    )

    conditions = []
    if q:
        conditions.append(Product.name.ilike(f"%{q}%"))
    if category_id is not None:
        conditions.append(Product.category_id == category_id)
    if min_price is not None:
        conditions.append(Product.price >= min_price)
    if max_price is not None:
        conditions.append(Product.price <= max_price)
    if min_rating is not None:
        conditions.append(rating_subq.c.avg_rating >= min_rating)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    sort_map = {
        "price_asc": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "newest": Product.created_at.desc(),
        "rating": rating_subq.c.avg_rating.desc().nullslast(),
    }
    stmt = stmt.order_by(sort_map[sort_by])

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    rows = db.execute(stmt).all()
    products = [row[0] for row in rows]

    return products, total