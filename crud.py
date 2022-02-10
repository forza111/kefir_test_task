from sqlalchemy.orm import Session
import paginate_sqlalchemy

import models


def get_users(db: Session, page_n, size):
    users = db.query(models.UserDetail)
    page = paginate_sqlalchemy.SqlalchemyOrmPage(users, page=page_n, items_per_page=size,db_session=db)
    return {"data": page.items, "meta": {"pagination": {"total": page.page_count, "page": page_n, "size": size}}}
