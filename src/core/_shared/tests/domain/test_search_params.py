from unittest import TestCase

from src.core._shared.domain.search_params import SearchParams


class TestSearchParams(TestCase):
    def test_should_be_able_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {"page": None, "expected": 1},
            {"page": "", "expected": 1},
            {"page": "fake", "expected": 1},
            {"page": 0, "expected": 1},
            {"page": -1, "expected": 1},
            {"page": "0", "expected": 1},
            {"page": "-1", "expected": 1},
            {"page": 5.5, "expected": 5},
            {"page": True, "expected": 1},
            {"page": False, "expected": 1},
            {"page": {}, "expected": 1},
            {"page": 1, "expected": 1},
            {"page": 2, "expected": 2},
        ]

        for i in arrange:
            params = SearchParams(page=i["page"])
            self.assertEqual(params.page, i["expected"])

    def test_should_be_able_to_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {"per_page": None, "expected": 15},
            {"per_page": "", "expected": 15},
            {"per_page": "fake", "expected": 15},
            {"per_page": 0, "expected": 15},
            {"per_page": -1, "expected": 15},
            {"per_page": "0", "expected": 15},
            {"per_page": "-1", "expected": 15},
            {"per_page": 5.5, "expected": 5},
            {"per_page": True, "expected": 1},
            {"per_page": False, "expected": 15},
            {"per_page": {}, "expected": 15},
            {"per_page": 1, "expected": 1},
            {"per_page": 2, "expected": 2},
        ]

        for i in arrange:
            params = SearchParams(per_page=i["per_page"])
            self.assertEqual(params.per_page, i["expected"], i)

    def test_should_be_able_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {"sort": None, "expected": None},
            {"sort": "", "expected": None},
            {"sort": "fake", "expected": "fake"},
            {"sort": 0, "expected": "0"},
            {"sort": -1, "expected": "-1"},
            {"sort": "0", "expected": "0"},
            {"sort": "-1", "expected": "-1"},
            {"sort": 5.5, "expected": "5.5"},
            {"sort": True, "expected": "True"},
            {"sort": False, "expected": "False"},
            {"sort": {}, "expected": "{}"},
        ]

        for i in arrange:
            params = SearchParams(sort=i["sort"])
            self.assertEqual(params.sort, i["expected"], i)

    def test_should_be_able_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort="")
        self.assertIsNone(params.sort_dir)

        arrange = [
            {"sort_dir": None, "expected": "asc"},
            {"sort_dir": "", "expected": "asc"},
            {"sort_dir": "fake", "expected": "asc"},
            {"sort_dir": 0, "expected": "asc"},
            {"sort_dir": {}, "expected": "asc"},
            {"sort_dir": "asc", "expected": "asc"},
            {"sort_dir": "ASC", "expected": "asc"},
            {"sort_dir": "desc", "expected": "desc"},
            {"sort_dir": "DESC", "expected": "desc"},
        ]

        for i in arrange:
            params = SearchParams(sort="name", sort_dir=i["sort_dir"])
            self.assertEqual(params.sort_dir, i["expected"], i)

    def test_should_be_able_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {"filter": None, "expected": None},
            {"filter": "", "expected": None},
            {"filter": "fake", "expected": "fake"},
            {"filter": 0, "expected": "0"},
            {"filter": -1, "expected": "-1"},
            {"filter": "0", "expected": "0"},
            {"filter": "-1", "expected": "-1"},
            {"filter": 5.5, "expected": "5.5"},
            {"filter": True, "expected": "True"},
            {"filter": False, "expected": "False"},
            {"filter": {}, "expected": "{}"},
        ]

        for i in arrange:
            params = SearchParams(filter=i["filter"])
            self.assertEqual(params.filter, i["expected"], i)
