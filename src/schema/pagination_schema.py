from pydantic import BaseModel

class pagination(BaseModel):
        concurrent_page: int
        items_per_page: int
        total_page: int
        total_items: int