from . import orders, order_details, customer, payments, ratings


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(customer.router)
    app.include_router(payments.router)
    app.include_router(ratings.router)
