import pandas as pd
from openpyxl import load_workbook
import os
import gc


def convert_file_to_xlsx(
    input_path: str,
    output_path: str
):

    extension = os.path.splitext(
        input_path
    )[1].lower()

    # =========================
    # CSV -> XLSX
    # =========================
    if extension == ".csv":

        df = pd.read_csv(
            input_path,
            dtype=str
        )

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Sheet1"
            )

    # =========================
    # XLSX -> CLEAN XLSX
    # =========================
    elif extension == ".xlsx":

        workbook = load_workbook(
            filename=input_path,
            data_only=True
        )

        try:

            with pd.ExcelWriter(
                output_path,
                engine="openpyxl"
            ) as writer:

                for ws in workbook.worksheets:

                    # Skip hidden sheets
                    if ws.sheet_state != "visible":
                        continue

                    data = list(ws.values)

                    if not data:
                        continue

                    headers = data[0]

                    df = pd.DataFrame(
                        data[1:],
                        columns=headers
                    )

                    clean_sheet_name = str(
                        ws.title
                    )[:31]

                    df.to_excel(
                        writer,
                        sheet_name=clean_sheet_name,
                        index=False
                    )

        finally:

            workbook.close()

    # =========================
    # XLS -> XLSX
    # =========================
    elif extension == ".xls":

        excel_data = pd.read_excel(
            input_path,
            sheet_name=None,
            engine="xlrd"
        )

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl"
        ) as writer:

            for sheet_name, df in excel_data.items():

                clean_sheet_name = str(
                    sheet_name
                )[:31]

                df.to_excel(
                    writer,
                    sheet_name=clean_sheet_name,
                    index=False
                )

    # =========================
    # XLSB -> XLSX
    # Skip hidden/helper sheets
    # =========================
    elif extension == ".xlsb":

        excel_file = None

        try:

            excel_file = pd.ExcelFile(
                input_path,
                engine="pyxlsb"
            )

            with pd.ExcelWriter(
                output_path,
                engine="openpyxl"
            ) as writer:

                for sheet_name in excel_file.sheet_names:

                    try:

                        lower_sheet = (
                            str(sheet_name)
                            .lower()
                            .strip()
                        )

                        # =========================
                        # Skip hidden/helper sheets
                        # =========================
                        skip_keywords = [
                            "_xlnm",
                            "filterdatabase",
                            "pivot",
                            "cache",
                            "helper",
                            "lookup",
                            "temp",
                            "hidden",
                            "print_area",
                            "print_titles"
                        ]

                        if (
                            str(sheet_name).startswith("_")
                            or any(
                                keyword in lower_sheet
                                for keyword in skip_keywords
                            )
                        ):

                            print(
                                f"Skipping hidden/helper sheet: {sheet_name}"
                            )

                            continue

                        print(
                            f"Reading visible sheet: {sheet_name}"
                        )

                        df = pd.read_excel(
                            input_path,
                            sheet_name=sheet_name,
                            engine="pyxlsb"
                        )

                        # Skip empty sheets
                        if df.empty:
                            continue

                        clean_sheet_name = str(
                            sheet_name
                        )[:31]

                        df.to_excel(
                            writer,
                            sheet_name=clean_sheet_name,
                            index=False
                        )

                        del df

                        gc.collect()

                    except Exception as e:

                        print(
                            f"Skipping sheet {sheet_name}: {e}"
                        )

        finally:

            try:

                if excel_file is not None:
                    excel_file.close()

            except:
                pass

            gc.collect()

# import os
# import gc
# import shutil
# import pandas as pd
# from openpyxl import load_workbook

# import pythoncom
# import win32com.client as win32


# def convert_xlsb_using_excel(
#     input_path: str,
#     output_path: str
# ):

#     pythoncom.CoInitialize()

#     excel = win32.DispatchEx("Excel.Application")

#     excel.Visible = False
#     excel.DisplayAlerts = False

#     try:

#         workbook = excel.Workbooks.Open(
#             os.path.abspath(input_path)
#         )

#         workbook.SaveAs(
#             os.path.abspath(output_path),
#             FileFormat=51  # XLSX
#         )

#         workbook.Close(False)

#     finally:

#         excel.Quit()
#         pythoncom.CoUninitialize()


# def remove_hidden_sheets(
#     xlsx_path: str
# ):

