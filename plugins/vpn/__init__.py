from core.plugins.registry import register_plugin
from .handlers import entry_point

register_plugin("🛡 VPN", entry_point)
