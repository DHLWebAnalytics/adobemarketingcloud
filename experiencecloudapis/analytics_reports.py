import typing
import pandas
import json
import requests
from copy import deepcopy
from .analytics import Analytics, ResponseError
from experiencecloudapis.authentication import AuthenticationClient


class ColumnsMissmatchError(Exception):
    """Raised if custom column names Sequence does not match payload columns"""
    pass


class NoDataRequestedError(Exception):
    """Raised if no data has been requested yet"""
    pass


class Table:
    """This class serves as an abstraction layer for the received data from
    the /reports endpoint. Received data will be modelled in this 2-d like
    table and can later be transformed into more advanced data models,
    ie pandas.Dataframe or alike.
    """

    def __init__(self,
                 analytics_client: Analytics,
                 column_names: typing.Union[
                     typing.Sequence[str], None] = None) -> None:
        self.analytics_client = analytics_client
        self.column_names = column_names
        self.columns: typing.List[str] = []
        self.rows: typing.List[
            typing.Tuple[str, typing.List[typing.Union[int, float]]]] = []
        self.dimension: str = ""

    def _expand_global_segment(self, global_filters: typing.List[dict]) -> str:
        """
        Creates a nested string of global segments applied and adds it to
        the column name of each metric.

        :param global_filters: globalFilters dict from Adobe Reports API
        response
        :return: concatenated global segments string
        """
        # global_segments serves as the collector of all global segment filter
        global_segments: typing.List[str] = []
        for filter in global_filters:
            # globalFilters can have dateRange or dimensions in the array:
            # If the item is of type segment and has a segmentId, then we can
            # use the id and resolve it to a descriptive name via Adobe API.
            # Other types are dateRanges or dimensions. We skip dateRanges, as
            # the date should be known to the consumer. Dimensions on the other
            # hand live in a special 'segmentDefinition' object which needs to
            # be resolved into a descriptive name.
            if filter['type'] == 'segment':
                if 'segmentId' in filter:
                    filter_name = filter['segmentId']
                    if filter_name.startswith('s1214'):
                        try:
                            response = self.analytics_client.get_segment(
                                filter['segmentId'])
                            filter_name = response.json()['name']
                        except ResponseError:
                            pass
                elif 'segmentDefinition' in filter:
                    try:
                        filter_name = \
                            f"{filter['segmentDefinition']['container']['pred']['description']}" \
                            f"[{filter['segmentDefinition']['container']['pred']['str']}]" # noqa
                    # if the above drill fails, then unknown to rescue
                    except KeyError:
                        filter_name = 'unknown'
                # if neither segmentId nor segmentDefinition are available,
                # then unknown is the last resort
                else:
                    filter_name = 'unknown'
                global_segments.append(filter_name)
        return f'[{"][".join(global_segments)}]' \
            if len(global_segments) else ''

    def _create_metric_filters_dict(self, metric_filters: dict) -> dict:
        """
        Helper that resolves the metricContainer.metricFilters list into a
        dict for quicker lookups

        :return: dict of metricFilters
        """
        mapping = {}
        for filter in metric_filters:
            # a filter type can be any of {breakdown, dateRange, segment}
            # while a segment can be resolved via API and dateRange is
            # straighforward, I couldnt find a way to resolve a breakdown
            # value into something useful for a label. Therefore the dimension
            # and id are provided
            filter_type = filter['type']
            filter_id = filter['id']
            label: str
            if filter_type == 'breakdown':
                dimension = filter['dimension'].replace('variables/', '') if \
                    filter['dimension'].startswith('variables/') else \
                    filter['dimension']
                if 'itemId' in filter:
                    dimension = f"{dimension}[{filter['itemId']}]"
                label = dimension
            elif filter_type == 'segment':
                if filter['segmentId'].startswith('s1214'):
                    try:
                        response = \
                            self.analytics_client.get_segment(
                                filter['segmentId'])
                        label = response.json()['name']
                    except ResponseError:
                        label = 'unknown'
                else:
                    label = filter['segmentId']
            elif filter_type == 'dateRange':
                label = filter['dateRange']
            # last resort unknown
            else:
                label = 'unknown'
            mapping[filter_id] = label
        return mapping

    def _expand_column_names(self, payload: dict) -> typing.List[str]:
        """
        Creates a list of column labels for the table. Each column name
        provides the metric name and any
        global or metric filters that are applied.

        :param payload: Full payload from Adobe Report API
        :return: list of column names concatenated with global and column
        filter information
        """
        # this list serves as the bucket for all column names
        columns = []
        # retrieves the global filters string, that is appended to each column
        global_segment_string = self._expand_global_segment(
            payload['globalFilters'])
        # metrics might be available multiple times per report. In order not
        # to request the same information multiple times, this dummy dict
        # cache will remember previously resolved metric descriptions
        dummy_cache = {}
        # create the filter to label mapping
        metric_filter_map = {}
        if 'metricFilters' in payload['metricContainer']:
            metric_filter_map = self._create_metric_filters_dict(
                payload['metricContainer']['metricFilters'])
        # each metric in the metricContainer of the Adobe Report API
        # response is looped and resolved
        for metric in payload['metricContainer']['metrics']:
            # metric.id can have various forms:
            # 1) default metric, starting with 'metrics/'
            # 2) custom metric, staring with 'cm'
            # custom metric id's are not very helpful for the consumer,
            # this is why each one is resolved via
            # Adobe API into the descriptive name before added to the columns
            # list
            metric_name: str = metric['id']
            # quick check if the metric hasn't be processed before. If so,
            # the cache is used
            if metric_name not in dummy_cache:
                # standard metric, the id can be used as column label.
                # We remove the prefix before adding
                if metric_name.startswith('metrics'):
                    metric_name = metric_name.split("/")[1]
                # a custom metric is detected and will be resolved via
                # Adobe API
                elif metric_name.startswith('cm'):
                    try:
                        response = self.analytics_client.get_calculatedmetric(
                            metric_name)
                        metric_name = response.json()['name']
                    except ResponseError:
                        metric_name = 'unknown'
                # last resort unknown
                else:
                    metric_name = 'unknown'
                dummy_cache[metric['id']] = metric_name
            else:
                metric_name = dummy_cache[metric['id']]

            # add global filters to the metric_name
            metric_name += global_segment_string

            # each metric can have a corresponding additional metric filter
            # attached that only applies to itself the filters list is
            # traversed and resolved into the metric label
            if 'filters' in metric:
                # traverse all metrics with individual filters and resolve to
                # a descriptive label
                for filter_id in metric['filters']:
                    metric_name = \
                        f'{metric_name}[{metric_filter_map[filter_id]}]'
            columns.append(metric_name)
        return columns

    def process_response(self, chunk: dict) -> None:
        """
        This function consumes Adobe Report API response chunks and appends
        it to the table data.
        If no rows are available in the dict, then the summary numbers are
        taken as this will indicate that no breakdown has been applied to
        the data request.

        :param chunk: Adobe Reporting Response Chunk
        :return: None
        """
        if 'rows' in chunk:
            rows = [(row['value'], row['data']) for row in chunk['rows']]
            if not getattr(self, 'rows', None):
                self.rows = rows
            else:
                self.rows += rows
        else:
            self.rows = [("Total", chunk['summaryData']['totals'])]
        if 'dimension' in chunk['columns']:
            self.dimension = chunk['columns']['dimension']['id']
        else:
            self.dimension = 'Summary'

    def process_payload(self, payload: typing.Union[str, dict]) -> None:
        """
        This function processes the payload object and configures the columns
        for the table response. Not all information can be extracted from the
        Adobe Report API Response, therefore this step is necessary in order
        to generate useful descriptive information for the column names.

        :param payload: Adobe Reporting Request Payload
        :return: None
        """
        if isinstance(payload, str):
            payload = json.loads(payload)
        self.columns = self.column_names if self.column_names else \
            self._expand_column_names(payload)

    def __repr__(self):
        return f'<Table {self.columns}>'