#     wb = load_workbook(
#         xlsx_path
#     )

#     try:

#         hidden_sheets = []

#         for ws in wb.worksheets:

#             if ws.sheet_state != "visible":

#                 hidden_sheets.append(
#                     ws.title
#                 )

#         for sheet_name in hidden_sheets:

#             del wb[sheet_name]

#         wb.save(
#             xlsx_path
#         )

#     finally:

#         wb.close()


# def convert_file_to_xlsx(
#     input_path: str,
#     output_path: str
# ):

#     extension = os.path.splitext(
#         input_path
#     )[1].lower()

#     # =====================================
#     # CSV -> XLSX
#     # =====================================
#     if extension == ".csv":

#         df = pd.read_csv(
#             input_path,
#             dtype=str,
#             encoding="utf-8-sig"
#         ).fillna("")

#         with pd.ExcelWriter(
#             output_path,
#             engine="openpyxl"
#         ) as writer:

#             df.to_excel(
#                 writer,
#                 index=False,
#                 sheet_name="Sheet1"
#             )

#     # =====================================
#     # XLSX -> XLSX
#     # Remove hidden sheets only
#     # Preserve formatting
#     # =====================================
#     elif extension == ".xlsx":

#         shutil.copy2(
#             input_path,
#             output_path
#         )

#         remove_hidden_sheets(
#             output_path
#         )

#     # =====================================
#     # XLS -> XLSX
#     # =====================================
#     elif extension == ".xls":

#         excel_data = pd.read_excel(
#             input_path,
#             sheet_name=None,
#             engine="xlrd"
#         )

#         with pd.ExcelWriter(
#             output_path,
#             engine="openpyxl"
#         ) as writer:

#             for sheet_name, df in excel_data.items():

#                 df.to_excel(
#                     writer,
#                     sheet_name=str(sheet_name)[:31],
#                     index=False
#                 )

#     # =====================================
#     # XLSB -> XLSX
#     # Use Excel application itself
#     # Preserves currency formatting
#     # =====================================
#     elif extension == ".xlsb":

#         import pythoncom
#         import win32com.client as win32
#         from openpyxl import Workbook

#         pythoncom.CoInitialize()

#         excel = win32.DispatchEx("Excel.Application")

#         excel.Visible = False
#         excel.DisplayAlerts = False

#         try:

#             wb_source = excel.Workbooks.Open(
#                 os.path.abspath(input_path)
#             )

#             wb_target = Workbook()

#             wb_target.remove(
#                 wb_target.active
#             )

#             for sheet in wb_source.Worksheets:

#                 # Visible sheets only
#                 if sheet.Visible != -1:
#                     continue

#                 ws_target = wb_target.create_sheet(
#                     title=str(sheet.Name)[:31]
#                 )

#                 used_range = sheet.UsedRange

#                 rows = used_range.Rows.Count
#                 cols = used_range.Columns.Count

#                 for r in range(1, rows + 1):

#                     row_data = []

#                     for c in range(1, cols + 1):

#                         try:

#                             cell = sheet.Cells(r, c)

#                             # IMPORTANT
#                             # Read displayed text
#                             value = cell.Text

#                         except:

#                             value = ""

#                         row_data.append(value)

#                     ws_target.append(
#                         row_data
#                     )

#             wb_target.save(
#                 output_path
#             )

#             wb_source.Close(False)

#         finally:

#             excel.Quit()

#             pythoncom.CoUninitialize()
#############################################################################################################################################################################################
# import os
# import gc
# import shutil
# import pandas as pd
# from openpyxl import Workbook, load_workbook

# import pythoncom
# import win32com.client as win32


# def convert_xlsb_using_excel(
#     input_path: str,
#     output_path: str
# ):

#     pythoncom.CoInitialize()

#     excel = win32.DispatchEx("Excel.Application")

#     excel.Visible = False
#     excel.DisplayAlerts = False

#     try:

#         source_wb = excel.Workbooks.Open(
#             os.path.abspath(input_path)
#         )

#         target_wb = Workbook()

#         target_wb.remove(
#             target_wb.active
#         )

#         for sheet in source_wb.Worksheets:

#             try:

#                 # Visible sheets only
#                 if sheet.Visible != -1:
#                     continue

#                 print(
#                     f"Processing sheet: {sheet.Name}"
#                 )

