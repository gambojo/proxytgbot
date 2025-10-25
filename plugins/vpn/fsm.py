from enum import Enum

# 🛡 Сценарий создания VPN
class VpnState(Enum):
    AWAITING_NAME = "vpn:awaiting_name"
    AWAITING_DURATION = "vpn:awaiting_duration"
    AWAITING_CONFIRMATION = "vpn:awaiting_confirmation"

# 📄 Сценарий просмотра/удаления VPN
class VpnManageState(Enum):
    AWAITING_SELECTION = "vpn:awaiting_selection"
    AWAITING_DELETION_CONFIRM = "vpn:awaiting_deletion_confirm"
