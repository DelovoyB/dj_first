from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

from goods.models import Products


def q_search(query):
    """
    Search for products by query.

    If the query is a number and less than or equal to 5 digits, search by id.
    If the query is a string, search by name and description using the PostgreSQL full text search.

    Returns a QuerySet of Products objects that match the query.
    """
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query)).select_related('category')

    vector = SearchVector('name', 'description')
    query = SearchQuery(query)

    result = (Products.objects.annotate(rank=SearchRank(vector, query))
              .filter(rank__gt=0)
              .order_by('-rank')
              .select_related('category'))

    return result
