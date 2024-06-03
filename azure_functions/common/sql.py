import pyodbc
import struct
from azure.identity import DefaultAzureCredential


class __SqlConnector__:
    def __init__(
        self,
        sql_server,
        sql_database,
    ):
        _connection_string = (
            "Driver={ODBC Driver 17 for SQL Server};SERVER="
            + sql_server
            + ".database.windows.net;DATABASE="
            + sql_database
        )
        self.connection_string = _connection_string

    def _get_access_token(self):
        _scope = "https://database.windows.net/.default"
        _credential = DefaultAzureCredential()
        _access_token = _credential.get_token(_scope)
        return _access_token

    def _get_token_struct(self):

        _access_token = self._get_access_token()
        _tokenb = bytes(_access_token.token, "UTF-8")
        _exptoken = b""
        for i in _tokenb:
            _exptoken += bytes({i})
            _exptoken += bytes(1)
        _tokenstruct = struct.pack("=i", len(_exptoken)) + _exptoken
        return _tokenstruct

    def get_sql_connection(self):

        _tokenstruct = self._get_token_struct()
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        _connection = pyodbc.connect(
            self.connection_string,
            attrs_before={SQL_COPT_SS_ACCESS_TOKEN: _tokenstruct},
        )
        return _connection
