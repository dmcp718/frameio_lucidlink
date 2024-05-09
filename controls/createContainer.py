from time import sleep
from .appFunctions import (
    check_podman_machine_exists,
    check_container_image,
    init_and_start_machine,
    build_container,
)

def create_container(e, kv_store, mount_path, createConn_progress_ind, configCol, stream_logs_callback, update_button_states):
    try:
        init_and_start_machine(e, mount_path, createConn_progress_ind, stream_logs_callback)
        while not check_podman_machine_exists():
            sleep(1)
        build_container(e, createConn_progress_ind, stream_logs_callback)
        while not check_container_image():
            sleep(1)
        kv_store.set("connector_created", "True")
        stream_logs_callback("INFO:     Connector created successfully.")
        update_button_states()  # Call the update_button_states function
        configCol.update_connector_status()
        e.page.update()
    except Exception as e:
        stream_logs_callback(f"ERROR:    {str(e)}")