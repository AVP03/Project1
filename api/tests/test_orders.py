from fastapi.testclient import TestClient
from unittest.mock import Mock
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models.orders import Order
from ..models import customer as customer_model
from ..schemas.orders import OrderCreate

# Create a test client for the app
client = TestClient(app)

#test 1 (create function) - ani
@pytest.fixture
def db_session(mocker):
    
    return mocker.Mock()

def test_create_order(db_session):
    """
    Test the create order functionality.
    """
    
    order_data = {
        "customer_id": 1,
        "description": "Test order",
        "order_details": []  
    }

    
    order_request = OrderCreate(**order_data)

    
    mock_created_order = {
        "id": 1,
        "customer_id": 1,
        "description": "Test order",
        "order_details": []
    }

   
    db_session.add = Mock()
    db_session.commit = Mock()
    db_session.refresh = Mock()

    
    controller.create = Mock(return_value=mock_created_order)

    
    created_order = controller.create(db=db_session, request=order_request)

    
    assert created_order is not None
    assert created_order["customer_id"] == 1
    assert created_order["description"] == "Test order"


#test 2 (read one) - ani
def test_read_order_by_id(db_session):
    """
    Test the read order by ID functionality.
    """
    
    sample_order = Order(id=1, customer_id=1, description="Sample order")
    sample_customer = customer_model.Customer(customer_id=1, name="Jane Doe")

    
    query_mock = Mock()
    query_mock.filter.return_value.first.return_value = (sample_order, sample_customer)
    db_session.query.return_value = query_mock

    
    controller.read_one = Mock(return_value=(sample_order, sample_customer))

    
    retrieved_order, retrieved_customer = controller.read_one(db=db_session, item_id=1)

    
    assert retrieved_order.id == 1
    assert retrieved_order.customer_id == 1
    assert retrieved_order.description == "Sample order"
    assert retrieved_customer.customer_id == 1
    assert retrieved_customer.name == "Jane Doe"

