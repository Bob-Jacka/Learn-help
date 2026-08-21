try:
    from device_lib.devices.virtual.IVirtDevice import IVirtDevice
    from device_lib.devices.virtual.Yandex_driver import Yandex_driver
except ModuleNotFoundError as e:
    print(f'No available modules found: {e}')


class Data_driver:
    data_driver: IVirtDevice | None = None

    def __init__(self):
        pass

    def start_driver(self):
        self.data_driver = Yandex_driver.create_yandex_virt_device(None)
