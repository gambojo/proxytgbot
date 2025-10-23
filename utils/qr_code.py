import qrcode
from io import BytesIO
from aiogram.types import BufferedInputFile


async def create_qr_code(connection_string: str) -> BufferedInputFile:
    """Создает QR-код из строки подключения и возвращает как файл для Telegram"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(connection_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Конвертируем в bytes без сохранения на диск
    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)

    return BufferedInputFile(bio.read(), filename="qrcode.png")