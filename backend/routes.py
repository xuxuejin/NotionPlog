from flask import Blueprint, jsonify, request, current_app
from notion_client import APIResponseError, APIErrorCode
from .notion_utils import query_database, query_page

bp = Blueprint('notion', __name__, url_prefix='/notion/v1')

PAGE_SIZE = 100

@bp.route('/pages', methods=['GET'])
@bp.route('/pages/<page_id>', methods=['GET'])
@bp.route('/databases/<int:database_id>/pages', methods=['GET'])
def notion_pages(database_id=None, page_id=None):
    results_list = None

    if not page_id:
        results_list = get_all_pages(database_id)
    else:
        results_list = get_page_by_id(page_id)

    return results_list


def get_all_pages(database_id):
    results_list = []

    if database_id:
        query_data = {"database_id": database_id, "page_size": PAGE_SIZE}
    else:
        query_data = {"database_id": current_app.config["DATABASE_ID"], "page_size": PAGE_SIZE}

    while True:
        try:
            query_result = query_database(query_data)

            results = query_result.get('results', [])
            if results:
                results_list.extend(results)
                if not query_result.get("has_more", False):
                    break

                if query_result.get("next_cursor"):
                    query_data = {
                        "database_id": database_id or current_app.config["DATABASE_ID"],
                        "start_cursor": query_result.get("next_cursor"),
                        "page_size": PAGE_SIZE
                    }
        except APIResponseError as error:
            if error.code == APIErrorCode.ObjectNotFound:
                print(error)
            else:
                print(error)
            return []

    return results_list


def get_page_by_id(page_id):
    return query_page(page_id)
