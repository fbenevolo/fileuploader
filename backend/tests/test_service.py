import pytest


@pytest.mark.asyncio
async def test_upload_file_service(file_service_fixture, file_input, file_object):
    object = await file_service_fixture.upload_file_service(file_input)
    assert object == file_object


@pytest.mark.asyncio
async def test_upload_file_service_with_failure_in_metadata(
    database_fixture, file_service_with_metadata_failure, file_input
):
    with pytest.raises(Exception) as exc_info:
        await file_service_with_metadata_failure.upload_file_service(file_input)

    # valida o rollback
    async with database_fixture.get_connection() as connection:
        cursor = await connection.execute("SELECT * FROM files")
        rows = await cursor.fetchall()
    assert rows == []

    assert str(exc_info.value) == "Metadata failure"


@pytest.mark.asyncio
async def test_upload_file_service_with_failure_in_file(
    file_service_with_file_failure, file_input
):
    with pytest.raises(Exception) as exc_info:
        await file_service_with_file_failure.upload_file_service(file_input)
    assert str(exc_info.value) == "File failure"


@pytest.mark.asyncio
async def test_list_files_metadata_service(
    populate_database_fixture, file_service_fixture, file_object
):
    objects = await file_service_fixture.list_files_metadata_service()
    assert objects[0]["original_name"] == file_object.original_name


@pytest.mark.asyncio
async def test_delete_file(file_service_fixture, file_input, database_fixture):
    uploaded_file = await file_service_fixture.upload_file_service(file_input)
    await file_service_fixture.delete_file_service(uploaded_file.stored_name)

    async with database_fixture.get_connection() as connection:
        cursor = await connection.execute("SELECT * FROM files")
        rows = await cursor.fetchall()
        assert rows == []


@pytest.mark.asyncio
async def test_delete_file_file_not_found(file_service_fixture):
    with pytest.raises(FileNotFoundError):
        await file_service_fixture.delete_file_service("somefile.txt")
