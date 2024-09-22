from src.core._shared.domain.repositories.search_result import SearchResult


class TestSearchResult:

    def test_last_page_calculation(self):
        items = [1, 2, 3, 4, 5]
        total = 17
        current_page = 2
        per_page = 5
        search_result = SearchResult[int](
            items=items, total=total, current_page=current_page, per_page=per_page
        )
        assert search_result.last_page == 4

        items = [1, 2, 3, 4, 5]
        total = 15
        current_page = 3
        per_page = 5
        search_result = SearchResult[int](
            items=items, total=total, current_page=current_page, per_page=per_page
        )
        assert search_result.last_page == 3

        items = [1, 2, 3, 4, 5]
        total = 5
        current_page = 1
        per_page = 5
        search_result = SearchResult[int](
            items=items, total=total, current_page=current_page, per_page=per_page
        )
        assert search_result.last_page == 1

        items = [1, 2, 3, 4, 5]
        total = 0
        current_page = 1
        per_page = 5
        search_result = SearchResult[int](
            items=items, total=total, current_page=current_page, per_page=per_page
        )
        assert search_result.last_page == 0

        items = []
        total = 0
        current_page = 1
        per_page = 5
        search_result = SearchResult[int](
            items=items, total=total, current_page=current_page, per_page=per_page
        )
        assert search_result.last_page == 0
