import can
import time
import os


# ===================== 用户配置 =====================
UPGRADE_BIN_PATH = r"/home/liu/Downloads/rs00_0.0.3.22.bin"

TARGET_MOTOR_ID = 0x03
HOST_ID = 0xFD

CAN_CHANNEL = "can0"
CAN_BITRATE = 1000000

TIMEOUT = 2.0
RETRY_CNT = 3


# ===================== 协议枚举 =====================
CANCOM_ANNOUNCE_DEVID = 0
CANCOM_OTA_START = 11
CANCOM_OTA_INFO = 12
CANCOM_OTA_ING = 13
CANCOM_OTA_END = 14

FEEDBACK_SUCCESS = 0x00
FEEDBACK_FAILED = 0xF0


class MotorOTA:

    def __init__(self):
        self.bus = None
        self.bin_data = b""
        self.bin_size = 0
        self.pack_number = 0
        self.pack_cnt = 0
        self.mcu_uid = None

    # ===================== 构造29位ID =====================
    def build_id(self, mode, data, dev_id):
        return (((mode & 0x1F) << 24)
                | ((data & 0xFFFF) << 8)
                | (dev_id & 0xFF)) & 0x1FFFFFFF

    # ===================== 解析29位ID =====================
    def parse_id(self, can_id):
        can_id &= 0x1FFFFFFF
        mode = (can_id >> 24) & 0x1F
        data = (can_id >> 8) & 0xFFFF
        dev_id = can_id & 0xFF
        return mode, data, dev_id

    # ===================== 初始化CAN =====================
    def init_can(self):
        self.bus = can.interface.Bus(
            channel=CAN_CHANNEL,
            interface="socketcan",
            bitrate=CAN_BITRATE
        )
        print("✅ CAN 初始化成功")

    # ===================== 发送并等待ACK =====================
    def send_and_wait_ack(self, mode, data, payload):

        tx_id = self.build_id(mode, data, TARGET_MOTOR_ID)

        msg = can.Message(
            arbitration_id=tx_id,
            data=payload,
            is_extended_id=True
        )

        for retry in range(RETRY_CNT):

            print(f"TX: {hex(tx_id)}")

            self.bus.send(msg)

            start = time.time()
            while time.time() - start < TIMEOUT:

                rx = self.bus.recv(timeout=0.1)
                if not rx or not rx.is_extended_id:
                    continue

                rx_mode, rx_data, rx_id = self.parse_id(rx.arbitration_id)

                # 必须是同模式
                if rx_mode != mode:
                    continue

                # 必须回给主机
                if rx_id != HOST_ID:
                    continue

                result = (rx_data >> 8) & 0xFF
                motor_id = rx_data & 0xFF

                if motor_id != TARGET_MOTOR_ID:
                    continue

                if result == FEEDBACK_SUCCESS:
                    return True, rx

                if result == FEEDBACK_FAILED:
                    return False, rx

            print("⚠ 超时重试...")
            time.sleep(0.05)

        return False, None

    # ===================== 获取设备ID =====================
    def get_device_id(self):

        print("📡 获取设备ID...")

        tx_id = self.build_id(
            CANCOM_ANNOUNCE_DEVID,
            HOST_ID,          # ❗ 这里不再 <<8
            TARGET_MOTOR_ID
        )

        msg = can.Message(
            arbitration_id=tx_id,
            data=[0] * 8,
            is_extended_id=True
        )

        self.bus.send(msg)

        start = time.time()
        while time.time() - start < TIMEOUT:

            rx = self.bus.recv(timeout=0.1)
            if not rx:
                continue

            mode, data, dev_id = self.parse_id(rx.arbitration_id)

            if mode != CANCOM_ANNOUNCE_DEVID:
                continue

            if dev_id != 0xFE:
                continue

            self.mcu_uid = rx.data
            print("✅ MCU UID:", self.mcu_uid.hex())
            return True

        print("❌ 获取设备ID失败")
        return False

    # ===================== 读取BIN =====================
    def read_bin(self, path):

        if not os.path.exists(path):
            print("❌ BIN文件不存在")
            return False

        with open(path, "rb") as f:
            self.bin_data = f.read()

        self.bin_size = len(self.bin_data)

        if self.bin_size == 0 or self.bin_size > 0x80000:
            print("❌ BIN非法")
            return False

        self.pack_number = (self.bin_size + 7) // 8

        print(f"BIN大小: {self.bin_size}")
        print(f"总包数: {self.pack_number}")

        return True

    # ===================== OTA流程 =====================
    def start_upgrade(self, path):

        self.init_can()

        if not self.read_bin(path):
            return

        if not self.get_device_id():
            return

        # ===== START =====
        ok, _ = self.send_and_wait_ack(
            CANCOM_OTA_START,
            HOST_ID,
            list(self.mcu_uid)
        )
        if not ok:
            print("❌ START失败")
            return

        # ===== INFO =====
        payload = list(self.bin_size.to_bytes(4, "little"))
        payload += list(self.pack_number.to_bytes(4, "little"))

        ok, _ = self.send_and_wait_ack(
            CANCOM_OTA_INFO,
            HOST_ID,
            payload
        )
        if not ok:
            print("❌ INFO失败")
            return

        # ===== ING =====
        self.pack_cnt = 0

        while self.pack_cnt < self.pack_number:

            start_index = self.pack_cnt * 8
            chunk = self.bin_data[start_index:start_index+8]
            payload = list(chunk) + [0xFF]*(8-len(chunk))

            ok, rx = self.send_and_wait_ack(
                CANCOM_OTA_ING,
                self.pack_cnt,
                payload
            )

            if ok:
                self.pack_cnt += 1
                if self.pack_cnt % 100 == 0:
                    print(f"进度: {self.pack_cnt}/{self.pack_number}")
            else:
                if rx:
                    resend_cnt = int.from_bytes(rx.data[0:2], "little")
                    print("🔁 断点续传:", resend_cnt)
                    self.pack_cnt = resend_cnt
                else:
                    print("❌ ING失败")
                    return

        # ===== END =====
        payload = list(self.pack_number.to_bytes(4, "little")) + [0]*4

        ok, _ = self.send_and_wait_ack(
            CANCOM_OTA_END,
            0,
            payload
        )

        if ok:
            print("🎉 OTA升级完成")
        else:
            print("❌ END失败")


# ===================== 主程序 =====================
if __name__ == "__main__":
    ota = MotorOTA()
    ota.start_upgrade(UPGRADE_BIN_PATH)