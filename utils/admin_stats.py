from database.postgres import db
from proxy_clients import vless, vmess, shadowsocks, trojan
from config import VLESS_INBOUND_ID, VMESS_INBOUND_ID, SHADOWSOCKS_INBOUND_ID, TROJAN_INBOUND_ID


class AdminStatsService:
    @staticmethod
    async def get_basic_stats():
        """Базовая статистика системы из БД и X-UI"""
        total_users = await db.get_users_count()
        new_today = await db.get_new_users_today()

        # Получаем реальную статистику по протоколам из X-UI
        protocol_stats = await AdminStatsService._get_protocol_stats()
        total_active = sum(protocol_stats.values())

        return {
            "total_users": total_users,
            "active_users": total_active,
            "new_today": new_today,
            "protocol_stats": protocol_stats
        }

    @staticmethod
    async def get_detailed_stats():
        """Детальная статистика из БД и X-UI"""
        total_users = await db.get_users_count()
        new_today = await db.get_new_users_today()

        # Получаем детальную статистику по протоколам
        protocol_stats = await AdminStatsService._get_protocol_stats_detailed()
        total_active = sum(stats['total'] for stats in protocol_stats.values())

        return {
            "total_users": total_users,
            "active_users": total_active,
            "new_today": new_today,
            "inactive_users": total_users - total_active,
            "protocol_stats": protocol_stats
        }

    @staticmethod
    async def _get_protocol_stats():
        """Получить общую статистику по протоколам из X-UI"""
        try:
            # Получаем клиентов из всех inbound'ов
            vless_clients = await vless.get_vless_clients(VLESS_INBOUND_ID)
            vmess_clients = await vmess.get_vmess_clients(VMESS_INBOUND_ID)
            ss_clients = await shadowsocks.get_ss_clients(SHADOWSOCKS_INBOUND_ID)
            trojan_clients = await trojan.get_trojan_clients(TROJAN_INBOUND_ID)

            # Считаем активных клиентов (с enable=True)
            vless_active = sum(1 for client in vless_clients if client.enable)
            vmess_active = sum(1 for client in vmess_clients if client.enable)
            ss_active = sum(1 for client in ss_clients if client.enable)
            trojan_active = sum(1 for client in trojan_clients if client.enable)

            return {
                "vless": vless_active,
                "vmess": vmess_active,
                "shadowsocks": ss_active,
                "trojan": trojan_active
            }

        except Exception as e:
            print(f"Ошибка получения статистики протоколов: {e}")
            return {"vless": 0, "vmess": 0, "shadowsocks": 0, "trojan": 0}

    @staticmethod
    async def _get_protocol_stats_detailed():
        """Получить детальную статистику по протоколам"""
        try:
            vless_clients = await vless.get_vless_clients(VLESS_INBOUND_ID)
            vmess_clients = await vmess.get_vmess_clients(VMESS_INBOUND_ID)
            ss_clients = await shadowsocks.get_ss_clients(SHADOWSOCKS_INBOUND_ID)
            trojan_clients = await trojan.get_trojan_clients(TROJAN_INBOUND_ID)

            def get_client_stats(clients):
                total = len(clients)
                active = sum(1 for client in clients if client.enable)
                inactive = total - active
                return {"total": total, "active": active, "inactive": inactive}

            return {
                "vless": get_client_stats(vless_clients),
                "vmess": get_client_stats(vmess_clients),
                "shadowsocks": get_client_stats(ss_clients),
                "trojan": get_client_stats(trojan_clients)
            }

        except Exception as e:
            print(f"Ошибка получения детальной статистики: {e}")
            empty_stats = {"total": 0, "active": 0, "inactive": 0}
            return {"vless": empty_stats, "vmess": empty_stats, "shadowsocks": empty_stats, "trojan": empty_stats}

    @staticmethod
    async def format_basic_stats(stats: dict) -> str:
        """Форматирование базовой статистики в текст"""
        protocol_stats = stats['protocol_stats']

        return (
            "📊 **Статистика системы**\n\n"
            f"• Пользователей всего: {stats['total_users']}\n"
            f"• Активных пользователей: {stats['active_users']}\n"
            f"• Новых за сегодня: {stats['new_today']}\n\n"
            "**По протоколам:**\n"
            f"• VLESS: {protocol_stats['vless']} активных\n"
            f"• VMess: {protocol_stats['vmess']} активных\n"
            f"• Shadowsocks: {protocol_stats['shadowsocks']} активных\n"
            f"• Trojan: {protocol_stats['trojan']} активных"
        )

    @staticmethod
    async def format_detailed_stats(stats: dict) -> str:
        """Форматирование детальной статистики в текст"""
        protocol_stats = stats['protocol_stats']

        text = (
            "📈 **Детальная статистика**\n\n"
            f"• Всего пользователей: {stats['total_users']}\n"
            f"• Активных: {stats['active_users']}\n"
            f"• Неактивных: {stats['inactive_users']}\n"
            f"• Новых за сегодня: {stats['new_today']}\n\n"
            "**Статистика по протоколам:**\n"
        )

        for protocol, data in protocol_stats.items():
            text += (
                f"• {protocol.upper()}: {data['active']} активных, "
                f"{data['inactive']} неактивных (всего: {data['total']})\n"
            )

        return text
