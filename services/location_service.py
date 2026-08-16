import unicodedata


# Danh sách 63 tỉnh/thành phố
PROVINCES = [
    "An Giang",
    "Bà Rịa - Vũng Tàu",
    "Bắc Giang",
    "Bắc Kạn",
    "Bạc Liêu",
    "Bắc Ninh",
    "Bến Tre",
    "Bình Định",
    "Bình Dương",
    "Bình Phước",
    "Bình Thuận",
    "Cà Mau",
    "Cao Bằng",
    "Cần Thơ",
    "Đà Nẵng",
    "Đắk Lắk",
    "Đắk Nông",
    "Điện Biên",
    "Đồng Nai",
    "Đồng Tháp",
    "Gia Lai",
    "Hà Giang",
    "Hà Nam",
    "Hà Nội",
    "Hà Tĩnh",
    "Hải Dương",
    "Hải Phòng",
    "Hậu Giang",
    "Hòa Bình",
    "Hưng Yên",
    "Khánh Hòa",
    "Kiên Giang",
    "Kon Tum",
    "Lai Châu",
    "Lâm Đồng",
    "Lạng Sơn",
    "Lào Cai",
    "Long An",
    "Nam Định",
    "Nghệ An",
    "Ninh Bình",
    "Ninh Thuận",
    "Phú Thọ",
    "Phú Yên",
    "Quảng Bình",
    "Quảng Nam",
    "Quảng Ngãi",
    "Quảng Ninh",
    "Quảng Trị",
    "Sóc Trăng",
    "Sơn La",
    "Tây Ninh",
    "Thái Bình",
    "Thái Nguyên",
    "Thanh Hóa",
    "Thừa Thiên Huế",
    "Tiền Giang",
    "TP Hồ Chí Minh",
    "Trà Vinh",
    "Tuyên Quang",
    "Vĩnh Long",
    "Vĩnh Phúc",
    "Yên Bái",
]


def normalize_text(text):
    """
    Chuẩn hóa chuỗi để so sánh:
    - bỏ khoảng trắng thừa
    - không phân biệt hoa/thường
    - không phân biệt dấu tiếng Việt
    """

    text = text.strip().lower()

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    text = text.replace("đ", "d")

    return " ".join(text.split())


def validate_province(address):
    """
    Kiểm tra tên tỉnh/thành phố có đầy đủ và hợp lệ hay không.
    """

    if not address:
        return {
            "valid": False,
            "province": None,
            "message": "Chưa nhập tỉnh/thành phố."
        }

    input_normalized = normalize_text(address)

    # Không chấp nhận chuỗi quá ngắn
    if len(input_normalized) < 3:
        return {
            "valid": False,
            "province": None,
            "message": "Tên tỉnh/thành phố quá ngắn."
        }

    for province in PROVINCES:

        if normalize_text(province) == input_normalized:

            return {
                "valid": True,
                "province": province,
                "message": "Tỉnh/thành phố hợp lệ."
            }

    return {
        "valid": False,
        "province": None,
        "message": (
            "Không tìm thấy tỉnh/thành phố. "
            "Vui lòng nhập đầy đủ tên."
        )
    }