class Reports:
    def __init__(self,
                 auth_client: AuthenticationClient,
                 session: requests.Session = requests.Session()) -> None:
        self.analytics_client = Analytics(auth_client, session)
        self.table_data = None

    @staticmethod
    def _update_page_settings(payload: dict) -> dict:
        """
        Response data for the Adobe Report API contains a lastPage flag which
        indicates that all data has been requested. In order to retrieve the
        next page if data is not fully requested, the page property
        of the payload object has to be incremented in the payload.
        This function increments payloads settings.page value by one if not
        last page.

        :param payload: Adobe Report API payload data
        :return: settings dict of the payload request object
        """
        updated_dict = deepcopy(payload)
        if 'settings' not in updated_dict:
            updated_dict['settings'] = {}
        if 'page' not in updated_dict['settings']:
            updated_dict['settings']['page'] = 0
        updated_dict['settings']['page'] += 1
        return updated_dict

    def _get(self, payload: typing.Union[str, dict]) -> \
            typing.Generator[dict, None, None]:
        """Requests the /report endpoint with the payload provided"""
        if isinstance(payload, str):
            payload = json.loads(payload)
        while True:
            response = self.analytics_client.reports(payload)
            response_dict = response.json()
            self.__class__._update_page_settings(payload)
            yield response_dict
            # lastPage indicates the last response chunk
            # break the loop if this flag is set in the response
            if response_dict['lastPage']:
                break

    def _create_table(self,
                      payload: typing.Union[str, dict],
                      all_pages: bool,
                      column_names: typing.Union[
                          typing.Sequence[str], None] = None) -> Table:
        """Creates a new intermediate table format Table"""
        table = Table(self.analytics_client, column_names)
        table.process_payload(payload)
        for chunk in self._get(payload):
            table.process_response(chunk)
            if not all_pages:
                break
        return table

    def request_report(self,
                       payload: typing.Union[str, dict],
                       all_pages: bool = True,
                       column_names: typing.Union[
                           typing.Sequence[str], None] = None) -> 'Reports':
        """
        Requests the Adobe Analytics /reports endpoint with the provided
        payload data.
        If 'all_pages' is set to False, only the first page will be requested.
        Otherwise this method will continue requesting following pages until
        the lastPage flag is set


        :param payload: payload json data from Adobe Debugger
        :param all_pages: request complete data if set to true, otherwise
        only the first page is requested
        :param column_names: automatic column resolution is skipped if
        custom column names are specified here
        :return: self
        """
        if isinstance(payload, str):
            payload = json.loads(payload)
        # custom column names must match the metricsContainer metrics length !
        if column_names:
            if len(payload['metricContainer']['metrics']) != len(column_names):
                raise ColumnsMissmatchError(
                    'Payload columns is {current_len} '
                    'but {requested_len} was provided. '
                    'Please check your input.'.format(
                        current_len=len(payload["metricContainer"]["metrics"]),
                        requested_len=len(column_names)
                    )
                )
        self.table_data = self._create_table(payload, all_pages, column_names)
        return self

    def to_table(self) -> Table:
        """
        Returns the resolved Table object

        :return: Table
        """
        return self.table_data

    def to_dataframe(self) -> pandas.DataFrame:
        """
        Returns a pandas.DataFrame object representation of the Report

        :return: padas.DataFrame representation of Table data
        """
        if not self.table_data:
            raise NoDataRequestedError(
                "You must first request data with '{}.{}'".format(
                    self.__class__.__name__,
                    'request_report'
                )
            )
        data = [row[1] for row in self.table_data.rows]
        index = [row[0] for row in self.table_data.rows]
        columns = self.table_data.columns
        return pandas.DataFrame(data, columns=columns, index=index)

    def to_csv(self, **kwargs) -> str:
        """
        Returns table data as csv

        :param kwargs: Parameters as described in pandas.DataFrame.to_csv
        :return: data as csv compliant string
        """
        return self.to_dataframe().to_csv(**kwargs)

    def to_json(self, **kwargs) -> str:
        """
        Returns table data as json string

        :param kwargs: Parameters as described in pandas.DataFrame.to_json
        :return: data as json string
        """
        return self.to_dataframe().to_json(**kwargs)

    def to_dict(self, **kwargs) -> dict:
        """
        Returns table data as dict

        :param kwargs: Parameters as described in pandas.DataFrame.to_json
        :return: data as dict
        """
        return json.loads(self.to_json(**kwargs))
