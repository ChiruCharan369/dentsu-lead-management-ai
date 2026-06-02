from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

import os
import uuid
import gc
import shutil
import time

from app.services.file_convert_service import convert_file_to_xlsx

router = APIRouter()

UPLOAD_FOLDER = "app/csv_files"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def cleanup_old_files(
    exclude_files=None
):

    if exclude_files is None:
        exclude_files = []

    gc.collect()

    for filename in os.listdir(UPLOAD_FOLDER):

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        # Skip active files
        if file_path in exclude_files:
            continue

        for _ in range(5):

            try:

                if os.path.isfile(file_path):

                    os.remove(file_path)

                elif os.path.isdir(file_path):

                    shutil.rmtree(
                        file_path,
                        ignore_errors=True
                    )

                break

            except PermissionError:

                time.sleep(1)

                gc.collect()

            except Exception as e:

                print(
                    f"Could not delete {file_path}: {e}"
                )

                break


def remove_file(path):

    try:

        gc.collect()

        time.sleep(2)

        if os.path.exists(path):

            os.remove(path)

    except Exception as e:

        print(
            f"Cleanup failed for {path}: {e}"
        )


@router.post(
    "/convert-file",
    response_class=FileResponse
)
async def convert_file(
    file: UploadFile = File(...)
):

    # =========================
    # Delete old files
    # =========================
    cleanup_old_files()

    # =========================
    # Allowed extensions
    # =========================
    allowed_extensions = [
        ".csv",
        ".xlsx",
        ".xls",
        ".xlsb"
    ]

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format"
            )
        )

    # =========================
    # Unique filenames
    # =========================
    unique_id = str(
        uuid.uuid4()
    )

    input_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}{extension}"
    )

    output_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}.xlsx"
    )

    try:

        # =========================
        # Save uploaded file
        # =========================
        with open(input_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        file.file.close()

        gc.collect()

        # =========================
        # Convert to XLSX
        # =========================
        convert_file_to_xlsx(
            input_path=input_path,
            output_path=output_path
        )

        gc.collect()

        # =========================
        # Download filename
        # Always XLSX
        # =========================
        original_name = os.path.splitext(
            os.path.basename(
                file.filename
            )
        )[0]

        download_name = (
            f"{original_name}_converted.xlsx"
        )

        # =========================
        # Return XLSX file
        # =========================
        return FileResponse(
            path=output_path,
            filename=download_name,
            media_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            background=BackgroundTask(
                lambda: (
                    remove_file(input_path),
                    remove_file(output_path)
                )
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        try:

            file.file.close()

        except:
            pass

        gc.collect()
