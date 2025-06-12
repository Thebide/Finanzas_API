from pydantic import BaseModel

class Pagination(BaseModel):
        concurrent_page: int
        items_per_page: int
        total_pages: int
        total_items: int