import flet as ft
import subprocess
import os
import shutil
from .KeyValueStore import KeyValueStore

log_thread = None

headingColor = ft.colors.DEEP_PURPLE_300
bodyColor = ft.colors.with_opacity(1, color=ft.colors.GREY_200)
logoColor = "#b3fb1e"
fontSizeVal = 12

userPath = os.path.expanduser("~")
dir_path = userPath + "/.lucidlinkFrameIOapp"
db_file_path = f"{dir_path}/app.db"

kv_store = KeyValueStore()

filepath = kv_store.get("filepath")
mount_path = kv_store.get("save_path")
portVal = kv_store.get("port")

# use the value of the key "connector_name" to set the container name
container_name = kv_store.get("connector_name")


def check_podman_installed():
    return os.path.exists("/opt/podman/bin/podman")

def check_container_image():
    podman_path = shutil.which("podman")
    if not podman_path:
        return False

    connector_created = kv_store.get("connector_created")
    print("connector_created: ", connector_created)
    if connector_created:
        return True
    else:
        return False

def check_podman_machine_exists():
    try:
        result = subprocess.run(
            ["/opt/podman/bin/podman", "machine", "list"],
            capture_output=True,
            text=True,
        )
        return "podman-machine-default" in result.stdout
    except FileNotFoundError:
        return False
    
machine_exists = check_podman_machine_exists()

def init_and_start_machine(e, mount_path, createConn_progress_ind, stream_logs_callback):
    global filepath
    if machine_exists:
        stream_logs_callback("INFO:     Podman machine already exists. Resetting.\n")
        try:
            process = subprocess.run(
                ["/opt/podman/bin/podman", "machine", "rm", "-f"],
                capture_output=True,
                text=True,
            )
            print(process.stdout)
        except FileNotFoundError:
            pass
    createConn_progress_ind.visible = True
    e.page.update()

    stream_logs_callback("INFO:     Initializing Podman machine...")
    # e.page.update()

    init_result = subprocess.run(
        ["/opt/podman/bin/podman", "machine", "init", "-v", f"{filepath}:{mount_path}"],
        capture_output=True,
        text=True,
    )

    if init_result.returncode == 0:
        stream_logs_callback("INFO:     Podman machine initialized successfully.\n")

        stream_logs_callback("INFO:     Starting Podman machine...\n")

        start_result = subprocess.run(
            ["/opt/podman/bin/podman", "machine", "start"],
            capture_output=True,
            text=True,
        )

        if start_result.returncode == 0:
            stream_logs_callback("INFO:     Podman machine started successfully.\n")
        else:
            stream_logs_callback("ERROR:    Failed to start Podman machine:\n")
            stream_logs_callback(start_result.stderr)
    else:
        stream_logs_callback("ERROR:    Failed to initialize Podman machine:\n")
        stream_logs_callback(init_result.stderr)

    createConn_progress_ind.visible = False
    e.page.update()


def build_container(e, createConn_progress_ind, stream_logs_callback):
    createConn_progress_ind.visible = True
    e.page.update()
    # Get environment variables for BEARER_TOKEN and SAVE_PATH
    bearer_token = kv_store.get("fTokn")
    save_path = kv_store.get("save_path")
    # export BEARER_TOKEN and SAVE_PATH as environment variables
    stream_logs_callback("INFO:     Building container image...")
    e.page.update()
    build_result = subprocess.run(
        [
            "/opt/podman/bin/podman",
            "build",
            "--build-arg",
            f"BEARER_TOKEN={bearer_token}",
            "--build-arg",
            f"SAVE_PATH={save_path}",
            "-t",
            "webhook-listener",
            "-f",
            "container/Containerfile",
            ".",
        ],
        capture_output=True,
        text=True,
    )
    if build_result.returncode == 0:
        stream_logs_callback("INFO:     Container image build successful.\n")
    else:
        stream_logs_callback("ERROR:    Failed to build container image:\n")
        stream_logs_callback(build_result.stderr)
    e.page.update()
    createConn_progress_ind.visible = False
    e.page.update()
