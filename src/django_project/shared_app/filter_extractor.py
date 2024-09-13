from typing import Dict


class FilterExtractor:
    @staticmethod
    def extract_filters(query_params: Dict[str, str]) -> Dict[str, str]:
        filters = {}
        keys_to_remove = []

        for key, value in query_params.items():
            if key.startswith("filter[") and key.endswith("]"):
                filter_key = key[len("filter[") : -1]
                filters[filter_key] = value
                keys_to_remove.append(key)

        for key in keys_to_remove:
            query_params.pop(key)

        return filters
