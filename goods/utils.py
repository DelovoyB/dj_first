from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q

from goods.models import Products


def q_search(query):

    """
    Search for products by query.

    If the query is a number and less than or equal to 5 digits, search by id.
    If the query is a string, search by name and description using the PostgreSQL full text search.

    Returns a QuerySet of Products objects that match the query.

    """
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector('name', 'description')
    query = SearchQuery(query)

    result = (Products.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by('-rank'))

    result = result.annotate(headline=SearchHeadline("name", query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>'))
    result = result.annotate(bodyline=SearchHeadline("description", query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>'))

    return result

    ### search v1

    # keywords = [word for word in query.split() if len(word) > 2]
    #
    # q_objects = Q()
    #
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token) | Q(name__icontains=token)
    #
    # return Products.objects.filter(q_objects)