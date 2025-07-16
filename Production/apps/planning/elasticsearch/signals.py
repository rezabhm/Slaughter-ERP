# apps/planning/elasticsearch/signals.py

from mongoengine import signals
from apps.planning.documents import PlanningSeries, PlanningSeriesCell
from apps.planning.elasticsearch.utils import (
    index_planning_series,
    delete_planning_series,
    index_planning_series_cell,
    delete_planning_series_cell,
)
from apps.planning.serializers import (
    PlanningSeriesSerializer,
    PlanningSeriesCellSerializer,
)


@signals.post_save.connect
def index_planning_series_on_save(sender, document, **kwargs):
    """
    Signal to index a PlanningSeries document when it's saved.
    """
    if isinstance(document, PlanningSeries):
        data = PlanningSeriesSerializer(document).data
        index_planning_series(data)


@signals.post_delete.connect
def delete_planning_series_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PlanningSeries document from the index when it's deleted.
    """
    if isinstance(document, PlanningSeries):
        delete_planning_series(str(document.id))


@signals.post_save.connect
def index_planning_series_cell_on_save(sender, document, **kwargs):
    """
    Signal to index a PlanningSeriesCell document when it's saved.
    """
    if isinstance(document, PlanningSeriesCell):
        data = PlanningSeriesCellSerializer(document).data
        index_planning_series_cell(data)


@signals.post_delete.connect
def delete_planning_series_cell_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PlanningSeriesCell document from the index when it's deleted.
    """
    if isinstance(document, PlanningSeriesCell):
        delete_planning_series_cell(str(document.id))