#                 target_ws = target_wb.create_sheet(
#                     title=str(sheet.Name)[:31]
#                 )

#                 used_range = sheet.UsedRange

#                 rows = used_range.Rows.Count
#                 cols = used_range.Columns.Count

#                 for r in range(1, rows + 1):

#                     row_data = []

#                     for c in range(1, cols + 1):

#                         try:

#                             value = sheet.Cells(
#                                 r,
#                                 c
#                             ).Text

#                             if value in [
#                                 "#N/A",
#                                 "#DIV/0!",
#                                 "#REF!",
#                                 "#VALUE!",
#                                 "#NAME?",
#                                 "#NUM!"
#                             ]:
#                                 value = ""

#                         except Exception:

#                             value = ""

#                         row_data.append(
#                             value
#                         )

#                     target_ws.append(
#                         row_data
#                     )

#             except Exception as e:

#                 print(
#                     f"Skipping sheet {sheet.Name}: {e}"
#                 )

#                 continue

#         target_wb.save(
#             output_path
#         )

#         source_wb.Close(False)

#     finally:

#         excel.Quit()

#         pythoncom.CoUninitialize()

#         gc.collect()


# def remove_hidden_sheets(
#     xlsx_path: str
# ):

#     wb = load_workbook(
#         xlsx_path
#     )

#     try:

#         hidden_sheets = []

#         for ws in wb.worksheets:

#             if ws.sheet_state != "visible":

#                 hidden_sheets.append(
#                     ws.title
#                 )

#         for sheet_name in hidden_sheets:

#             del wb[sheet_name]

#         wb.save(
#             xlsx_path
#         )

#     finally:

#         wb.close()


# def convert_file_to_xlsx(
#     input_path: str,
#     output_path: str
# ):

#     extension = os.path.splitext(
#         input_path
#     )[1].lower()

#     # =====================================
#     # CSV -> XLSX
#     # =====================================
#     if extension == ".csv":

#         df = pd.read_csv(
#             input_path,
#             dtype=str,
#             encoding="utf-8-sig"
#         ).fillna("")

#         with pd.ExcelWriter(
#             output_path,
#             engine="openpyxl"
#         ) as writer:

#             df.to_excel(
#                 writer,
#                 index=False,
#                 sheet_name="Sheet1"
#             )

#     # =====================================
#     # XLSX -> XLSX
#     # Visible sheets only
#     # Values only
#     # =====================================
#     elif extension == ".xlsx":

#         source_wb = load_workbook(
#             input_path,
#             data_only=True
#         )

#         target_wb = Workbook()

#         target_wb.remove(
#             target_wb.active
#         )

#         try:

#             for ws in source_wb.worksheets:

#                 try:

#                     if ws.sheet_state != "visible":
#                         continue

#                     target_ws = target_wb.create_sheet(
#                         title=str(ws.title)[:31]
#                     )

#                     for row in ws.iter_rows(
#                         values_only=True
#                     ):

#                         target_ws.append([
#                             "" if v is None else str(v)
#                             for v in row
#                         ])

#                 except Exception as e:

#                     print(
#                         f"Skipping sheet {ws.title}: {e}"
#                     )

#             target_wb.save(
#                 output_path
#             )

#         finally:

#             source_wb.close()

#     # =====================================
#     # XLS -> XLSX
#     # =====================================
#     elif extension == ".xls":

#         excel_data = pd.read_excel(
#             input_path,
#             sheet_name=None,
#             engine="xlrd",
#             dtype=str
#         )

#         with pd.ExcelWriter(
#             output_path,
#             engine="openpyxl"
#         ) as writer:

#             for sheet_name, df in excel_data.items():

#                 try:

#                     df.fillna(
#                         "",
#                         inplace=True
#                     )

#                     df.to_excel(
#                         writer,
#                         sheet_name=str(sheet_name)[:31],
#                         index=False
#                     )

#                 except Exception as e:

#                     print(
#                         f"Skipping sheet {sheet_name}: {e}"
#                     )

#     # =====================================
#     # XLSB -> XLSX
#     # Preserve displayed text
#     # =====================================
#     elif extension == ".xlsb":

#         convert_xlsb_using_excel(
#             input_path=input_path,
#             output_path=output_path
#         )

#     else:

#         raise ValueError(
#             f"Unsupported file type: {extension}"
#         )

#     gc.collect()