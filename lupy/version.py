from .fdtd_manager import get_fdtd_instance

def version():
    FD = get_fdtd_instance()
    return FD.version()