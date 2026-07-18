"""Unit tests for REL-03: filter_local materializes file_names to a list."""

from unittest.mock import MagicMock, patch

from oeleo.workers import simple_worker


def test_filter_local_materializes_generator(db_tmp_path, local_tmp_path, external_tmp_path):
    worker = simple_worker(
        db_name=db_tmp_path,
        base_directory_from=local_tmp_path,
        base_directory_to=external_tmp_path,
    )
    paths = sorted(local_tmp_path.glob("*.xyz"))
    assert len(paths) == 2

    worker.local_connector.base_filter_sub_method = MagicMock(
        return_value=(p for p in paths)
    )

    result = worker.filter_local()
    assert isinstance(result, list)
    assert isinstance(worker.file_names, list)
    assert worker.file_names == paths

    # Consuming once must not empty file_names (generator would).
    assert list(worker.file_names) == paths
    assert list(worker.file_names) == paths


def test_double_run_after_one_filter_local(
    simple_worker_with_two_matching_and_one_not_matching,
):
    worker = simple_worker_with_two_matching_and_one_not_matching

    worker.connect_to_db()
    worker.filter_local()
    assert isinstance(worker.file_names, list)
    assert len(worker.file_names) == 2
    names = list(worker.file_names)

    worker.run()
    assert worker.file_names == names

    processed = []

    def track_chunk(chunk):
        processed.extend(chunk)
        worker.status = ("local_exists", True)
        return []

    with patch.object(worker, "_process_single_chunk", side_effect=track_chunk):
        worker.run()

    assert processed == names
    assert len(processed) == 2
