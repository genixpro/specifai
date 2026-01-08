from sqlmodel import Session

from bradstarter.items.backend.components.item_crud import create_item
from bradstarter.items.backend.data_models.item_models import Item, ItemCreate
from bradstarter.users.backend.components.user_test_utils import create_random_user
from bradstarter.general.backend.utils.test_utils import random_lower_string


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return create_item(session=db, item_in=item_in, owner_id=owner_id)
