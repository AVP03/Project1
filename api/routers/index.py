from . import orders, order_details, sandwiches, recipes, resources  # Add recipes and resources

def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(sandwiches.router)
    app.include_router(recipes.router)  # Include recipes -troy
    app.include_router(resources.router)  # Include resources -troy
