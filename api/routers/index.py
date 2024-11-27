from . import orders, order_details, sandwiches, recipes, resources  # Add recipes and resources
from . import orders, order_details, customer, payments, ratings


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(sandwiches.router)
    app.include_router(recipes.router)  # Include recipes -troy
    app.include_router(resources.router)  # Include resources -troy
    app.include_router(customer.router)
    app.include_router(payments.router)
    app.include_router(ratings.router)
