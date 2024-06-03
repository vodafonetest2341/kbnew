import html
from azure.ai.formrecognizer import DocumentAnalysisClient
from shared.shared import __Page__


class __DocumentAnalysisManager__:
    def parseDocument(self, blob_content, _forms_recognizer_service, credentials):

        # Create a Text Analytics client
        user_agent = "azure-functions/1.0.0"
        _model_id = "prebuilt-layout"
        with DocumentAnalysisClient(
            endpoint=_forms_recognizer_service,
            credential=credentials,
            headers={"x-ms-useragent": user_agent},
        ) as form_recognizer_client:
            poller = form_recognizer_client.begin_analyze_document(
                model_id=_model_id, document=blob_content
            )
            form_recognizer_results = poller.result()
        _results = self.get_pages(
            form_recognizer_results=form_recognizer_results,
        )
        return _results

    # toget all the pages from the results after extracting contentes from Document
    def get_pages(
        self,
        form_recognizer_results,
    ):
        offset = 0
        _pages = []
        for page_num, page in enumerate(form_recognizer_results.pages):
            tables_on_page = [
                table
                for table in (form_recognizer_results.tables or [])
                if table.bounding_regions
                and table.bounding_regions[0].page_number == page_num + 1
            ]

            # mark all positions of the table spans in the page
            page_offset = page.spans[0].offset
            page_length = page.spans[0].length
            table_chars = [-1] * page_length
            for table_id, table in enumerate(tables_on_page):
                for span in table.spans:
                    # replace all table spans with "table_id" in table_chars array
                    for i in range(span.length):
                        idx = span.offset - page_offset + i
                        if idx >= 0 and idx < page_length:
                            table_chars[idx] = table_id

            # build page text by replacing characters in table spans with table html
            page_text = ""
            added_tables = set()
            for idx, table_id in enumerate(table_chars):
                if table_id == -1:
                    page_text += form_recognizer_results.content[page_offset + idx]
                elif table_id not in added_tables:
                    page_text += __DocumentAnalysisManager__.table_to_html(
                        tables_on_page[table_id]
                    )
                    added_tables.add(table_id)

            _page = __Page__(
                page_num=page_num,
                offset=offset,
                text=page_text,
            )
            _pages.append(_page)
            offset += len(page_text)
        return _pages

    @classmethod
    def table_to_html(cls, table):
        # convert table data to HTML tages
        table_html = "<table>"
        rows = [
            sorted(
                [cell for cell in table.cells if cell.row_index == i],
                key=lambda cell: cell.column_index,
            )
            for i in range(table.row_count)
        ]
        for row_cells in rows:
            table_html += "<tr>"
            for cell in row_cells:
                tag = (
                    "th"
                    if (cell.kind == "columnHeader" or cell.kind == "rowHeader")
                    else "td"
                )
                cell_spans = ""
                if cell.column_span is not None and cell.column_span > 1:
                    cell_spans += f" colSpan={cell.column_span}"
                if cell.row_span is not None and cell.row_span > 1:
                    cell_spans += f" rowSpan={cell.row_span}"
                table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
            table_html += "</tr>"
        table_html += "</table>"
        return table_html
