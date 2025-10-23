from proxy_clients import vless, vmess, shadowsocks, trojan


class AdminProtocolsService:
    @staticmethod
    async def test_protocol(protocol: str, user_id: str):
        """Тестирование протокола"""
        try:
            if protocol == "vless":
                result = await vless.create_vless_client(user_id)
            elif protocol == "vmess":
                result = await vmess.create_vmess_client(user_id)
            elif protocol == "shadowsocks":
                result = await shadowsocks.create_ss_client(user_id)
            elif protocol == "trojan":
                result = await trojan.create_trojan_client(user_id)
            else:
                return {"success": False, "error": "Неизвестный протокол"}

            return {
                "success": True,
                "data": result,
                "protocol": protocol.upper()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "protocol": protocol.upper()
            }

    @staticmethod
    async def format_test_result(test_result: dict) -> str:
        """Форматирование результата теста"""
        if test_result['success']:
            data = test_result['data']
            return (
                f"✅ **Тест {test_result['protocol']} - УСПЕШНО**\n\n"
                f"**Конфиг создан:** Да\n"
                f"**Действует:** {data['expiry_time']} дней\n"
                f"**Статус:** Активен\n\n"
                f"```\n{data['connection_string']}\n```"
            )
        else:
            return (
                f"❌ **Тест {test_result['protocol']} - ОШИБКА**\n\n"
                f"Ошибка: {test_result['error']}"
            )
